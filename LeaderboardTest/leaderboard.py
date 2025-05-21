from __future__ import annotations
import json


# The leaderboard is calculated using the following rules: 
# ● Users are ranked by the sum of their best submission scores 
# ● For each user, only scores from their best 24 submissions count 
# ● A user must have at least 3 submissions to appear in the rankings 

MIN_SCORES = 3
MAX_SCORES = 24
SCORES_FILE = "scores.json"

def read_data(path_to_file):
    try:
        with open(path_to_file, 'r') as f:
            data = json.load(f)
        #print(data)
        return data
    except FileNotFoundError:
        print(f"File {path_to_file} doesn't exist")

loaded_data = read_data(SCORES_FILE)
if loaded_data:
    print(f"Data loading worked")
    for i, entry in enumerate(loaded_data):
        if i < 3:
            print(f"First three as example {entry}")
        else:
            break
    print(f"Total users loaded: {len(loaded_data)}")
else:
    print("No data")
