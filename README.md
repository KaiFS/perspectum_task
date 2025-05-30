# Online leaderboard technical test submission

## Core task requirements
- **Load, process and store data:** Loads the user scores from 'data/scores.json', processes them according to the technical doc rules, and stores ranked leaderboard (currently in memory) for display
- **Leaderboard calculation:**
    - Users are ranked by the sum of their best submission scores
    - Only the top 24 scores for each user are used
    - Users need >=3 submissions to appear in the rankings
    - Ties in score result in shared ranks currently (e.g 1st, 2nd, 2nd, 3rd)
- **Leaderboard/web display:** Flask wep app displays the top leaderboard users on a webpage

## Structure
LeaderboardTest/
|- app.py                   # main flask application
|- leaderboard_logic.py     # core logic for loading processing and ranking user data
|- requirements.txt         # depedencies 
|- README.md                # what you're reading now
|- data/
|-- scores.json             # the provided scores.json
|- static/
|-- style.css               # some very basic CSS for the leaderboard page
|- templates/
|-- leaderboard.html        # the HTML template for the leaderboard

## Setup and how to run

1. **Prerequisites**
- python 3.10+
- pip

2. **Create and activate venv**
- python3 -m venv venv
- source venv/bin/activate

3. **Install dependencies**
- cd LeaderboardTest
- pip install -r requirements.txt

4. **Run the app**
- python3 app.py


## Design choices and reasoning for them

- **Why Flask?**
I've used it previously for my dissertation project, I've used it as part of my current role, it's simple, does what I need it to do, is lightweight and allows for quick/easy development

- **Data handling**
scores.json is loaded into memory when the Flask app runs, that works for this task, because I don't expect the data set to change, for a production system, I believe some kind of database
would be much more suitable

- **Ranking ties?**
Adding because it took not an inconsequential amount of time trying to figure out how I should deal with ties (once I realised there would be), I went with simply giving the users with the same score the same rank.
Obviously on an actual leaderboard, this feels like a cop out, I could have used standard competition ranking maybe (1, 2, 2, 4), or use a secondary key like submission data?

- **Handling errors**
There's basic error handling implemented for loading files, and invalid/missing scores in user submissions.
- 
In a production environment, I wouldn't expect a perfectly formed JSON, from searching google I should probably implement some kind of JSON schema?, beyond the scope of my current experience/submission I think

## Potential improvements/potential future considerations
- Database integration? 
- Some kind of mechanism to update scores without restarting the app?
- Better/more robust error handling
- If deployed to prod, some kind of config management for settings like file path, min/max submissions etc (e.g, config file, using envionment variables etc etc)
- Unit tests
- Dockerisation?

## Time management and time spent
I've come back to the project as and when I have time between being ill <> work, I think at point of finalising this read-me I'm realising I'm probably just changing things to change things at this point,
and I should instead just submit a final submission, and talk through anything else I was considering during the interview.