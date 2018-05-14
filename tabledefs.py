#!/usr/bin/env python2

class ColumnDef:
    def __init__(self, columnName, columnType, isPrimaryKey = False):
        self.columnName = columnName
        self.columnType = columnType
        self.isPrimaryKey = isPrimaryKey

    def getCreateTableString(self):
        return "{} {}".format(self.columnName, self.columnType)

class TableDef:
    def __init__(self, tableName, columnList):
        self.tableName = tableName
        self.columnList = columnList

    def getCreateTableString(self):
        columnString = ", ".join(column.getCreateTableString() for column in self.columnList)
        primaryKeyString = ", ".join(column.columnName for column in self.columnList if column.isPrimaryKey)
        return "{} ({}, PRIMARY KEY({}))".format(self.tableName, columnString, primaryKeyString)

ZCASH_DB_NAME = 'ZCashMetrics'

TABLE_DEFS = (
    [
        TableDef('Block',
            [
                ColumnDef('Height', 'INTEGER', True),
                ColumnDef('Time', 'BIGINT'),
                ColumnDef('NumTx', 'INTEGER')
            ]),
        TableDef('Tx',
            [
                ColumnDef('TxId', 'BYTEA', True),
                ColumnDef('BlockHeight', 'INTEGER'),
                ColumnDef('CoinBase', 'BOOLEAN'),
                ColumnDef('NumVIn', 'INTEGER'),
                ColumnDef('NumVOut', 'INTEGER'),
                ColumnDef('NumVJoinSplit', 'INTEGER')
            ]),
        TableDef('VIn',
            [
                ColumnDef('TxId', 'BYTEA'),
                ColumnDef('PrevTxId', 'BYTEA', True),
                ColumnDef('PrevN', 'INTEGER', True)
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
                ColumnDef('VPubOld', 'BIGINT'), # Out
                ColumnDef('VPubNew', 'BIGINT')  # In
            ])
    ])

BLOCK_INSERT_QUERY = ("INSERT INTO Block (Height, Time, NumTx)"
        "VALUES (%s, %s, %s)"
        "ON CONFLICT (Height) DO NOTHING")
TX_INSERT_QUERY = ("INSERT INTO Tx (TxId, BlockHeight, CoinBase, NumVIn, NumVOut, NumVJoinSplit) "
        "VALUES (decode(%s, 'hex'), %s, %s, %s, %s, %s) "
        "ON CONFLICT (TxId) DO NOTHING")
VIN_INSERT_QUERY = ("INSERT INTO VIn (TxId, PrevTxId, PrevN)"
        "VALUES (decode(%s, 'hex'), decode(%s, 'hex'), %s) "
        "ON CONFLICT (PrevTxId, PrevN) DO NOTHING")
VOUT_INSERT_QUERY = ("INSERT INTO VOut (TxId, N, Value)"
        "VALUES (decode(%s, 'hex'), %s, %s)"
        "ON CONFLICT (TxId, N) DO NOTHING")
VJOINSPLIT_INSERT_QUERY = ("INSERT INTO VJoinSplit (TxId, N, VPubOld, VPubNew)"
        "VALUES (decode(%s, 'hex'), %s, %s, %s)"
        "ON CONFLICT (TxId, N) DO NOTHING")