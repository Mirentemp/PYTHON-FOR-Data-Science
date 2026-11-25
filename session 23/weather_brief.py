import csv
import requests

def analyze_forecast(csv_path='gujarat_forecast.csv'):
    hottest_row = None
    rain_by_city = {}

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t_max = float(row['temp_max_c'])
            rain = float(row['rain_mm'])
            city = row['city']

            if hottest_row is None or t_max > float(hottest_row['temp_max_c']):
                hottest_row = row

            rain_by_city[city] = rain_by_city.get(city, 0.0) + rain

    wettest_city = max(rain_by_city, key=rain_by_city.get)
    print(f"hottest city-day: {hottest_row['city']} on {hottest_row['date']} ({hottest_row['temp_max_c']} c)")
    print(f"most total rain: {wettest_city} ({round(rain_by_city[wettest_city], 2)} mm)")

def fetch_forecast(lat, lon, url='https://api.open-meteo.com/v1/forecast'):
    try:
        resp = requests.get(
            url,
            params={
                'latitude': lat,
                'longitude': lon,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
                'forecast_days': 7,
                'timezone': 'Asia/Kolkata'
            },
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print('request failed:', e)
        return None

if __name__ == '__main__':
    analyze_forecast()
    bhuj_data = fetch_forecast(23.25, 69.67)
    print('bhuj fetch ok:', bhuj_data is not None)
    bad_data = fetch_forecast(23.25, 69.67, url='https://unreachable-host.invalid/v1/forecast')
    print('unreachable fetch result:', bad_data)
