# like-counter.py
# Counts how many times each user id has liked a message.

import csv
import json
import sys

def count_likes(file_path):
    user_counts = {}

    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            likes = row['favorited_by'][1:-1].split(' ')

            if likes == ['']:
              continue

            likes = [user_id.replace("'", '') for user_id in likes]

            for user_id in likes:
                if user_id in user_counts:
                    user_counts[user_id] += 1
                else:
                    user_counts[user_id] = 1

    return user_counts

if __name__ == '__main__':
  with open(sys.argv[2], 'w') as f:
    user_counts = count_likes(sys.argv[1])
    f.writelines([f'{k},{v}\n' for k, v in user_counts.items()])

