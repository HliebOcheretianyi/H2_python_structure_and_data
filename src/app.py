from flask import Flask, request, jsonify, render_template
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
    return render_template('forecast_dashboard.html')


@app.route('/api/regions')
def regions_api():
    time = pd.to_datetime(datetime.now()).floor('h').strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = os.path.join(os.getcwd(), r'predict_data/forecast')
    file_path = os.path.join(data_dir, f"forecast_{time}.json")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    regions = list(data.get("regions_forecast", {}).keys())
    regions.insert(0, "All regions")
    return jsonify(regions)


@app.route('/api/forecast', methods=['POST'])
def forecast_api():
    data = request.get_json()
    region = data.get('region')
    time = pd.to_datetime(datetime.now()).floor('h').strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = os.path.join(os.getcwd(), r'predict_data/forecast')
    file_path = os.path.join(data_dir, f"forecast_{time}.json")

    with open(file_path, 'r', encoding='utf-8') as f:
        forecast_data = json.load(f)

    forecasts = forecast_data.get("regions_forecast", {})

    if region == "All regions":
        return jsonify(forecasts)
    elif region in forecasts:
        return jsonify({region: forecasts[region]})



if __name__ == '__main__':
    app.run(debug=True)