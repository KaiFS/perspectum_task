from flask import Flask
import json
from leaderboard_logic import load_scores_data, SCORES_FILE_PATH, process_users_for_leaderboard

app = Flask(__name__)

@app.route("/")
def show_all_data():
    all_scores_data = load_scores_data(SCORES_FILE_PATH)
    display_data = json.dumps(all_scores_data)
    return display_data

if __name__ == "__main__":
    app.run(debug=True)