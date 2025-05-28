from __future__ import annotations
import os
import json
import logging

# The leaderboard is calculated using the following rules:
# ● Users are ranked by the sum of their best submission scores
# ● For each user, only scores from their best 24 submissions count
# ● A user must have at least 3 submissions to appear in the rankings

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

MIN_SUBMISSIONS = 3
MAX_SCORES = 24
SCORES_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "scores.json"
)

def load_scores_data(path_to_file=SCORES_FILE_PATH):
    """Attempts to load the provided SCORES.json from the given path"""
    try:
        with open(path_to_file, "r") as f:
            all_data = json.load(f)
        # print(all_data)
        return all_data
    except FileNotFoundError as e:
        logging.error(f"File cannot be found at {path_to_file}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON data is broken or malformed: {e}")
        return None

def _is_user_eligible(number_of_submissions):
    """Checks if the user has the minimum required
    number of submissions"""
    return number_of_submissions >= MIN_SUBMISSIONS

def _calculate_user_score(user_submissions_list: list, user_name: str) -> int:
    """
    Calculates the total leaderboard score for a single user based on their submissions.
    Only considers the top MAX_SCORES submissions.
    """
    all_scores_for_this_user = []
    for user_submission_dictionary in user_submissions_list:
        current_score = user_submission_dictionary.get("score")
        if current_score is not None:
            if isinstance(current_score, (int, float)):
                all_scores_for_this_user.append(int(current_score))
            else:
                logging.info(f"{user_name} has a submission with a non-numeric score: '{current_score}', skipping this score.")
        else:
            logging.info(f"{user_name} has a submission with no score (score is None)")

    # logging.debug(f"All collected scores for {user_name} BEFORE sorting: {all_scores_for_this_user}")

    all_scores_for_this_user.sort(reverse=True)
    # logging.info(f"Individual submission score list for {user_name} (sorted): {all_scores_for_this_user}")

    top_scores_for_user = all_scores_for_this_user[:MAX_SCORES]
    # logging.debug(f"Top {len(top_scores_for_user)} eligible scores for {user_name}: {top_scores_for_user}")
    
    total_leaderboard_score = sum(top_scores_for_user)
    # logging.info(f"User: {user_name}, Calculated Total Score for leaderboard: {total_leaderboard_score}")
    
    return total_leaderboard_score
            
def process_final_users_for_leaderboard(all_users_data):
    final_processed_users_for_ranking = []
    # ineligible_users = []

    for user_entry in all_users_data:
        user_name = user_entry.get("name", "Unknown user")
        user_submissions_list = user_entry.get("submissions", [])
        number_of_submissions = len(user_submissions_list)

        if _is_user_eligible(number_of_submissions):
            total_leaderboard_score = _calculate_user_score(user_submissions_list, user_name)
            final_processed_users_for_ranking.append({"name": user_name, "leaderboard_score": total_leaderboard_score})
        else:
            logging.info(f"User {user_name} isn't eligible: (Submissions < {MIN_SUBMISSIONS})")
            
    if final_processed_users_for_ranking:
        final_processed_users_for_ranking.sort(key= lambda x: x['leaderboard_score'], reverse=True)
        logging.info("Sorted final rankings after processing")
        for user_data_dictionary in final_processed_users_for_ranking:
            logging.info(f"Sorted - Name: {user_data_dictionary['name']}, Score: {user_data_dictionary['leaderboard_score']}")
    else:
        logging.warning("No eligible users found")                    
            
    return final_processed_users_for_ranking
5

if __name__ == "__main__":
    data = load_scores_data()
    if data is not None:
        process_final_users_for_leaderboard(data)
    else:
        logging.error("Can't load data")
