import requests
import json
import pytest

def test_get_league_summoner_test():
    req = requests.get('https://127.0.0.1:20090/get/league-summoner-by-name-na1/zeuschops', verify=False)
    req_json = json.loads(req.text.replace("'", '"'))
    print("test_get_league_summoner_test(): ", list(req_json))
    assert list(req_json).sort() == ['id', 'accountId', 'puuid', 'name', 'profileIconId', 'revisionDate', 'summonerLevel'].sort() #Sorting as this list may return out of order - thanks JSON

@pytest.mark.filterwarnings("")
def test_get_league_match_test():
    req = requests.get('https://127.0.0.1:20090/get/league-match-by-id-na1/NA1_3874018047', verify=False)
    req_json = json.loads(req.text.replace("'", '"'))
    assert list(req_json).sort() == ['info', 'metadata'].sort() #Sorting as this list may return out of order - thanks JSON
