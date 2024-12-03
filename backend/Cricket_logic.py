# cricket_logic.py


# Global match data structure
match_data = {
    "team1": "",
    "team2": "",
    "overs": 0,
    "total_players": 0,
    "team1_players": [],
    "team2_players": [],
    "current_batters": [],
    "out_batters": [],
    "current_bowler": ""
}

# Function to start a match
def start_match(team1, team2, overs, total_players):
    """Initialize the match data."""
    match_data["team1"] = team1
    match_data["team2"] = team2
    match_data["overs"] = overs
    match_data["total_players"] = total_players

# Function to enter players' names for both teams
def enter_players(team1_players, team2_players):
    """Enter the player names for both teams."""
    match_data["players_team1"] = team1_players
    match_data["players_team2"] = team2_players

# Function to record the toss winner
def toss_winner(winner_team):
    """Set the toss winner and who will bat first."""
    match_data["toss_winner"] = winner_team

# Function to set the current batters
def update_batters(batter1, batter2):
    """Set the current batters."""
    match_data["current_batters"] = [{"name": batter1, "runs": 0}, {"name": batter2, "runs": 0}]

# Function to update the current bowler
def update_bowler(bowler_name):
    """Set the current bowler."""
    match_data["bowler"] = bowler_name

# Function to mark a batter out and replace with a new batter
def mark_out(batter_name, new_batter_name):
    """Mark a batter out and replace with a new batter."""
    for batter in match_data["current_batters"]:
        if batter["name"] == batter_name:
            match_data["out_batters"].append(batter)
            match_data["current_batters"].remove(batter)
            break
    match_data["current_batters"].append({"name": new_batter_name, "runs": 0})

# Function to get the current match data
def get_match_data():
    """Return the current match data."""
    return match_data
