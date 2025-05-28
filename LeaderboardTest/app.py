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

@app.route("/")
def show_data():
    return render_template(
        "leaderboard.html", users_to_display=PROCESSED_LEADERBOARD_DATA
    )

if __name__ == "__main__":
    app.run(debug=True)
