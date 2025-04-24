from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
    return render_template('forecast_dashboard.html')


@app.route('/api/regions')
def regions_api():
    forecast_path = os.path.join(base_dir, '..', 'data', 'forecasts', 'forecast.json')
    with open(forecast_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    regions = list(data.get("regions_forecast", {}).keys())
    regions.insert(0, "All regions")
    return jsonify(regions)
@app.route('/api/forecast', methods=['POST'])
def forecast_api():
    data = request.get_json()
    region = data.get('region')
    forecast_path = os.path.join(base_dir, '..', 'data', 'forecasts', 'forecast.json')
    with open(forecast_path, 'r', encoding='utf-8') as f:
            forecast_data = json.load(f)

    forecasts = forecast_data.get("regions_forecast", {})

    if region == "All regions":
        return jsonify(forecasts)
    elif region in forecasts:
        return jsonify({region: forecasts[region]})



if __name__ == '__main__':
    app.run(debug=True)