from __future__ import annotations
from pathlib import Path
import json
import logging

# The leaderboard is calculated using the following rules:
# ● Users are ranked by the sum of their best submission scores
# ● For each user, only scores from their best 24 submissions count
# ● A user must have at least 3 submissions to appear in the rankings

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

MIN_SUBMISSIONS_TO_QUALIFY = 3
MAX_SUBMISSIONS_TO_SCORE = 24
SCORES_FILE_PATH = Path(__file__).parent / "data" / "scores.json"

def load_scores_data(path_to_file: str = SCORES_FILE_PATH) -> list | None:
    """Attempts to load the scores data from the specified JSON file"""
    try:
        with open(path_to_file, "r") as f:
            all_data = json.load(f)
        # print(all_data)
        return all_data
    except FileNotFoundError:
        logging.error(f"File cannot be found at {path_to_file}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"JSON data is broken or malformed: {e}")
        return None
    except Exception as e:
        logging.error(f"Some unexpected error occured while attempting to load data from {path_to_file}")
        return None

def _is_user_eligible(number_of_submissions: int) -> bool:
    """Checks if the user meets the minimum required number of submissions criteria"""
    return number_of_submissions >= MIN_SUBMISSIONS_TO_QUALIFY

def _calculate_user_score(user_submissions_list: list, user_name: str) -> int:
    """
    Calculates the total leaderboard score for a single user based on their submissions.
    Only considers the top MAX_SUBMISSIONS_TO_SCORE submissions.
    """
    valid_scores_for_this_user = []
    for user_submission_dictionary in user_submissions_list:
        current_score = user_submission_dictionary.get("score")
        if current_score is not None:
            if isinstance(current_score, (int, float)):
                valid_scores_for_this_user.append(int(current_score))
            else:
                logging.info(f"{user_name} has a submission with a non-numeric score: '{current_score}', skipping this score.")
        else:
            logging.warning(f"{user_name} has a submission with no score (score is None)")

    # logging.debug(f"All collected scores for {user_name} BEFORE sorting: {valid_scores_for_this_user}")

    valid_scores_for_this_user.sort(reverse=True)
    # logging.info(f"Individual submission score list for {user_name} (sorted): {valid_scores_for_this_user}")
    top_scores_for_user = valid_scores_for_this_user[:MAX_SUBMISSIONS_TO_SCORE]
    # logging.debug(f"Top {len(top_scores_for_user)} eligible scores for {user_name}: {top_scores_for_user}")
    total_leaderboard_score = sum(top_scores_for_user)
    # logging.info(f"User: {user_name}, Calculated Total Score for leaderboard: {total_leaderboard_score}")
    return total_leaderboard_score
            
def process_final_users_for_leaderboard(all_users_data: list) -> list:
    """Processes all user data to generate a ranked leaderboard"""
    final_processed_users_for_ranking = []
    # ineligible_users = []

    if not all_users_data:
        return []
    
    for user_entry in all_users_data:
        user_name = user_entry.get("name", "Unknown user")
        user_submissions_list = user_entry.get("submissions", [])
        number_of_submissions = len(user_submissions_list)

        if _is_user_eligible(number_of_submissions):
            total_leaderboard_score = _calculate_user_score(user_submissions_list, user_name)
            final_processed_users_for_ranking.append({"name": user_name, "leaderboard_score": total_leaderboard_score})
        else:
            logging.info(f"User {user_name} isn't eligible: (Submissions < {MIN_SUBMISSIONS_TO_QUALIFY})")
            
    if final_processed_users_for_ranking:
        final_processed_users_for_ranking.sort(key= lambda x: x['leaderboard_score'], reverse=True)
        
        current_rank = 0
        last_score = float('-inf') 
        for user_data_dictionary in final_processed_users_for_ranking:
            if user_data_dictionary['leaderboard_score'] != last_score:
                current_rank += 1
            user_data_dictionary['display_rank'] = current_rank
            last_score = user_data_dictionary['leaderboard_score']
            
            # assign styles (ranks) based on display_rank (top 3)
            user_data_dictionary['style_class'] = ''
            if current_rank == 1:
                user_data_dictionary['style_class'] = 'rank-gold'
            elif current_rank == 2:
                user_data_dictionary['style_class'] = 'rank-silver'
            elif current_rank == 3:
                user_data_dictionary['style_class'] = 'rank-bronze'
        
        logging.info("Sorted final rankings after processing (with ranks and styles applied):")
        for user_data_dictionary in final_processed_users_for_ranking:
            logging.info(
                f"Rank: {user_data_dictionary.get('display_rank', 'N/A')}, "
                f"Name: {user_data_dictionary['name']}, "
                f"Score: {user_data_dictionary['leaderboard_score']}, "
                f"Class: {user_data_dictionary.get('style_class', '')}"
            )
    else:
        logging.warning("No eligible users found after processing")                  
            
    return final_processed_users_for_ranking

if __name__ == "__main__":
    data = load_scores_data()
    if data is not None:
        process_final_users_for_leaderboard(data)
    else:
        logging.error("Can't load data")