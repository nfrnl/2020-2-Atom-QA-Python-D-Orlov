from urllib.parse import urljoin

APP_HOST, APP_PORT = '127.0.0.1', 1050
APP_URL = f'http://{APP_HOST}:{APP_PORT}/'
APP_USERS_URL = urljoin(APP_URL, 'users')
APP_AVAIL_URL = urljoin(APP_URL, 'available')

MOCK_HOST, MOCK_PORT = '127.0.0.1', 1051
MOCK_URL = f'http://{MOCK_HOST}:{MOCK_PORT}/'
MOCK_AUTH_URL = urljoin(MOCK_URL, 'get_token/')
MOCK_ANOTHER_INST_URL = 'http://127.0.0.1:1060/'
