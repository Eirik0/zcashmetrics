#!/usr/bin/env python2

import dbwrapper
from dbwrapper import ColumnDef, TableDef

TABLE_DEFS = (
    [
        TableDef('Block',
            [
                ColumnDef('Height', 'INTEGER', True),
                ColumnDef('Time', 'BIGINT'),
                ColumnDef('NumTxs', 'INTEGER')
            ]),
        TableDef('Tx',
            [
                ColumnDef('TxId', 'BYTEA', True),
                ColumnDef('Block', 'INTEGER'),
                ColumnDef('CoinBase', 'BOOLEAN'),
                ColumnDef('NumVIn', 'INTEGER'),
                ColumnDef('NumVOut', 'INTEGER'),
                ColumnDef('NumVJoinSplit', 'INTEGER')
            ]),
        TableDef('VIn',
            [
                ColumnDef('TxId', 'BYTEA', True),
                ColumnDef('PrevN', 'INTEGER', True),
                ColumnDef('PrevTxId', 'BYTEA')
            ]),
        TableDef('VOut',
            [
                ColumnDef('TxId', 'BYTEA', True),
                ColumnDef('N', 'INTEGER', True),
                ColumnDef('Value', 'BIGINT')
            ]),
        TableDef('VJoinSplit',
            [
                ColumnDef('TxId', 'BYTEA', True),
                ColumnDef('N', 'INTEGER', True),
                ColumnDef('VPubOld', 'BIGINT'),
                ColumnDef('VPubNew', 'BIGINT')
            ])
    ])

def ensureTablesExist():
    connection = dbwrapper.openConnection()
    try:
        for tableDef in TABLE_DEFS:
            dbwrapper.ensureTableExists(connection, tableDef)
    finally:
        if connection:
            connection.close()