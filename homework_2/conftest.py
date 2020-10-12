import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui.page import BasePage, IndexPage

CAPABILITIES = {'browserName': 'chrome', 'version': '80.0', 'platform': 'LINUX'}


def pytest_addoption(parser):
    parser.addoption('--selenoid', default='none')


@pytest.fixture(scope='session')
def config(request):
    selenoid_ports = request.config.getoption('--selenoid')
    return {'selenoid_ports': selenoid_ports}


@pytest.fixture(scope='function')
def driver(config):
    if config['selenoid_ports'] == 'none':
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        host, port = config['selenoid_ports'].split(':')
        driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                                  desired_capabilities=CAPABILITIES)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def index_page(driver):
    return IndexPage(driver=driver)
