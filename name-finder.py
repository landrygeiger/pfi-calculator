# name-finder.py
# Finds the first used name for each user id in a csv of messages and saves
# these associations to a csv.

import csv
import sys

def create_user_dict(file_name):
    user_dict = {}
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_dict[row['user_id']] = row['name']
    return user_dict

def write_to_csv(file_name, user_dict):
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        for user_id, name in user_dict.items():
            writer.writerow([user_id, name])

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    user_dict = create_user_dict(input_file)
    write_to_csv(output_file, user_dict)