import random
from flask import Flask, render_template, request, redirect, url_for
from Cricket_logic import start_match, enter_players, toss_winner, update_batters, update_bowler, mark_out, get_match_data, match_data

# Initialize the Flask app
app = Flask(__name__, template_folder='../frontend/templates')



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


@app.route('/toss', methods=['GET', 'POST'])
def toss():
    if request.method == 'POST':
        # Perform toss logic and render toss result
        team1 = match_data['team1']
        team2 = match_data['team2']
        toss_result = random.choice([team1, team2])
        winner = toss_result
        return render_template('toss.html', match_data=match_data, toss_result=toss_result, winner=winner)
    return render_template('toss.html', match_data=match_data)

@app.route('/team_players')
def team_players():
    return render_template('team_players.html', match_data=match_data)

@app.route('/match_play', methods=['GET', 'POST'])
def match_play():
    # Your function code
    return render_template('match_play.html')

if __name__ == '__main__':
    app.run(debug=True)