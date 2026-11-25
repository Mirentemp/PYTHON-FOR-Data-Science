import requests

base_url = 'https://jsonplaceholder.typicode.com'

def get_json(path, params=None):
    resp = requests.get(f'{base_url}{path}', params=params, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    raise RuntimeError(f'request failed with status code {resp.status_code}')

if __name__ == '__main__':
    for test_path in ['/todos/1', '/todos/9999']:
        try:
            data = get_json(test_path)
            print(test_path, data)
        except RuntimeError as e:
            print(test_path, 'error:', e)
