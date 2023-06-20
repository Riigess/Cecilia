import sqlite3 as sql
from datetime import datetime

class SQLConnector:
    def __init__(self, database_file:str):
        self.database_file = database_file
    
    def find_cache(self, table:str, column:str, data:str):
        cnx = sql.connect(self.database_file)
        cur = cnx.cursor()
        cur.execute('SELECT * FROM %s WHERE %s LIKE "%s"' % (table, column, data))
        headers = [i[0] for i in cur.description]
        resp = cur.fetchall()
        to_return = []
        for arr in resp:
            to_return.append({})
            for i in range(len(arr)):
                to_return[-1].update({headers[i]:arr[i]})
        return to_return
    
    #TODO: Build a filter against duplicating cached data.
    #TODO: Continue to build out **data connector. Sample response data should be viewed using kwargs references here - https://realpython.com/python-kwargs-and-args/
    def add_cache(self, table:str, **data):
        cnx = sql.connect(self.database_file)
        cur = cnx.cursor()
        cur.execute(f"SELECT * FROM {table}")
        columns = [i[0] for i in cur.description]
        
        cur.execute('SELECT * FROM %s WHERE %s="%s"' % (table, columns[0], data[0]))
        if len(cur.fetchall()) > 0:
            for i in range(len(columns)):
                if 'time' in columns[i] and 'expir' in columns[i]:
                    date = datetime.strptime(data[i], '%Y-%m-%d %H:%M:%S')
                    #TODO: Finish out timeline as part of something that should warrant passing off the issue
        command = "INSERT INTO %s(" % table
        for i in range(len(columns)):
            if len(columns) - 1 != i:
                command += columns[i] + ','
            else:
                command += columns[i] + ') '
        command += "VALUES ("
        for i in range(len(data)):
            if len(data) - 1 != i:
                if type(data[i]) is type(""):
                    command += '"%s",' % data[i]
                else:
                    command += data[i] + ','
            else:
                if type(data[i]) is type(""):
                    command += '"%s")' % data[i]
                else:
                    command += data[i] + ')'
        cur.execute(command)
        cnx.commit()
    
    def get_from_table(self, table:str, column='*'):
        cnx = sql.connect(self.database_file)
        cur = cnx.cursor()
        cur.execute('SELECT %s FROM %s' % (column, table))
        headers = [i[0] for i in cur.description]
        resp = cur.fetchall()
        to_return = []
        for i in range(len(resp)):
            to_return.append({})
            for j in range(len(headers)):
                to_return[-1].update({headers[j]:resp[i][j]})
        return to_return
