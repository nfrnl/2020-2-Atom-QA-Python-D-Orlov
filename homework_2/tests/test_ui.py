import random
import string
import pytest

from tests.base import BaseCase
from ui.page import DashboardPage

USER_EMAIL = 'uvcxcjfpfwouvgrklk@twzhhq.online'
USER_PASSWORD = '8Khaeyk85Wpj2qr'


@pytest.fixture
def randomized_string(length: int = 60):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@pytest.mark.UI
class TestUI(BaseCase):
    @pytest.fixture
    def authorized(self):
        self.driver.get(self.index_page.URL)
        self.index_page.authorize(USER_EMAIL, USER_PASSWORD)
        return DashboardPage(self.driver)

    def test_login(self):
        self.driver.get(self.index_page.URL)
        self.index_page.authorize(USER_EMAIL, USER_PASSWORD)
        assert self.driver.current_url == DashboardPage.URL

    def test_login_error(self):
        email = 'nosuchemail@test.com'
        password = '123123123'
        self.driver.get(self.index_page.URL)
        self.index_page.authorize(email, password)
        assert 'Invalid login or password' or 'Login attempts limit has been exceeded' in self.driver.page_source

    def test_campaign_creation(self, authorized, randomized_string):
        page = authorized
        page.create_campaign(randomized_string)
        assert randomized_string in page.driver.page_source

    def test_segment_creation(self, authorized, randomized_string):
        page = authorized.go_to_segments()
        page.create_segment(randomized_string)
        assert randomized_string in self.driver.page_source

    def test_segment_deletion(self, authorized, randomized_string):
        page = authorized.go_to_segments()
        page.create_segment(randomized_string)
        page.delete_segment(randomized_string)
        assert randomized_string not in self.driver.page_source
