import sqlite3
from sqlite3 import Error
import re


class Database():
    def __init__(self, file=':memory:'):
        self.file=file
        self.conn = sqlite3.connect(self.file)    
        self.cursor = self.conn.cursor()

    def createTbl(self, tblName, tblStruct):
        cols = ','.join([str(x) for t in list(tblStruct.items()) for x in t])
        cols = re.sub(',([^,]*,?)', r' \1', cols)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tblName} ({cols});")

    def getTblInfo(self, tblName): 
        pragma = f"PRAGMA table_info({tblName});"
        self.cursor.execute(pragma)
        return self.cursor.fetchall()

    def getTblCols(self, tblName):
        tblInfo = self.getTblInfo(tblName)
        columns = [x[1] for x in tblInfo]
        return columns

    def checkTbl(self, checkQuery):      
        self.cursor.execute(checkQuery)
        result = self.cursor.fetchall()
        return result

    def insert(self, tblName, data, check=True):
        counter = 0
        if check:
            cols = ','.join(self.getTblCols(tblName))
        else:
            cols = self.getTblCols(tblName)
            cols.remove("id")
            cols = ','.join(cols)
        for item in data:
            if check:
                sqlCheck = f"SELECT * FROM {tblName} WHERE id = {item[0]};"
                result = self.checkTbl(sqlCheck)
            else:
                result = []
            if len(result) == 0:
                values = ",".join(f"'{i}'" for i in item)           
                sql = f"INSERT INTO {tblName} ({cols}) VALUES ({values});"
                self.cursor.execute(sql)
                counter += 1
            else:
                print(f"Element with ID {item[0]} already exists in {tblName}.")
        print(f"Inserted {counter} new elements to {tblName}.")

    def selectAll(self, tblName):
        sql = f"SELECT * FROM {tblName};"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update(self, tblName, compareColumn):
        query = f"SELECT {compareColumn} from {tblName};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def updateVals(self, tblName, playersData):
        toUpdate = self.update(tblName, "id")
        marketVals = [x[4] for x in playersData]
        trends = [x[5] for x in playersData]
        ids = [x[0] for x in toUpdate]
        counter = 0
        for id in ids:
            index = ids.index(id)
            query = f"UPDATE {tblName} SET value = {marketVals[index]} WHERE id = {id};"
            query2 = f"UPDATE {tblName} SET trend = {trends[index]} WHERE id = {id};"
            self.cursor.execute(query)
            self.cursor.execute(query2)
            counter += 1
        print(f"Updated {counter} elements in {tblName}.")
        
    def delete(self, tblName, elementsToDel):
        for i in elementsToDel:
            self.select(f"DELETE FROM {tblName} WHERE id = {i};")
            print(f"Deleted element with id {i} from {tblName}." )

    def __enter__(self):
        return self
            
       
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


class DatabaseHelpers():
    def __init__(self, columnNames):
        self.columnNames = columnNames

    def pyType2sqliteType(self, type):
        if type == "str":
            return "TEXT"
        elif type== "int":
            return "INTEGER"
        elif type== "float":
            return "REAL"
        else:
            return "UNKNOWN"

    def getSqlTypes(self, cols):
        types = list()
        for col in cols:
            typ = type(col).__name__
            sqlType = self.pyType2sqliteType(typ)
            types.append(sqlType)
        return types

    def getTblStructure(self, columns):
        sqlDict = dict(zip(self.columnNames, self.getSqlTypes(columns)))
        return sqlDict

