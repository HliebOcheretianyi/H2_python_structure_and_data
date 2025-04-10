from flask import Flask, request, jsonify, render_template
from src import weather_scrap
import datetime
from dotenv import load_dotenv

from src.alerts_in_ua import get_alert_status\

load_dotenv()

app = Flask(__name__)

app.weather_info = None
app.alerts_info = None

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    json_data = request.get_json()

    location = json_data.get("location")


    if not location:
        raise "location is required: status_code=400"

    weather_info = weather_scrap.generate_forecast(location, str(datetime.date.today()))

    result = {
        "location": location,
        "weather": weather_info,
    }

    app.weather_info = result

    return jsonify(result)

@app.route('/alerts', methods = ['POST', 'GET'])
def alerts():
    alert_data = request.get_json()

    location = alert_data.get("location")

    if not location:
        raise "location is required status_code: 400"


    status = get_alert_status(location)

    app.alerts_info = status

    return jsonify(status)




