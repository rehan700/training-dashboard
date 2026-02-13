#run this always .venv\Scripts\activate
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('MY_API_KEY')
url = 'https://api.football-data.org/v4/matches'
params = {
    'dateFrom': '2026-01-10',
    'dateTo': '2026-01-11'
}
headers = {'X-Auth-Token': API_KEY}
response = requests.get(url, headers=headers, params=params, verify=False)
data=response.json()['matches']
for d in data:
    print(d['homeTeam']['name'], 'vs', d['awayTeam']['name'], 'on', d['utcDate'])
    