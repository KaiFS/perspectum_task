from flask import Flask, render_template
from leaderboard_logic import load_scores_data, process_final_users_for_leaderboard
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

app = Flask(__name__)

@app.route("/")
def display_leaderboard():
    users_to_display = []
    all_raw_scores_data = load_scores_data()
    if all_raw_scores_data is not None:
        processed_leaderboard_data = process_final_users_for_leaderboard(all_raw_scores_data)
        if not processed_leaderboard_data:
            logging.warning("No eligible users found")
        else:
            logging.info("Leaderboard data found successfully")
            users_to_display = processed_leaderboard_data
    else:
        logging.error("Failed to load raw scores data, leaderboard will be empty")
    return render_template("leaderboard.html", users_to_display=users_to_display)

if __name__ == "__main__":
    app.run(debug=True)