import time

current_token = None
token_expiry = 0.0

def token_endpoint(client_id, client_secret):
    if client_id == 'demo_app' and client_secret == 'demo_secret':
        now = time.time()
        tok = {
            'access_token': 'tok_' + str(now),
            'token_type': 'Bearer',
            'expires_in': 3
        }
        with open('oauth_flow.log', 'a', encoding='utf-8') as f:
            f.write(f"issued {tok['access_token']} at {now:.2f}\n")
        return tok
    raise PermissionError('invalid client credentials')

def get_profile():
    global current_token, token_expiry
    if current_token is None or time.time() >= token_expiry:
        tok_data = token_endpoint('demo_app', 'demo_secret')
        current_token = tok_data['access_token']
        token_expiry = time.time() + tok_data['expires_in']
    return {'student': 'miren', 'course': 'data_science', 'token': current_token}

if __name__ == '__main__':
    with open('oauth_flow.log', 'w', encoding='utf-8') as f:
        pass
    print(get_profile())
    time.sleep(4)
    print(get_profile())
