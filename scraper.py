# scraper.py

import requests
import dotenv
import os
import csv

# CHANGE TO DESIRED OUTPUT LOCATION
OUTPUT_FILE = './data/messages.csv'

dotenv.load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = os.getenv('GROUP_ID') 
MESSAGES_PER_REQUEST = 100

GROUP_ME_MESSAGE_ATTRS = ["id", "group_id", "deleted_at", "user_id", "sender_type", "attachments", "pinned_at", "text", "system", "favorited_by", "sender_id", "event", "avatar_url", "pinned_by", "platform", "source_guid", "created_at", "name", "deletion_actor", 'likes']

BASE_URL = f'https://api.groupme.com/v3/groups/{GROUP_ID}/messages?token={ACCESS_TOKEN}&limit={MESSAGES_PER_REQUEST}' 

def json_list_to_csv(json_list, output_dir, do_header):
    with open(output_dir, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=GROUP_ME_MESSAGE_ATTRS)

        if do_header:
          writer.writeheader()

        for json_obj in json_list:
            likes = len(json_obj['favorited_by'])
            json_obj = {k: str(v).replace(",", "").replace("\n", "").replace("\t", "").replace("\r", "") for k, v in json_obj.items() if not k == 'event'}
            json_obj['likes'] = likes
            writer.writerow(json_obj)

def write_next_messages(get_messages_before=0):
  if get_messages_before:
    res = requests.get(BASE_URL + '&before_id=' + get_messages_before)
  else:
    res = requests.get(BASE_URL)
  res_obj = res.json()['response']

  res_messages = res_obj['messages']

  json_list_to_csv(res_messages, OUTPUT_FILE, not bool(get_messages_before))

  return res_messages[-1]['id'], len(res_messages)

if __name__ == '__main__':
  os.remove(OUTPUT_FILE)
  
  last_id, messages_written = write_next_messages()
  i = MESSAGES_PER_REQUEST 
  while messages_written > 0:
    print('Wrote', i, 'messages')
    last_id, messages_written = write_next_messages(last_id)
    i += MESSAGES_PER_REQUEST 

