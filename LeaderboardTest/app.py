from flask import Flask, render_template, jsonify
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

@app.route("/api/leaderboard/top10")
def api_top_10_leaderboard():
    """Add a basic API endpoint for top 10 users"""
    print("Top 10 request")
    all_raw_scores_data = load_scores_data()
    if all_raw_scores_data is None:
        return jsonify({"error": "Could not load scores data"}), 500 # internal server error

    processed_leaderboard_data = process_final_users_for_leaderboard(all_raw_scores_data)

    if not processed_leaderboard_data:
        logging.warning("No eligible users found after processing")
        return jsonify({"users": [], "message": "No eligible users found"}), 200 # OK, but no data

    top_10_users_full_data = processed_leaderboard_data[:10]
    
    # need to exclude html things like style_class for the api response
    api_users_data = []
    for user in top_10_users_full_data:
        api_users_data.append({
            "rank": user.get('display_rank'),
            "name": user.get('name'),
            "score": user.get('leaderboard_score')
        })
    logging.info(f"API top 10: returning {len(api_users_data)}")
    return jsonify(users=api_users_data)

if __name__ == "__main__":
    app.run(debug=True)