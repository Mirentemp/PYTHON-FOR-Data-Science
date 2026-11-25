import csv
import json
import time
from datetime import datetime
import requests

INTERVAL_SECONDS = 3600
ROUNDS = 3
API_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality'
LOG_PATH = 'aqi_errors.log'
CSV_PATH = 'aqi_history.csv'

CITIES = [
    ('ahmedabad', 23.03, 72.58),
    ('surat', 21.17, 72.83),
    ('vadodara', 22.31, 73.18),
    ('rajkot', 22.30, 70.80),
    ('mumbai', 19.08, 72.88),
    ('delhi', 28.61, 77.21),
    ('pune', 18.52, 73.86),
    ('bengaluru', 12.97, 77.59),
    ('chennai', 13.08, 80.27),
    ('kolkata', 22.57, 88.36)
]

def log_error(message):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f'{ts} | {message}\n')

def fetch_city(lat, lon, retries=3, hourly_var='pm2_5', base_url=API_URL):
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': hourly_var,
        'forecast_days': 1,
        'timezone': 'Asia/Kolkata'
    }
    for attempt in range(retries):
        try:
            resp = requests.get(base_url, params=params, timeout=10)
            if resp.status_code == 429:
                raise requests.exceptions.HTTPError('HTTP 429 rate limited', response=resp)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', None)
            log_error(f'lat={lat}, lon={lon}, attempt={attempt + 1}/{retries}, status={status_code}, err={e}')
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None

def append_history_rows(rows, csv_path=CSV_PATH):
    file_exists = False
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            if f.read(1):
                file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'city', 'pm2_5'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

def run_once(csv_path=CSV_PATH):
    now_dt = datetime.now()
    hour_idx = now_dt.hour
    ts_str = now_dt.strftime('%Y-%m-%d %H:%M:%S')

    try:
        with open('aqi_hourly_raw.json', 'r', encoding='utf-8') as f:
            cached_raw = json.load(f)
    except FileNotFoundError:
        cached_raw = {}

    batch_rows = []
    for city, lat, lon in CITIES:
        data = fetch_city(lat, lon, retries=2)
        pm_val = None
        if data and 'hourly' in data and 'pm2_5' in data['hourly']:
            vals = data['hourly']['pm2_5']
            if vals and hour_idx < len(vals):
                pm_val = vals[hour_idx]
        elif city in cached_raw and len(cached_raw[city]) > hour_idx:
            pm_val = cached_raw[city][hour_idx]

        batch_rows.append({
            'timestamp': ts_str,
            'city': city,
            'pm2_5': pm_val
        })

    append_history_rows(batch_rows, csv_path=csv_path)
    return len(batch_rows)

def run_loop(interval_seconds=INTERVAL_SECONDS, rounds=ROUNDS, csv_path=CSV_PATH):
    for r in range(rounds):
        run_once(csv_path=csv_path)
        if r < rounds - 1:
            time.sleep(interval_seconds)

if __name__ == '__main__':
    # Clear old test files if re-running directly
    open('aqi_history.csv', 'w', encoding='utf-8').close()
    open('aqi_errors.log', 'w', encoding='utf-8').close()

    run_loop(interval_seconds=20, rounds=3, csv_path='aqi_history.csv')

    # Test fetch_city with invalid hourly variable and unreachable host
    fetch_city(23.03, 72.58, retries=1, hourly_var='not_a_variable')
    fetch_city(23.03, 72.58, retries=1, hourly_var='pm2_5', base_url='https://unreachable-host.invalid/v1/air-quality')

    with open('aqi_history.csv', 'r', newline='', encoding='utf-8') as f:
        hist_rows = list(csv.DictReader(f))
    with open('aqi_errors.log', 'r', encoding='utf-8') as f:
        err_lines = f.readlines()

    print('history data rows:', len(hist_rows))
    print('error log lines:', len(err_lines))
