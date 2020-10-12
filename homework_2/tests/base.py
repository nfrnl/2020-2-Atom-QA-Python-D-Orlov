import pytest
from _pytest.fixtures import FixtureRequest

from ui.page import BasePage, IndexPage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest):
        self.driver = driver
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.index_page: IndexPage = request.getfixturevalue('index_page')
