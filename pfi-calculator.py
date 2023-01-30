import csv
import sys
import dotenv
import os
from scraper import scrape
import statistics

A = 2
B = 1
C = 1

MINIMUM_MESSAGES_SENT = 10

def pfi_func(individual_user_stats):
  avg, stdev, highest = individual_user_stats
  return (avg ** A) * (highest ** C) / (stdev ** B) / 10 * 0.5

def catalog_like_counts_on_user_msgs(messages_file): 
  msg_like_counts = {}

  with open(messages_file, 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
      user_id = row['user_id']
      likes = int(row['likes'])

      if user_id in msg_like_counts:
        msg_like_counts[user_id].append(likes)
      else:
        msg_like_counts[user_id] = [likes]
  
  return msg_like_counts

def count_user_msgs_and_get_names(messages_file):
  user_msg_counts = {}
  user_names = {}

  with open(messages_file, 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
      user_id = row['user_id']
      user_msg_counts[user_id] = user_msg_counts.get(user_id, 0) + 1
      user_names[user_id] = row['name']

  return user_msg_counts, user_names

def filter_low_msg_counts(like_dict, user_msg_counts):
  return {k: like_dict[k] for k in like_dict if user_msg_counts[k] >= MINIMUM_MESSAGES_SENT}

def calc_user_stats(like_counts_on_user_msgs):
  user_stats = {}

  for user_id, like_counts in like_counts_on_user_msgs.items():
    avg = statistics.mean(like_counts)
    stdev = statistics.stdev(like_counts)
    best = max(like_counts)

    user_stats[user_id] = (avg, stdev, best) 

  return user_stats

def calc_pfi(user_stats_dict):
  pfi_dict = {}

  for user_id, stats in user_stats_dict.items():
    pfi_dict[user_id] = pfi_func(stats)

  return pfi_dict

def write_pfi_results_to_file(output_file, pfi_dict, stats_dict, names_dict):
  with open(output_file, 'w') as f:
    f.write('user_id,avg_likes,stdev_likes,max_likes,pfi,name\n')
    writer = csv.writer(f)
    sorted_pfi_dict = sorted(pfi_dict.items(), key=lambda x: x[1], reverse=True)

    rows = [(user_id, stats_dict[user_id][0], stats_dict[user_id][1], stats_dict[user_id][2], pfi, names_dict[user_id]) for user_id, pfi in sorted_pfi_dict]

    writer.writerows(rows)

if __name__ == '__main__':
  dotenv.load_dotenv()

  access_token = os.getenv('ACCESS_TOKEN')
  group_id = sys.argv[1]

  output_file = sys.argv[2]
  input_file = sys.argv[3] if len(sys.argv) >= 4 else None

  if input_file == None:
    input_file = './scraped_messages.csv'
    scrape(input_file, access_token, group_id)

  # Create lists of everyone's like counts + num msgs sent
  like_counts_on_user_msgs = catalog_like_counts_on_user_msgs(input_file)
  user_msg_counts, user_names = count_user_msgs_and_get_names(input_file)

  like_counts_on_user_msgs = filter_low_msg_counts(like_counts_on_user_msgs, user_msg_counts)
  # Find avg, stdev, max of each like count
  user_stats_dict = calc_user_stats(like_counts_on_user_msgs)
  # Calculate PFI for each individual and save to csv
  pfi_dict = calc_pfi(user_stats_dict)

  write_pfi_results_to_file(output_file, pfi_dict, user_stats_dict, user_names)