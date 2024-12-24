import random
from flask import Flask, render_template, request, redirect, url_for, session
from Cricket_logic import start_match, enter_players, toss_winner, update_batters, update_bowler, mark_out, get_match_data, match_data


# Initialize the Flask app
app = Flask(__name__, template_folder='../frontend/templates')

app.secret_key = 'b8c9f4e5a6d7e8f9c0b1a2d3e4f5g6h7'
# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cricket', methods=['GET', 'POST'])
def cricket():
    if request.method == 'POST':
        # Fetch form data for teams, overs, total players
        match_data["team1"] = request.form.get('team1')
        match_data["team2"] = request.form.get('team2')
        match_data["overs"] = int(request.form.get('overs'))
        match_data["total_players"] = int(request.form.get('total_players'))
        
        return render_template('enter_players.html', match_data=match_data)
    return render_template('cricket.html')

@app.route('/enter_players', methods=['GET', 'POST'])
def enter_players():
    if request.method == 'POST':
        total_players = match_data.get('total_players', 0)

        # Collect team player names from the form dynamically
        for i in range(1, total_players + 1):
            match_data[f"team1_player{i}"] = request.form.get(f"team1_player{i}", f"Player {i}")
            match_data[f"team2_player{i}"] = request.form.get(f"team2_player{i}", f"Player {i}")

        # Redirect to another route or render a confirmation page
        return render_template('team_players.html', match_data=match_data)

    return render_template('enter_players.html', match_data=match_data)

@app.route('/mark_out', methods=['POST'])
def mark_out():
    batter_to_remove = request.form.get('out_batter')
    
    # Move the batter to the out list and remove from current batters
    match_data["out_batters"].append(batter_to_remove)
    match_data["current_batters"] = [batter for batter in match_data["current_batters"] if batter != batter_to_remove]
    
    return render_template('match_play.html', match_data=match_data)

@app.route('/add_batter', methods=['POST'])
def add_batter():
    new_batter = request.form['new_batter']
    match_data["current_batters"].append(new_batter)
    return render_template('match_play.html', match_data=match_data)

@app.route('/update_bowler', methods=['POST'])
def update_bowler():
    match_data["bowler"] = request.form['bowler_name']
    return render_template('match_play.html', match_data=match_data)

@app.route('/submit_players', methods=['POST'])
def submit_players():
    # Fetching player names for Team 1
    match_data["team1_players"] = [
        request.form.get(f'team1_player{i}') for i in range(1, match_data["total_players"] + 1)
    ]
    # Fetching player names for Team 2
    match_data["team2_players"] = [
        request.form.get(f'team2_player{i}') for i in range(1, match_data["total_players"] + 1)
    ]

    # Handle cases where fields might be left empty
    match_data["team1_players"] = [p for p in match_data["team1_players"] if p]
    match_data["team2_players"] = [p for p in match_data["team2_players"] if p]

    # Validate the input
    if len(match_data["team1_players"]) != match_data["total_players"] or len(match_data["team2_players"]) != match_data["total_players"]:
        return "Error: Please ensure all player names are filled.", 400

    # Proceed to toss page
    return render_template('toss.html', match_data=match_data)

@app.route('/start_toss', methods=['POST'])
def start_toss():
    toss_winner = request.form['toss_winner']
    toss_decision = request.form['toss_decision']
    
    # Store toss information
    match_data["toss_winner"] = toss_winner
    match_data["toss_decision"] = toss_decision

    # Redirect to match play page
    return render_template('match_play.html', match_data=match_data)

@app.route('/setup_match', methods=['POST'])
def setup_match():
    # Get team names and total players from the form
    team1 = request.form.get('team1', '').strip()  # Get and clean input
    team2 = request.form.get('team2', '').strip()
    total_players = int(request.form.get('total_players', 0))

    # Validate input
    if not team1 or not team2:
        return "Error: Team names cannot be empty.", 400

    # Store in the session
    session['match_data'] = {
        'team1': team1,
        'team2': team2,
        'total_players': total_players,
        'winner': ''
    }

    print("DEBUG: match_data stored in session:", session['match_data'])  # Debugging

    # Redirect to the toss page
    return redirect(url_for('toss'))

