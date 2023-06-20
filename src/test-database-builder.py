import sqlite3 as sqlite
import shutil
import os

if 'database.sqlite' not in os.listdir('./'):
    raise Exception("database.sqlite file not found, please create it and go from there..")

shutil.copyfile('database.sqlite', 'database-test.sqlite')

cnx = sqlite.connect('database-test.sqlite')
cur = cnx.cursor()
cur.execute("SELECT * FROM SQLite_master")
tables = cur.fetchall()

to_check = []

for i in range(len(tables)):
    if 'token' in tables[i][-1].lower():
        to_check.append(tables[i])

for i in range(len(to_check)):
    table = to_check[i][1]
    if 'view' not in to_check[i][0]:
        column = to_check[i][-1].replace('\n', ' ').replace('\t','').split(', ')[-2].split(' ')[0]
        if 'token' in column:
            cur.execute("UPDATE " + table + " SET " + column + "=\"\"") # Delete all tokens, because we don't want to publish these
cnx.commit()
