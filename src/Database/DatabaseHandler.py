#Using MySQL, let's get going...
# import sqlite3 as sqlite
from datetime import datetime
import requests

import json
import os

from Database.RiotEndpoints import RiotEndpoints
from Database.SQLConnector import SQLConnector
from Debugging.Debugger import Debugger #Import the debugger OwO

class DatabaseHandler:
    #Connect to database and (temporarily) staticly set token information from the database
    def __init__(self, database_file:str):
        self.sql_connector = SQLConnector(database_file)
        self.database_file = database_file
        self.debugger = Debugger()
    
    def fetch_codenames(self) -> dict:
        resp = self.sql_connector.get_from_table('Codenames')
        to_return = [r['id'] for r in resp]
        return {'codenames':to_return}

    #This should fetch a URL scheme, headers, and then append some data to the URL..
    def fetch_from_codename(self, codename:str, data) -> dict:
        response = self.sql_connector.find_cache("CodenameTokens", "id", codename)
        resp = []
        if len(response) > 0:
            resp = response[0]
        if len(resp) == 0:
            raise Exception("Issue collecting content from SQLConnector, please verify we're using the correct method for this.")
        reference_link = resp['url']
        headers = {resp['headerValue']:resp['token']}
        #If the url does not end with /, then add one so we can use the '/'.join(data) part..
        if '/' not in reference_link[-1]:
            reference_link = reference_link + '/'
        return self.fetch_or_cache(url=reference_link + '/'.join(data), request_headers=headers)

    #This works, so basically what happens here is that we get a URLRequest but we want to validate we haven't searched for that URL before. If we have searched for it before, we're fetching our tabled copy, and if we haven't searched for it before then we're fetching a new copy.
    def fetch_or_cache(self, url:str, request_headers:dict) -> dict:
        cache = self.sql_connector.find_cache('URLRequests', 'url', url)
        if len(cache) > 0:
            expiry_date = cache[-1]['expiryDate']
            if type(expiry_date) is type(None):
                expiry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S") > datetime.now(): #If the expiryDate field is beyond 'now'
                return cache[-2]['data']
        req = requests.get(url, headers=request_headers)
        resp = {}
        try:
            resp = req.json()
        except:
            resp = json.loads(req.text.replace("'", '"'))
        if len(list(resp)) > 1:
            if '127.0.0.1' not in url:
                expiry_date = datetime.now()
                expiry_date = datetime(expiry_date.year, expiry_date.month, expiry_date.day + 1, expiry_date.hour, expiry_date.minute, expiry_date.second)
                # self.sql_connector.add_cache('URLRequests', ['url', 'data', 'date', 'expiryDate'], [url, json.dumps(resp).replace("\"", "'"), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), expiry_date.strftime("%Y-%m-%d %H:%M:%S")])
                self.sql_connector.add_cache('URLRequests', dict=resp)
                return resp
        else:
            raise Exception("Error completing fetch request. Please check connection and validate the headers are correct and try again.")
     
    def always_fetch_new(self, url:str, request_headers:dict):
        req = requests.get(url, headers=request_headers)
        resp = {}
        try:
            resp = req.json()
        except:
            resp = json.loads(req.text.replace("'", '"'))
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(list(resp)) > 1:
            if '127.0.0.1' not in url:
                self.sql_connector.add_cache('URLRequests', ['url', 'data', 'date'], [url, json.dumps(resp).replace("'", '"'), date])
            return {'url':url, 'data':resp, 'date': date}
        else:
            raise Exception("Error completing request. Data for url - %s - returned empty." % url)

    def add_codename(self, codename:str, url:str, request_headers:dict) -> dict:
        token_header = {}
        if len(list(request_headers)) > 1:
            for i in range(len(list(request_headers))):
                if 'token' in list(request_headers)[i].lower():
                    header = list(request_headers)[i]
                    token_header.update({header:request_headers[header]})
        else:
            token_header = request_headers
        self.sql_connector.add_cache('APITokens', ['id', 'serviceName', 'headerValue', 'token'], ['(SELECT count(*)+1 FROM APITokens)', codename, url, list(token_header)[0], token_header[list(token_header)[0]]])
        self.sql_connector.add_cache('Codenames', ['id', 'url', 'token_id'], [codename, url, '(SELECT count(*) FROM APITokens)'])
        return {'id':codename, 'url':url, 'token_header':list(token_header)[0]}
    
    def fetch_riot_account_by_name(self, endpoint:RiotEndpoints, name:str):
        token = self.sql_connector.get_from_table('APITokens', 'token')[0]['token']
        return self.fetch_or_cache(f"https://{endpoint.value}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", request_headers={'X-Riot-Token':token})

    def fetch_riot_account_by_id(self, endpoint:RiotEndpoints, account_id:str):
        token = self.sql_connector.get_from_table('APITokens', 'token')[0]['token']
        return self.fetch_or_cache(f"https://{endpoint.value}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{account_id}", request_headers={'X-Riot-Token': token})
