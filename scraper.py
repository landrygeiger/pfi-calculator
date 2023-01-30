# scraper.py

import requests
import dotenv
import os
import csv
import sys

MESSAGES_PER_REQUEST = 100
GROUP_ME_MESSAGE_ATTRS = ["id", "group_id", "deleted_at", "user_id", "sender_type", "attachments", "pinned_at", "text", "system", "favorited_by", "sender_id", "event", "avatar_url", "pinned_by", "platform", "source_guid", "created_at", "name", "deletion_actor", 'likes']

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

def get_url(access_token, group_id):
 return f'https://api.groupme.com/v3/groups/{group_id}/messages?token={access_token}&limit={MESSAGES_PER_REQUEST}' 

def write_next_messages(output_file, access_token, group_id, get_messages_before=0):
  base_url = get_url(access_token, group_id)
  if get_messages_before:
    res = requests.get(base_url + '&before_id=' + get_messages_before)
  else:
    res = requests.get(base_url)

  try:
    res_obj = res.json()['response']
  except:
    return 0, 0

  res_messages = res_obj['messages']

  json_list_to_csv(res_messages, output_file, not bool(get_messages_before))

  return res_messages[-1]['id'], len(res_messages)

def scrape(output_file, access_token, group_id):
  if os.path.exists(output_file):
    os.remove(output_file)
  
  last_id, messages_written = write_next_messages(output_file, access_token, group_id)

  i = MESSAGES_PER_REQUEST 
  
  while messages_written > 0:
    if (i % 500 == 0 and i != 0):
      print('Scraped', i, 'messages')

    last_id, messages_written = write_next_messages(output_file, access_token, group_id, get_messages_before=last_id)
    i += MESSAGES_PER_REQUEST 

