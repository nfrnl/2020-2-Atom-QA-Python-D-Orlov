import json
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class MockHandleRequests(BaseHTTPRequestHandler):
    users_data = None
    users_sens_data = None
    auth_token = None
    avail_data = {}

    def _set_headers(self, status=200, is_json=True):
        self.send_response(status)
        if is_json:
            self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def _bad_request(self):
        self._set_headers(400)
        self.wfile.write('Error: bad request'.encode())

    def _forbidden(self):
        self._set_headers(403)
        self.wfile.write('Error: forbidden'.encode())

    def _not_found(self):
        self._set_headers(404)
        self.wfile.write('Error: not found'.encode())

    def _method_not_supported(self):
        self._set_headers(405)
        self.wfile.write('Error: method not allowed'.encode())

    def do_GET(self):
        if self.path == '/':
            self._set_headers()
            self.wfile.write(json.dumps(self.users_data).encode())
        elif self.path.startswith('/get_token/') and self.path[11:].isnumeric():
            if 'Authorized' in self.headers and self.headers['Authorized'] == self.auth_token:
                user_id = int(self.path[11:])
                for i, user in enumerate(self.users_sens_data):
                    if user['id'] == user_id:
                        ret_token = user['token']
                        break
                else:
                    self.users_sens_data.append({'id': user_id, 'token': '000000'})
                    ret_token = '000000'
                self._set_headers()
                self.wfile.write(ret_token.encode())
            else:
                self._set_headers(401)
                self.wfile.write('Error: authorization error'.encode())
        elif self.path == '/availability':
            if self.avail_data is True:
                sleep(3)
            else:
                self._set_headers(500)
                self.wfile.write('Internal server error'.encode())
        elif self.path.startswith('/') and self.path[1:].isnumeric():
            self._method_not_supported()
        else:
            self._not_found()

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            read_data = json.loads(self.rfile.read(content_length).decode())
            if 'id' in read_data and 'name' in read_data and len(read_data) == 2:
                self.users_data = self.users_data.append(read_data)
                self._set_headers()
                self.wfile.write('Success'.encode())
            else:
                self._bad_request()
        else:
            self._method_not_supported()

    def do_PUT(self):
        if self.path.startswith('/') and self.path[1:].isnumeric():
            content_length = int(self.headers['Content-Length'])
            read_data = json.loads(self.rfile.read(content_length).decode())
            if 'name' in read_data and len(read_data) == 1:
                for i, user in enumerate(self.users_data):
                    if user['id'] == int(self.path[1:]):
                        self.users_data[i]['name'] = read_data['name']
                        break
                else:
                    self._set_headers(400)
                    self.wfile.write('Error: no such user exists'.encode())
                    return
                self._set_headers()
                self.wfile.write('Success'.encode())
            else:
                self._bad_request()
        else:
            self._method_not_supported()


class SimpleHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop_server = False
        self.handler = MockHandleRequests
        self.handler.data = None
        self.server = HTTPServer((self.host, self.port), self.handler)

    def start(self):
        self.server.allow_reuse_address = True
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        return self.server

    def stop(self):
        self.server.server_close()
        self.server.shutdown()

    def set_data(self, users, users_sens, token):
        self.handler.users_data = users
        self.handler.users_sens_data = users_sens
        self.handler.auth_token = token

    def set_availability(self, data):
        self.handler.avail_data = data
