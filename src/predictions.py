import os
import pandas as pd
import numpy as np
import pickle
import joblib
import json
from datetime import datetime
from src.model_building import Stacking, CoolStacking

def load_models():
    scaler = joblib.load('../src/our_models/scaler_v1.pkl')
    with open('../src/our_models/3__MUSE__v1.pkl', 'rb') as f:
        model = pickle.load(f)
    return scaler, model

def load_data():
    data_dir = os.path.join(os.getcwd(), 'predict_data/everyhour_predict')
    test_file = os.path.join(data_dir, 'test.csv')
    return pd.read_csv(test_file, sep=";")

def generate_forecast(df, scaler, model):
    region_map = {
        1: "Kyiv", 2: "Vinnytsia", 3: "Lutsk", 4: "Dnipro", 5: "Donetsk",
        6: "Zhytomyr", 7: "Uzhgorod", 8: "Zaporozhye", 9: "Ivano-Frankivsk",
        10: "Kyiv region", 11: "Kropyvnytskyi", 13: "Lviv", 14: "Mykolaiv",
        15: "Odesa", 16: "Poltava", 17: "Rivne", 18: "Sumy", 19: "Ternopil",
        20: "Kharkiv", 21: "Kherson", 22: "Khmelnytskyi", 23: "Cherkasy",
        24: "Chernivtsi", 25: "Chernihiv"
    }
    hour = int(pd.to_datetime(datetime.now()).floor('h').strftime("%H"))
    hours = [f"{((hour + h)%24):02d}:00" for h in range(24)]
    regions_forecast = {}

    for region_id, region_name in region_map.items():
        X_new = df[df['region_id'] == region_id]
        if X_new.empty:
            continue

        X_all = X_new.drop("status", axis=1)
        X_all_scaled = scaler.transform(X_all)
        y_pred_all = model.predict(X_all_scaled)

        forecast = {
            hour: True if status == 1 else False
            for hour, status in zip(hours, y_pred_all)
        }
        regions_forecast[region_name] = forecast

    return regions_forecast

def save_forecast(forecast):
    time = pd.to_datetime(datetime.now()).floor('h').strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = os.path.join(os.getcwd(), 'predict_data/forecast')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, f"forecast_{time}.json")

    result = {
        "last_model_train_time": '2025-04-26_23-18-03',
        "regions_forecast": forecast
    }

    with open(file_path, "w") as f:
        json.dump(result, f)

    print(f"Forecast saved to {file_path}")

def main():
    scaler, model = load_models()
    df = load_data()
    forecast = generate_forecast(df, scaler, model)
    save_forecast(forecast)

if __name__ == "__main__":
    main()