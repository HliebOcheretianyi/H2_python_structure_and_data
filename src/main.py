from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import datetime
import logging
import dotenv
from src import weather_scrap
from src.alerts_in_ua import get_alert_status

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.weather_info = None
app.weather_location = None
app.alerts_info = None
app.alerts_location = None


@app.route('/')
def home_page():
    return render_template('index.html',
                           weather_info=app.weather_info,
                           weather_location=app.weather_location,
                           alerts_info=app.alerts_info,
                           alerts_location=app.alerts_location)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    try:
        if request.method == 'POST':
            json_data = request.get_json() or {}
            location = json_data.get("location")
        else:
            location = request.args.get("location")

        if not location:
            return jsonify({"error": "location is required"}), 400

        weather_info = weather_scrap.generate_forecast(location, str(datetime.date.today()))

        app.weather_info = weather_info
        app.weather_location = location

        result = {
            "location": location,
            "weather": weather_info,
        }

        return jsonify(result)
    except Exception as e:
        logger.error(f"Weather error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    try:
        if request.method == 'POST':
            json_data = request.get_json() or {}
            location = json_data.get("location")
        else:
            location = request.args.get("location")

        if not location:
            return jsonify({"error": "location is required"}), 400

        status = get_alert_status(location)

        app.alerts_info = status
        app.alerts_location = location

        return jsonify({"location": location, "status": status})
    except Exception as e:
        logger.error(f"Alerts error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":

    app.run()