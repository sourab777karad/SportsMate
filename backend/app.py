from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__, template_folder='frontend/templates')

# Define a route
@app.route('/')
def home():
    return render_template('index.html')

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    
