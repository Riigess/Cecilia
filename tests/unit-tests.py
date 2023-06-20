import pytest
import json

import sqlite3 as sqlite

#Importing application from another location for use...
import sys
import os
sys.path.insert(0, '../src/')
from Database.SQLConnector import SQLConnector

def test_unit_fetch_codenames_test():
    cnx = sqlite.connect('../src/database-test.sqlite')
    cur = cnx.cursor()
    cur.execute('SELECT * FROM Codenames')
    a = cur.fetchall()
    resp = [i[0] for i in a]
    s = SQLConnector('../src/database-test.sqlite')
    resp_s = [i['id'] for i in s.get_from_table('Codenames', column='id')]
    assert resp_s == resp
    assert type(resp_s) is type(resp)
    assert type(resp_s) is type([''])

def test_all_ipsw_devices():
    cnx = sqlite.connect('../src/database-test.sqlite')
    cur = cnx.cursor()
    cur.execute('SELECT * FROM AppleDevices')
    resp = cur.fetchall()
    s = SQLConnector('../src/database-test.sqlite')
    resp_s = s.get_from_table('AppleDevices')
    assert len(resp_s) == len(resp)
    assert type(resp_s) is type([{}])
    assert type(resp) is type([()])