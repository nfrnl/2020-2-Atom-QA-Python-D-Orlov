from typing import Any, Dict, List
from urllib.parse import urljoin
import requests


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class CSRFTokenNotSetException(Exception):
    pass


class APIClient:
    def __init__(self):
        self.base_url = 'https://target.my.com'
        self.session = requests.Session()

    @property
    def csrf_token(self) -> str:
        token = self.session.cookies.get('csrftoken')
        if token is None:
            raise CSRFTokenNotSetException('No CSRF Token set for this client')
        return token

    def _request(self, method: str, location: str, status_code: int = 200, headers: Dict = None, params: Dict = None,
                 data: Dict = None, json: Dict = None, json_resp: bool = True, fullpath: bool = False) -> Any:
        if not fullpath:
            url = urljoin(self.base_url, location)
        else:
            url = location
        response = self.session.request(method, url, headers=headers, params=params, data=data, json=json)
        if response.status_code != status_code:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')
        if json_resp:
            json_response = response.json()
            if json_response.get('bStateError'):
                error = json_response['sErrorMsg']
                raise RequestErrorException(f'Request "{url}" failed with error "{error}"!')
            return json_response
        return response

    def _get_csrf_token(self) -> None:
        location = 'csrf/'
        self._request('GET', location, json_resp=False)

    def login(self, email: str, password: str) -> None:
        location = 'https://auth-ac.my.com/auth'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://target.my.com/'
        }
        data = {
            'email': email,
            'password': password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self._request('POST', location, status_code=200, headers=headers, data=data, json_resp=False, fullpath=True)
        self._get_csrf_token()

    def create_segment(self, name: str) -> int:
        location = 'api/v2/remarketing/segments.json'
        payload = {'name': name,
                   'pass_condition': 1,
                   'relations': [{'object_type': 'remarketing_player',
                                  'params': {'type': 'positive',
                                             'left': 365,
                                             'right': 0}}],
                   'logicType': 'or'}
        headers = {'Content-Type': 'application/json',
                   'X-CSRFToken': self.csrf_token}
        response = self._request('POST', location, headers=headers, json=payload)
        return response['id']

    def get_all_segments_ids(self) -> List[int]:
        location = 'api/v2/remarketing/segments.json'
        segments_json = self._request('GET', location)
        return [item['id'] for item in segments_json['items']]

    def delete_segment(self, segment_id: int) -> None:
        location = f'api/v2/remarketing/segments/{segment_id}.json'
        headers = {'X-CSRFToken': self.csrf_token}
        self._request('DELETE', location, status_code=204, headers=headers, json_resp=False)
