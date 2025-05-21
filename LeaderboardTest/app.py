from flask import Flask
import json
from leaderboard_logic import load_scores_data, process_users_for_leaderboard

app = Flask(__name__)

@app.route("/")
def show_processed_leaderboard_data():
    all_raw_scores_data = load_scores_data()
    processed_user_list = process_users_for_leaderboard(all_raw_scores_data)

    data_to_display = "<h1>User scores</h1>"
    if processed_user_list:
        data_to_display += "<ul>"
        for user_data_item in processed_user_list:
            name = user_data_item.get('name')
            score = user_data_item.get('leaderboard_score')
            data_to_display += f"<li>{name}: {score}</li>" # Add each user as a list item
        data_to_display += "</ul>"
    #data_to_display = json.dumps(processed_user_list)
    return data_to_display

if __name__ == "__main__":
    app.run(debug=True)