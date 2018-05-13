#!/usr/bin/env python2

from tabledefs import TABLE_DEFS, ZCASH_DB_NAME

import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def openConnection(dbName = ZCASH_DB_NAME.lower()):
    try:
        connection = psycopg2.connect(dbname = dbName, user = 'postgres', host = 'localhost', password = 'password')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    except Exception as e:
        print "ERROR: Count not connect to database: {}".format(dbName)
        print e
        exit(1)

# Create database (ZCASH_DB_NAME) if it does not exist
def ensureDatabaseExists():
    # Open connection to default database
    connection = openConnection('postgres')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_database WHERE lower(datname) = lower(%s))", [ZCASH_DB_NAME])
        if not cursor.fetchone()[0]:
            print "Creating databse: {}".format(ZCASH_DB_NAME)
            cursor.execute("CREATE DATABASE {}".format(ZCASH_DB_NAME))
    except Exception as e:
        print "ERROR: Unable to find or create dabatase: {}".format(ZCASH_DB_NAME)
        print e
        exit(1)
    finally:
        connection.close()

# Create table (tableDef.tableName) if it does not exist
def ensureTableExists(connection, tableDef):
    try:
        cursor = connection.cursor()
        query = ("SELECT EXISTS("
                "SELECT 1 FROM information_schema.tables " 
                "WHERE lower(table_catalog) = lower(%s) AND " 
                "table_schema = 'public' AND " 
                "lower(table_name) = lower(%s))")
        cursor.execute(query, [ZCASH_DB_NAME, tableDef.tableName])
        if not cursor.fetchone()[0]:
            print "Creating table: {}".format(tableDef.getCreateTableString())
            cursor.execute("CREATE TABLE {}".format(tableDef.getCreateTableString()))
    except Exception as e:
        print "ERROR: Unable to find or create table {}".format(tableDef.tableName)
        print e
        exit(1)

def ensureTablesExist():
    connection = openConnection()
    try:
        for tableDef in TABLE_DEFS:
            ensureTableExists(connection, tableDef)
    finally:
        if connection:
            connection.close()
