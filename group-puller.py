# group-puller.py
# Finds the id's of all the user's groups and saves them into a csv.

import requests
import dotenv
import os

OUTPUT_FILE = './data/groups.txt'

dotenv.load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = os.getenv('GROUP_ID') 

URL = f'https://api.groupme.com/v3/groups?token={ACCESS_TOKEN}'

if __name__ == '__main__':
  res = requests.get(URL)
  res_obj = res.json()['response']
  
  with open(OUTPUT_FILE, 'w') as f:
    for group in res_obj:
      f.write(group['name'] + ': ' + group['group_id'] + '\n')