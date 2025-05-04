import os
import pandas as pd
from datetime import date
from src.preparations import alerts_in_ua as a, weather_scrap as w
import holidays


def main():
    df_regions = pd.read_csv(f"../data/regions.csv")
    df_regions["region"] = df_regions["region"].apply(lambda x: x + " обл.")

    weather_regions = [
        "Vinnytsia, Ukraine", "Lutsk, Ukraine", "Dnipro, Ukraine", "Donetsk, Ukraine",
        "Zhytomyr, Ukraine", "Uzhhorod, Ukraine", "Zaporizhia, Ukraine",
        "Ivano-Frankivsk, Ukraine", "Kyiv, Ukraine", "Kropyvnytskyi, Ukraine",
        "Lviv, Ukraine", "Mykolaiv, Ukraine", "Odessa, Ukraine", "Poltava, Ukraine",
        "Rivne, Ukraine", "Sumy, Ukraine", "Ternopil, Ukraine", "Kharkiv, Ukraine",
        "Kherson, Ukraine", "Khmelnytskyi, Ukraine", "Cherkasy, Ukraine",
        "Chernivtsi, Ukraine", "Chernigiv, Ukraine"
    ]

    all_data = []
    for region in weather_regions:
        forecast = w.generate_forecast(region)
        df_region = pd.DataFrame(forecast)
        all_data.append(df_region)

    df_weather = pd.concat(all_data, ignore_index=True)
    df_weather["city"] = df_weather["city_resolvedAddress"].apply(lambda x: x.split(",")[0])
    df_weather["city"] = df_weather["city"].replace('Хмельницька область', "Хмельницький")

    df_weather_reg = pd.merge(df_weather, df_regions, left_on="city", right_on="center_city_ua")
    df_weather_reg["region"] = df_weather_reg["region"].str.replace(r"\s*обл\.?", " область", regex=True)

    kyiv_reg = df_weather_reg[df_weather_reg["region"] == "Київська область"].copy()
    kyiv_reg["region"] = "Київ"
    kyiv_reg["region_id"] = 1
    df_weather_reg = pd.concat([df_weather_reg, kyiv_reg])

    df_alarms = pd.DataFrame(a.get_alerts())
    df_alarms["status"] = df_alarms["status"].apply(lambda x: 1 if x == 'A' or x == 'P' else 0)

    df_weather_reg_al = df_weather_reg.merge(df_alarms, how="left", on="region")
    df_weather_reg_al["day_datetime"] = pd.to_datetime(df_weather_reg_al["day_datetime"])

    df_isw_vect = pd.read_csv("../data/ISW_vector.csv")
    df_isw_vect = df_isw_vect.tail(1)
    df_isw_vect = pd.concat([df_isw_vect] * len(df_weather_reg_al), ignore_index=True)

    df_ready = pd.concat([df_weather_reg_al.reset_index(drop=True), df_isw_vect.reset_index(drop=True)], axis=1)

    df = df_ready.fillna(df_ready.median(numeric_only=True))
    df['hour_preciptype'] = df['hour_preciptype'].astype(str)
    df_encoded = pd.get_dummies(df, columns=['hour_preciptype'], prefix='hour_preciptype')

    bool_columns = df_encoded.select_dtypes(include=['bool']).columns
    df_encoded[bool_columns] = df_encoded[bool_columns].astype(int)

    preciptype = [
        "hour_preciptype_['freezingrain']", "hour_preciptype_['ice']",
        "hour_preciptype_['rain', 'snow']", "hour_preciptype_['rain']",
        "hour_preciptype_['snow']"
    ]

    for col in preciptype:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    other_cols = [c for c in df_encoded.columns if c not in preciptype]
    df_encoded = df_encoded[other_cols + preciptype]

    todrop = [
        'city_resolvedAddress', 'day_datetime', 'city', 'region',
        'center_city_ua', 'center_city_en', 'region_alt', 'date',
        'content', 'lemma_content', 'stem_content'
    ]
    df_encoded = df_encoded.drop(todrop, axis=1)

    temp_df = df_encoded['keywords'].str.split(expand=True).astype('float64')
    df_encoded_v2 = pd.concat([df_encoded.drop('keywords', axis=1), temp_df], axis=1)

    unique_values = sorted(df['hour_conditions'].astype(str).unique())
    mapping = {val: idx for idx, val in enumerate(unique_values)}
    df_encoded_v2['hour_conditions'] = df['hour_conditions'].astype(str).map(mapping)

    for col in ['hour_datetime', 'day_sunrise', 'day_sunset']:
        df_encoded_v2[col] = pd.to_datetime(df_encoded_v2[col], format='%H:%M:%S')
        df_encoded_v2[col] = (df_encoded_v2[col].dt.hour * 3600 +
                              df_encoded_v2[col].dt.minute * 60 +
                              df_encoded_v2[col].dt.second) / 86400

    df_temp = pd.read_parquet("../data/all_data_preprocessed/all_merged.parquet", engine="pyarrow",
                              columns=['event_all_region', 'region_id', 'hour_datetimeEpoch'])
    df_temp['timestamp'] = pd.to_datetime(df_temp['hour_datetimeEpoch'], unit='s')
    df_temp['date'] = df_temp['timestamp'].dt.date
    last_date = df_temp['date'].max()
    df_temp = df_temp[df_temp['date'] == last_date]

    df_encoded_v2['timestamp'] = pd.to_datetime(df_encoded_v2['hour_datetimeEpoch'], unit='s')
    df_encoded_v2 = df_encoded_v2.set_index(pd.DatetimeIndex(df_encoded_v2['timestamp']))
    df_temp = df_temp.set_index(pd.DatetimeIndex(df_temp['timestamp']))

    hourly_has_event = df_temp.groupby('region_id')['event_all_region'].resample('h').sum().gt(0).astype(int)
    hours_with_events_per_day = hourly_has_event.groupby('region_id').resample('D', level=1).sum().reset_index()
    hours_with_events_per_day.rename(columns={'event_all_region': 'event_lastDay_region'}, inplace=True)

    df_encoded_v2['date'] = df_encoded_v2['timestamp'].dt.strftime('%Y-%m-%d')
    hours_with_events_per_day['date'] = hours_with_events_per_day['timestamp'].dt.strftime('%Y-%m-%d')

    df_encoded_v2 = df_encoded_v2.sort_values('timestamp')
    hours_with_events_per_day = hours_with_events_per_day.sort_values('timestamp')

    df_encoded_v2 = pd.merge_asof(
        df_encoded_v2,
        hours_with_events_per_day[['timestamp', 'region_id', 'event_lastDay_region']],
        on='timestamp',
        by='region_id',
        direction='backward'
    )

    class UkrainianECBHolidays(holidays.HolidayBase):
        def __init__(self, years=None, **kwargs):
            self.country = "UA"
            super().__init__(years=years, **kwargs)

        def _populate(self, year):
            self[date(year, 1, 1)] = "New Year's Day"
            self[date(year, 1, 7)] = "Orthodox Christmas"
            self[date(year, 3, 8)] = "International Women's Day"
            self[date(year, 5, 1)] = "Labour Day"
            self[date(year, 5, 8)] = "Day of Remembrance and Reconciliation"
            self[date(year, 5, 9)] = "Victory Day"
            self[date(year, 6, 28)] = "Constitution Day of Ukraine"
            self[date(year, 8, 24)] = "Independence Day of Ukraine"
            self[date(year, 12, 25)] = "Christmas (Western)"

    class RussianECBHolidays(holidays.HolidayBase):
        def __init__(self, years=None, **kwargs):
            self.country = "RU"
            super().__init__(years=years, **kwargs)

        def _populate(self, year):
            self[date(year, 1, 1)] = "New Year's Day (Russia)"
            self[date(year, 1, 7)] = "Orthodox Christmas (Russia)"
            self[date(year, 2, 23)] = "Defender of the Fatherland Day (Russia)"
            self[date(year, 3, 8)] = "International Women's Day (Russia)"
            self[date(year, 5, 1)] = "Spring and Labor Day (Russia)"
            self[date(year, 5, 9)] = "Victory Day (Russia)"
            self[date(year, 6, 12)] = "Russia Day"
            self[date(year, 11, 4)] = "Unity Day (Russia)"

    ua_holidays = UkrainianECBHolidays(years=range(2020, 2032))
    ru_holidays = RussianECBHolidays(years=range(2020, 2032))

    df_encoded_v2['ru_holiday'] = df_encoded_v2['date'].apply(lambda x: 1 if x in ru_holidays else 0)
    df_encoded_v2['ua_holiday'] = df_encoded_v2['date'].apply(lambda x: 1 if x in ua_holidays else 0)

    df_encoded_v2.drop(['date', 'timestamp'], axis=1, inplace=True)

    col_data = df_encoded_v2.pop("status")
    insert_at = df_encoded_v2.columns.get_loc("event_lastDay_region") + 1
    df_encoded_v2.insert(insert_at, "status", col_data)

    col_data = df_encoded_v2.pop("region_id")
    insert_at = df_encoded_v2.columns.get_loc('day_datetimeEpoch')
    df_encoded_v2.insert(insert_at, "region_id", col_data)

    if 'hour_preciptype_None' in df_encoded_v2.columns:
        df_encoded_v2.drop(["hour_preciptype_None"], axis=1, inplace=True)

    data_dir = os.path.join(os.getcwd(), 'predict_data/everyhour_predict')
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, 'test.csv')
    df_encoded_v2.to_csv(csv_path, sep=';', index=False)


if __name__ == "__main__":
    main()
