from flask import Flask, render_template
from leaderboard_logic import load_scores_data, process_final_users_for_leaderboard
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

app = Flask(__name__)

class DataManager:
    """Manages the dataset for this project"""
    def __init__(self):
        self._leaderboard_data = self._initialise_data() # Load and store on instantiation instead
        
    def _initialise_data(self):
        raw_data = load_scores_data()
        if raw_data:
            processed_data = process_final_users_for_leaderboard(raw_data)
            if not processed_data:
                logging.warning("Leaderboard data was processed, but no eligible users were found")
            else:
                logging.info("Found and loaded the processed leaderboard data successfully")
            return processed_data
        logging.error("Failed to load or process the raw data for leaderboard")
        return []
                
    def get_leaderboard(self):
        return self._leaderboard_data
                
data_manager = DataManager()

@app.route("/")
def display_leaderboard():
    users_to_display = data_manager.get_leaderboard()
    return render_template("leaderboard.html", users_to_display=users_to_display)

if __name__ == "__main__":
    app.run(debug=True)