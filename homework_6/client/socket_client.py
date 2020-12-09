from dataclasses import dataclass
import json as _json
import socket
from typing import Any


@dataclass
class Response:
    status_code: int
    data: Any


class SocketClient:
    def __init__(self, target_host, target_port):
        self.host = target_host
        self.port = target_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10)
        self.client.connect((self.host, self.port))

    def _send_and_receive(self, method, url, data=None, headers=None, json=None):
        url = url.replace(f'http://{self.host}:{self.port}', '')
        request = f'{method} {url} HTTP/1.1\r\nHost: {self.host}\r\n'
        if headers is not None:
            for name, value in headers.items():
                request += f'{name}: {value}\r\n'
        if json is not None:
            request += 'Content-Type: application/json\r\nAccept: application/json\r\n'
        payload = ''
        if json is not None:
            payload += _json.dumps(json)
        elif data is not None:
            payload += _json.dumps(data)
        if payload != '':
            payload = payload.encode()
            request += f'Content-Length: {len(payload)}\r\n'
        request += '\r\n'
        if payload != '':
            self.client.send(request.encode() + payload)
        else:
            self.client.send(request.encode())

        total_data = []
        while True:
            data = self.client.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                break
        response = ''.join(total_data)
        status_code = response.split()[1]
        resp_data = response.split('\r\n\r\n')[1]
        return Response(int(status_code), _json.loads(resp_data))

    def get(self, url, headers=None):
        return self._send_and_receive('GET', url, headers=headers)

    def post(self, url, data=None, headers=None, json=None):
        return self._send_and_receive('POST', url, data, headers, json)

    def put(self, url, data=None, headers=None, json=None):
        return self._send_and_receive('PUT', url, data, headers, json)
