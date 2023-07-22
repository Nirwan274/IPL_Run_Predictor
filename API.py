from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import joblib
import pandas as pd
from flask_cors import CORS

API = Flask(__name__)
CORS(API)
api = Api(API)

with open('IPL_Joblib', 'rb') as ipl:
    model = joblib.load(ipl)

# Load the original dataset used for training
data = pd.read_csv("IPL.csv", low_memory=False)
columns_to_drop = ['match_id', 'season', 'start_date', 'venue', 'innings', 'batting_team', 'bowling_team',
                   'non_striker', 'other_wicket_type', 'player_dismissed', 'penalty', 'other_player_dismissed',
                   'noballs', 'byes', 'legbyes', 'wides']
data.drop(columns=columns_to_drop, inplace=True)
data.fillna(0, inplace=True)
data['previous_runs'] = data['runs_off_bat'].shift(fill_value=0)
data.drop(columns=['runs_off_bat'], inplace=True)
data = pd.get_dummies(data, columns=['striker', 'bowler', 'wicket_type'])
data = data.iloc[1:]
X = data.drop(columns=['previous_runs'])
X.columns = X.columns.astype(str)  # Convert column names to strings


def runs(X, striker_name, bowler_name, ball):
    input_data = pd.DataFrame([[0] * len(X.columns)], columns=X.columns)
    input_data['striker_' + striker_name] = 1
    input_data['bowler_' + bowler_name] = 1
    input_data['ball'] = str(ball)
    predicted_runs = model.predict(input_data)
    return int(predicted_runs[0])


class getData(Resource):
    def get(self):
        try:
            return data.to_json(orient='records')
        except MemoryError:
            return jsonify(error="Memory Error: The dataset is too large to convert to JSON."), 500


class prediction(Resource):
    def get(self, striker_name, bowler_name, ball):
        predicted_runs = runs(X, striker_name, bowler_name, ball)
        return str(predicted_runs)


api.add_resource(getData, '/api')
api.add_resource(prediction, '/prediction/<string:striker_name>/<string:bowler_name>/<float:ball>')

if __name__ == '__main__':
    API.run(debug=True)

# http://127.0.0.1:5000/prediction/SC%20Ganguly/P%20Kumar/2.1
# http://127.0.0.1:5000/prediction/MS%20Dhoni/P%20Kumar/19.1
