from __future__ import annotations
import os
import json

# The leaderboard is calculated using the following rules: 
# ● Users are ranked by the sum of their best submission scores 
# ● For each user, only scores from their best 24 submissions count 
# ● A user must have at least 3 submissions to appear in the rankings 

MIN_SCORES = 3
MAX_SCORES = 24
SCORES_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "scores.json")

def load_scores_data(path_to_file = SCORES_FILE_PATH):
    """Loads and returns data from scores.json"""
    try:
        with open(path_to_file, 'r') as f:
            all_data = json.load(f)
        #print(all_data)
        return all_data
    except FileNotFoundError:
        print(f"File {path_to_file} doesn't exist")
        return None

def process_users_for_leaderboard(all_users_data: list):
    """Process users, submissions, scores, etc"""
    final_processed_users_for_ranking = []
    # ineligible_users = [] 

    for user_entry in all_users_data:
        user_name = user_entry.get("name")
        user_submissions_list = user_entry.get('submissions')
        number_of_submissions = len(user_submissions_list)
        print(f"Users: {user_name}")
        print(f"Submission list: {user_submissions_list}")
        print(f"Number of submissions: {number_of_submissions}")
    
        # if number_of_submissions >= MIN_SCORES:
        #     print(f"{user_name} has {number_of_submissions} submissions, and is eligible so far")
        # else:
        #     print(f"{user_name} ")

        all_scores_for_this_user = [] # all user total scores

        for user_submission_dictionary in user_submissions_list: # for each users submissions
            current_score = user_submission_dictionary.get('score') # get their score
            if current_score is not None: # basic sanity check
                all_scores_for_this_user.append(current_score) # add their score to calculate their score total
            else:
                print(f"{user_name} has a submission with no score")

            # TODO - I think this is the point where I should sort the users submissions scores, order them, and then remove the lowest

            print(f"    All current submission scores for {user_name}: {all_scores_for_this_user}")

        total_user_scores = sum(all_scores_for_this_user)
        print(user_name, total_user_scores)


    if final_processed_users_for_ranking:
        for name in final_processed_users_for_ranking:
            print(name)
    else:
        return None 
    

data = load_scores_data()
process_users_for_leaderboard(data)