from flask import Flask, render_template
from leaderboard_logic import load_scores_data, process_final_users_for_leaderboard
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")


app = Flask(__name__)

PROCESSED_LEADERBOARD_DATA = []

all_raw_scores_data = load_scores_data()
if all_raw_scores_data is not None:
    PROCESSED_LEADERBOARD_DATA = process_final_users_for_leaderboard(
        all_raw_scores_data
    )
else:
    logging.error("Couldn't load scores data at startup")

# TODO - move things into correct places

# @app.route("/")
# def show_processed_leaderboard_data():
#     all_raw_scores_data = load_scores_data()
#     processed_user_list = process_final_users_for_leaderboard(all_raw_scores_data)

#     data_to_display = "<h1>Leaderboard Rankings</h1>"
#     if processed_user_list:
#         data_to_display += "<ul>"
#         for user_data_item in processed_user_list:
#             name = user_data_item.get('name')
#             score = user_data_item.get('leaderboard_score')
#             data_to_display += f"<li>{name}: {score}</li>" # Add each user as a list item
#         data_to_display += "</ul>"
#     #data_to_display = json.dumps(processed_user_list)
#     return data_to_display


@app.route("/")
def show_data():
    return render_template(
        "leaderboard.html", users_to_display=PROCESSED_LEADERBOARD_DATA
    )


if __name__ == "__main__":
    app.run(debug=True)