@app.route('/toss', methods=['GET', 'POST'])
def toss():
    # Ensure match_data exists in the session
    if 'match_data' not in session:
        return "Error: Match data not found. Please set up the match first.", 400

    match_data = session['match_data']

    if request.method == 'POST':
        # Perform the toss
        match_data['winner'] = random.choice([match_data['team1'], match_data['team2']])
        session['match_data'] = match_data  # Update session with the winner

        print("DEBUG: Winner:", match_data['winner'])  # Debugging

        return render_template('toss.html', match_data=match_data)

    # Render the toss page with the current match data
    return render_template('toss.html', match_data=match_data)

@app.route('/start_match', methods=['GET', 'POST'])
def start_match():
    if 'match_data' not in session:
        return redirect(url_for('cricket'))  # Redirect if match data is missing

    match_data = session['match_data']

    if request.method == 'POST':
        # Get selected batters and bowler from the form
        batter1 = request.form.get('batter1')
        batter2 = request.form.get('batter2')
        bowler = request.form.get('bowler')

        # Validate inputs
        if not batter1 or not batter2 or not bowler:
            return "Error: Please select two batters and one bowler.", 400
        if batter1 == batter2 or batter1 == bowler or batter2 == bowler:
            return "Error: Players must be unique.", 400

        # Update match data
        match_data['current_batters'] = [batter1, batter2]
        match_data['current_bowler'] = bowler
        match_data['strike_batter'] = batter1  # Batter facing the first delivery
        session['match_data'] = match_data

        # Redirect to the main match interface
        return redirect(url_for('match_play'))

    # Determine batting and bowling teams
    batting_team = match_data['team1'] if match_data['toss_decision'] == 'bat' else match_data['team2']
    bowling_team = match_data['team2'] if batting_team == match_data['team1'] else match_data['team1']

    # Debugging: Check the players
    batting_players = match_data['team1_players'] if batting_team == match_data['team1'] else match_data['team2_players']
    bowling_players = match_data['team2_players'] if bowling_team == match_data['team2'] else match_data['team1_players']
    print("DEBUG: Batting Players:", batting_players)
    print("DEBUG: Bowling Players:", bowling_players)

    return render_template('select_players.html', match_data=match_data, batting_players=batting_players, bowling_players=bowling_players)

@app.route('/team_players')
def team_players():
    return render_template('team_players.html', match_data=match_data)

@app.route('/match_play', methods=['GET', 'POST'])
def match_play():
    if 'match_data' not in session:
        return "Error: Match data is missing!", 400

    match_data = session['match_data']

    # Initialize current batters and out batters if not set
    if 'current_batters' not in match_data:
        match_data['current_batters'] = []  # Current batters
        match_data['out_batters'] = []  # Players who are out

    # If players haven't been stored in the session, this could be the issue
    if 'team1_players' not in match_data or 'team2_players' not in match_data:
        # Add fallback for test purposes, or retrieve it from somewhere else
        match_data['team1_players'] = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5']
        match_data['team2_players'] = ['Player A', 'Player B', 'Player C', 'Player D', 'Player E']

    # Handle POST logic for out and new batters
    if request.method == 'POST':
        dismissed_batter = request.form.get('out_batter')
        new_batter = request.form.get('new_batter')

        if dismissed_batter:
            match_data['current_batters'].remove(dismissed_batter)
            match_data['out_batters'].append(dismissed_batter)

        if new_batter:
            match_data['current_batters'].append(new_batter)

        session['match_data'] = match_data  # Save updates to session

    return render_template('match_play.html', match_data=match_data)

@app.route('/save_toss_decision', methods=['POST'])
def save_toss_decision():
    if 'match_data' not in session:
        return "Error: Match data is missing!", 400

    match_data = session['match_data']
    decision = request.form.get('decision')

    if not decision:
        return "Error: Invalid decision.", 400

    # Save the toss decision
    match_data['toss_decision'] = decision
    session['match_data'] = match_data

    print(f"DEBUG: {match_data['winner']} chose to {decision}.")  # Debugging

    # Redirect to the match play page
    return redirect(url_for('start_match'))

if __name__ == '__main__':
    app.run(debug=True)