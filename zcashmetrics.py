#!/usr/bin/env python2

from tabledefs import BLOCK_INSERT_QUERY, TX_INSERT_QUERY
from progresstracker import formatTime, ProgressTracker

import tabledefs
import dbwrapper

import sys

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

if len(sys.argv) > 3:
    print "Usage: python privacymetrics.py (BLOCKFROM) (BLOCKTO)"
    exit(1)

# Make sure the database and tables exist
dbwrapper.ensureDatabaseExists()
dbwrapper.ensureTablesExist()

# Have a local running instance of zcashd
api = AuthServiceProxy("http://username:password@127.0.0.1:8232")

# Open a connection to the database
connection = dbwrapper.openConnection()
cursor = connection.cursor()

try:
    block_from = 0
    chain_height = api.getblockcount()
    if len(sys.argv) == 1 or sys.argv[1] == '-':
        cursor.execute("SELECT COALESCE(MAX(Height), -1) FROM Block")
        block_from = cursor.fetchone()[0] + 1
    else:
        block_from = int(sys.argv[1])
    block_to = min(int(sys.argv[2]), chain_height) if len(sys.argv) > 2 else chain_height

    if block_from >= block_to:
        print "\nInvalid block range: {}-{}\n".format(block_from, block_to)
        exit(0)
    
    print "\nloading blocks {}-{}...\n".format(block_from, block_to)
    
    progress_tracker = ProgressTracker()
    total_blocks = block_to - block_from + 1
    blocks_loaded = 0
    
    # Add transactions and blocks to the database
    for block_height in xrange(block_from, block_to + 1): # +1 so inclusive
        block = api.getblock("{}".format(block_height), 2)
        txs = block["tx"]
        
        for tx in txs:
            txid = tx["txid"]
            vins = tx["vin"]
            vouts = tx["vout"]
            joinsplits = tx["vjoinsplit"]
            is_coinbase = len(vins) == 1 and "coinbase" in vins[0]
            
            cursor.execute(TX_INSERT_QUERY, [txid, block_height, is_coinbase, len(vins), len(vouts), len(joinsplits)])
            if not is_coinbase:
                tabledefs.executeVInInsertQuery(cursor, [[txid, vin["txid"], vin["vout"]] for vin in vins])
            tabledefs.executeVOutInsertQuery(cursor, [[txid, index, vout["value"] * 100000000] for index, vout in enumerate(vouts)])
            tabledefs.executeVJoinSplitInsertQuery(cursor, [[txid, index, joinsplit["vpub_old"] * 100000000, joinsplit["vpub_new"] * 100000000] for index, joinsplit in enumerate(joinsplits)])
        
        cursor.execute(BLOCK_INSERT_QUERY, [block_height, block["time"], len(txs)])
        
        blocks_loaded += 1
        progress_tracker.setProgress(blocks_loaded, total_blocks)

    print "\n{} blocks processed in {}\n".format(blocks_loaded, formatTime(progress_tracker.getTimeElapsed()))

finally:
    if connection:
        connection.close()