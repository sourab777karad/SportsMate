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

@app.route('/enter_players', methods=['POST'])
def enter_players():
    # Dynamically add players based on total players per team
    team1_players = [request.form.get(f'team1_player{i}') for i in range(1, match_data["total_players"] + 1)]
    team2_players = [request.form.get(f'team2_player{i}') for i in range(1, match_data["total_players"] + 1)]
    
    match_data["team1_players"] = team1_players
    match_data["team2_players"] = team2_players
    
    # Initialize batters (first 2 players from each team)
    match_data["current_batters"] = [team1_players[0], team2_players[0]]
    
    return render_template('match_play.html', match_data=match_data)

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

if __name__ == '__main__':
    app.run(debug=True)