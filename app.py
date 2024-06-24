from flask import Flask, render_template, request
import pickle
import pandas as pd
import os

app = Flask(__name__)


# Assuming 'pipe.pkl' is in the 'model' directory relative to app.py
model_file_path = os.path.join(os.path.dirname(__file__), 'model', 'pipe.pkl')

# Load the model
with open(model_file_path, 'rb') as model_file:
    pipe = pickle.load(model_file)
    
# Print the pipeline to debug
print(pipe)

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 
    'Nagpur', 'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 
    'Christchurch', 'Trinidad'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        city = request.form['city']
        current_score = int(request.form['current_score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])
        last_five = int(request.form['last_five'])

        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        current_run_rate = current_score / overs

        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [city], 
             'current_score': [current_score], 'balls_left': [balls_left], 
             'wickets_left': [wickets_left], 'current_run_rate': [current_run_rate], 'last_five': [last_five]}
        )

        print(input_df)  # Print the input dataframe to debug

        result = pipe.predict(input_df)
        prediction = int(result[0])

    return render_template('index.html', teams=sorted(teams), cities=sorted(cities), prediction=prediction)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
