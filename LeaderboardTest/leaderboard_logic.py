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


def process_final_users_for_leaderboard(all_users_data):
    final_processed_users_for_ranking = []
    # ineligible_users = []

    for user_entry in all_users_data:
        user_name = user_entry.get("name", "Unknown user")
        user_submissions_list = user_entry.get("submissions", [])
        number_of_submissions = len(user_submissions_list)

        # CONDITION 1: We begin processing by first checking that the user has more than the minimum amount of submissions required to appear in the rankings
        if number_of_submissions >= MIN_SUBMISSIONS:
            logging.info(
                f"{user_name} has {number_of_submissions} submissions, and is eligible so far"
            )

            all_scores_for_this_user = []

            for user_submission_dictionary in user_submissions_list:
                current_score = user_submission_dictionary.get("score")

                if current_score is not None:  # TODO
                    all_scores_for_this_user.append(current_score)
                else:
                    logging.info(f"{user_name} has a submission with no score")

                # TODO - I think this is the point where I should sort the users submissions scores, order them, and then remove the lowest

            # print(f"    All collected scores for {user_name} BEFORE sorting: {all_scores_for_this_user}")

            all_scores_for_this_user.sort(reverse=True)
            logging.info(
                f"    Individual submission score list for {user_name}: {all_scores_for_this_user}"
            )

            # CONDITION 2: We need to check that only the users best 24 submissions count
            top_scores_for_user = all_scores_for_this_user[:MAX_SCORES]
            print(
                f"    Top eligible total scores for {user_name}: {top_scores_for_user}"
            )
            logging.info(
                f"{user_name} has {len(top_scores_for_user)} total submissions eligible"
            )

            # CONDITION 3.1: Sum the users best scores so we can sort them later
            total_leaderboard_score = sum(top_scores_for_user)
            logging.info(f"User: {user_name}, Total Score: {total_leaderboard_score}")

            final_processed_users_for_ranking.append(
                {"name": user_name, "leaderboard_score": total_leaderboard_score}
            )
        else:
            logging.info(
                f"User {user_name} isn't eligible: (Submissions < {MIN_SUBMISSIONS})"
            )

    if final_processed_users_for_ranking:
        for user_data_dict in final_processed_users_for_ranking:
            # Condition 3.2: Sort the list of processed users by their total leaderboard_score that we calculated earlier
            final_processed_users_for_ranking.sort(
                key=lambda x: x["leaderboard_score"], reverse=True
            )
            print(
                f"  Name: {user_data_dict['name']}, Score: {user_data_dict['leaderboard_score']}"
            )
    else:
        logging.warning("  No users eligible for ranking.")

    return final_processed_users_for_ranking


if __name__ == "__main__":
    data = load_scores_data()
    if data is not None:
        process_final_users_for_leaderboard(data)
    else:
        logging.error("Can't load data")
