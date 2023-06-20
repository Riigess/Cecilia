## Start the initial connection and database handler
from Database.DatabaseHandler import DatabaseHandler
from Debugging.Debugger import Debugger
from Debugging.LogLevel import LogLevel

import os

db_handler = DatabaseHandler('database-test.sqlite')
if 'database.sqlite' in os.listdir('./'):
    db_handler = DatabaseHandler('database.sqlite')

debugger = Debugger()

## Start the flask API portion of this application
from flask import Flask, Response, request
import json

app = Flask(__name__)

@app.route('/')
def home():
    debugger.log(LogLevel.debug, "")
    return Response(status=403)

@app.route('/get/<codename>/<data>')
def get_by_codename(codename:str, data:str):
    return db_handler.fetch_from_codename(codename, [data])

@app.route('/get/codenames')
def get_all_codenames():
    return db_handler.fetch_codenames()

@app.route('/post/new-codename', methods=['POST'])
def add_endpoint():
    codename = ""
    url = ""
    request_headers = {}
    post_req_json = list(request.form.to_dict(flat=False))[0].replace("'", '"')
    post_req_json = json.loads(post_req_json)
    if 'url' in list(post_req_json):
        url = post_req_json['url']
    if 'codename' in list(post_req_json):
        codename = post_req_json['codename']
    token_name = ''
    for i in list(post_req_json):
        if 'token' in i:
            request_headers = post_req_json[i]
    if len(url) == 0 or len(codename) == 0 or len(list(request_headers)) == 0:
        return {}
    return db_handler.add_codename(codename, url, request_headers)

## SumReel endpoints..
@app.route('/riot/account/by-name/<region>/<name>')
def riot_account_by_name(region:str, name:str):
    return db_handler.fetch_riot_account_by_name(name)

#Regions:
#   NA1 - https://na1.api.riotgames.com
#   EUW - https://euw1.api.riotgames.com

@app.route('/riot/account/by-accountId/<region>/<account_id>')
def riot_account_by_id(region:str, account_id:str):
    return db_handler.fetch_riot_account_by_id(region, account_id)

@app.route('/riot/matches/by-id/<region>/<id>')
def riot_get_match_by_id(region:str, id:str):
    return db_handler.fetch_match_by_id(region, id)

@app.route('/riot/matchlist/by-account/<region>/<account_id>')
def riot_get_matchlist_by_account_id(region:str, account_id:str):
    return db_handler.fetch_matchlist_by_account_id(region, account_id)


#This is a bit silly, but I need the IP address of the local device that's a cross-platform solution. I also need to focus on one specific network use-case.
import subprocess
import os
import socket

if __name__ == "__main__":
    developer_only_mode = False
    port = 20090

    #context = ('austinbennett.dev.crt', 'austinbennett.dev.pem')
    context = None

    if developer_only_mode:
        app.run(host='127.0.0.1', port=port, ssl_context=context)
    elif 'nt' in os.name:
        sp = str(subprocess.run('ipconfig', capture_output=True).stdout)[2:-1].replace('\\r', '').replace('\\n', '\n').replace('\n\n\n', '\n').replace('\n\n', '\n')
        ip_addr = sp[sp.index('IPv4 Address'):sp.index('Subnet')].split(': ')[1].split('\n')[0]
        app.run(host=ip_addr, port=port, ssl_context=context)
    else:
        ip_addr = socket.gethostbyname(socket.gethostname())
        app.run(host=ip_addr, port=port,ssl_context=context)
