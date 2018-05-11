#!/usr/bin/env python2

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

ZCASH_DB_NAME = 'ZCashMetrics'

class ColumnDef:
    def __init__(self, columnName, columnType, isPrimaryKey = False):
        self.columnName = columnName
        self.columnType = columnType
        self.isPrimaryKey = isPrimaryKey

    def toQueryString(self):
        return "{} {}".format(self.columnName, self.columnType)

class TableDef:
    def __init__(self, tableName, columnList):
        self.tableName = tableName
        self.columnList = columnList

    def toQueryString(self):
        columnString = ", ".join(column.toQueryString() for column in self.columnList)
        primaryKeyString = ", ".join(column.columnName for column in self.columnList if column.isPrimaryKey)
        return "{} ({}, PRIMARY KEY({}))".format(self.tableName, columnString, primaryKeyString)

def openConnection(dbName = ZCASH_DB_NAME.lower()):
    try:
        connection = psycopg2.connect(dbname = dbName, user = 'postgres', host = 'localhost', password = 'password')
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    except Exception as e:
        print "ERROR: Count not connect to database: {}".format(dbName)
        print e
        exit(0)

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
        exit(0)
    finally:
        connection.close()

# Create table (tableDef.tableName) if it does not exist
def ensureTableExists(connection, tableDef):
    try:
        cursor = connection.cursor()
        query = ("SELECT EXISTS("
                    "SELECT 1 FROM information_schema.tables " 
                    "WHERE lower(table_catalog)=lower(%s) AND " 
                    "table_schema='public' AND " 
                    "lower(table_name)=lower(%s))")
        cursor.execute(query, [ZCASH_DB_NAME, tableDef.tableName])
        if not cursor.fetchone()[0]:
            print "Creating table: {}".format(tableDef.toQueryString())
            cursor.execute("CREATE TABLE {}".format(tableDef.toQueryString()))
    except Exception as e:
        print "ERROR: Unable to find or create table {}".format(tableDef.tableName)
        print e
        exit(0)