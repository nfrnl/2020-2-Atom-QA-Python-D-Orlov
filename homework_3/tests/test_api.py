import pytest

from api.client import APIClient

USER_EMAIL = 'uvcxcjfpfwouvgrklk@twzhhq.online'
USER_PASSWORD = '8Khaeyk85Wpj2qr'


@pytest.mark.API
class TestAPI:
    client = APIClient()

    @pytest.fixture(scope='function')
    def login(self):
        self.client.login(USER_EMAIL, USER_PASSWORD)

    def test_segment_creation(self, login):
        segment_id = self.client.create_segment('New segment')
        assert segment_id in self.client.get_all_segments_ids()

    def test_segment_deletion(self, login):
        segment_id = self.client.create_segment('New segment')
        self.client.delete_segment(segment_id)
        assert segment_id not in self.client.get_all_segments_ids()
