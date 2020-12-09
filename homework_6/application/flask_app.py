import threading
from urllib.parse import urljoin
from flask import Flask, request, jsonify
import requests
from requests.exceptions import ConnectionError, Timeout

from tests import settings

app = Flask(__name__)
avail_data = {}


def run_app():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.APP_HOST,
        'port': settings.APP_PORT
    })
    server.start()
    return server


def shutdown_app():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_app()


@app.errorhandler(405)
def method_not_allowed(error):
    return 'Error: method not allowed', 405


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        resp = requests.get(settings.MOCK_URL)
        if resp.status_code == requests.codes.ok:
            users_data = resp.json()
            result = [user['name'] for user in users_data]
            return jsonify(result)
        else:
            return jsonify('Error: could not add user'), 400
    elif request.method == 'POST':
        if request.is_json:
            requests.post(settings.MOCK_URL, data=request.data)
            return jsonify('User successfully added')
        else:
            return jsonify('Error: expected JSON'), 400


@app.route('/users/<user_id>', methods=['PUT'])
def user(user_id):
    if request.method == 'PUT':
        if request.is_json:
            resp = requests.put(urljoin(settings.MOCK_URL, str(user_id)), data=request.data)
            if resp.status_code == requests.codes.ok:
                return jsonify('User successfully updated')
            else:
                return jsonify('Error: could not update user'), 400
        else:
            return jsonify('Error: expected JSON'), 400


@app.route('/<user_id>/authorized')
def authorized(user_id):
    if 'Authorized' not in request.headers:
        resp = requests.get(urljoin(settings.MOCK_AUTH_URL, user_id))
    else:
        resp = requests.get(urljoin(settings.MOCK_AUTH_URL, user_id),
                            headers={'Authorized': request.headers['Authorized']})
    if resp.status_code != requests.codes.ok:
        return jsonify('Error: not authorized'), 401
    return jsonify('Token successfully set')


@app.route('/available')
def avail():
    try:
        resp = requests.get(urljoin(avail_data['url'], 'availability'), timeout=avail_data['timeout'])
        if resp.status_code == requests.codes.ok:
            return jsonify('Success')
        else:
            return jsonify('Unavailable'), 500
    except ConnectionError:
        return jsonify('Could not connect'), 500
    except Timeout:
        return jsonify('Connection has timeouted'), 500


if __name__ == '__main__':
    run_app()
