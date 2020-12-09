from urllib.parse import urljoin
import pytest
import requests

from client.socket_client import SocketClient
from application import flask_app
from mock.http_server_mock import SimpleHTTPServer
from tests import settings


@pytest.fixture(scope='session', autouse=True)
def mock_server():
    mock = SimpleHTTPServer(settings.MOCK_HOST, settings.MOCK_PORT)
    mock.start()
    yield mock
    mock.stop()


@pytest.fixture(scope='session', autouse=True)
def app_server():
    flask_app.run_app()
    yield flask_app
    requests.get(urljoin(settings.APP_URL, 'shutdown'))


def app_client():
    return SocketClient(settings.APP_HOST, settings.APP_PORT)


class TestMock:
    @pytest.fixture(scope='function')
    def init_data(self, mock_server):
        users_data = [
            {
                'id': 0,
                'name': 'Name1'
            },
            {
                'id': 1,
                'name': 'Name2'
            }
        ]
        users_sens_data = [
            {
                'id': 0,
                'token': '000000'
            }
        ]
        token = 'abcdefg'
        mock_server.set_data(users_data, users_sens_data, token)
        return {
            'users_data': users_data,
            'users_sens_data': users_sens_data,
            'token': token
        }

    def test_get_users(self, init_data):
        resp = app_client().get(settings.APP_USERS_URL)
        init_users = [user['name'] for user in init_data['users_data']]
        assert resp.data == init_users

    def test_add_user(self, init_data):
        resp = app_client().post(settings.APP_USERS_URL, json={'id': 100, 'name': 'Name100'})
        assert resp.status_code == 200

    def test_update_user_info(self, init_data):
        url = urljoin(settings.APP_URL, 'users/1')
        resp = app_client().put(url, json={'name': 'NewName'})
        assert resp.status_code == 200

    def test_update_malformed_user_info(self, init_data):
        url = urljoin(settings.APP_URL, 'users/1')
        resp = app_client().put(url)
        assert resp.status_code == 400

    def test_update_nonexistent_user(self, init_data):
        url = urljoin(settings.APP_URL, 'users/2')
        resp = app_client().put(url, json={'name': 'NewName'})
        assert resp.status_code == 400

    def test_mock_unavailable(self):
        flask_app.avail_data = {'url': settings.MOCK_ANOTHER_INST_URL, 'timeout': 5}
        resp = app_client().get(settings.APP_AVAIL_URL)
        assert resp.status_code == 500

    def test_mock_timeouted(self, mock_server):
        flask_app.avail_data = {'url': settings.MOCK_URL, 'timeout': 1}
        mock_server.set_availability(True)
        resp = app_client().get(settings.APP_AVAIL_URL)
        assert resp.status_code == 500

    def test_mock_server_error(self, mock_server):
        flask_app.avail_data = {'url': settings.MOCK_URL, 'timeout': 30}
        mock_server.set_availability(False)
        resp = app_client().get(settings.APP_AVAIL_URL)
        assert resp.status_code == 500

    def test_mock_header_valid_data(self, init_data):
        url = urljoin(settings.APP_URL, '0/authorized')
        resp = app_client().get(url, headers={'Authorized': init_data['token']})
        assert resp.status_code == 200

    def test_mock_header_invalid_data(self, init_data):
        url = urljoin(settings.APP_URL, '0/authorized')
        resp = app_client().get(url, headers={'Authorized': 'what'})
        assert resp.status_code == 401

    def test_mock_header_missing(self, init_data):
        url = urljoin(settings.APP_URL, '0/authorized')
        resp = app_client().get(url)
        assert resp.status_code == 401
