from pathlib import Path
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .locators import BasePageLocators, IndexPageLocators, DashboardPageLocators, SegmentsPageLocators

CLICK_RETRY_COUNT = 3
IMAGE_PATH = Path.cwd() / 'resources' / 'image.jpg'


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver) -> None:
        self.driver = driver

    def wait(self, timeout: int = 10) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout: int = 10, hidden: bool = False) -> WebElement:
        web_elem = self.wait(timeout).until(ec.presence_of_element_located(locator))
        if hidden:
            return web_elem
        else:
            return self.wait(timeout).until(ec.visibility_of_element_located(locator))

    def click(self, locator, timeout: int = 10) -> None:
        for i in range(CLICK_RETRY_COUNT):
            try:
                self.find(locator, timeout)
                element = self.wait().until(ec.element_to_be_clickable(locator))
                element.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY_COUNT - 1:
                    raise

    def input(self, locator, data: str, hidden: bool = False) -> None:
        self.find(locator, hidden=hidden).send_keys(data)


class IndexPage(BasePage):
    locators = IndexPageLocators()
    URL = 'https://target.my.com/'

    def authorize(self, email: str, password: str) -> None:
        self.click(self.locators.LOGIN_BUTTON)
        self.input(self.locators.INPUT_EMAIL, email)
        self.input(self.locators.INPUT_PASSWORD, password)
        self.click(self.locators.INPUT_BUTTON)


class DashboardPage(BasePage):
    locators = DashboardPageLocators()
    URL = 'https://target.my.com/dashboard'

    def create_campaign(self, name: str, url: str = 'nosuchsite.com', path_to_image: str = str(IMAGE_PATH)) -> None:
        try:
            self.click(self.locators.CREATE_CAMPAIGN_BUTTON_EMPTY, 5)
        except TimeoutException:
            self.click(self.locators.CREATE_CAMPAIGN_BUTTON)
        self.click(self.locators.CHOOSE_TYPE_BUTTON)
        self.input(self.locators.INPUT_URL, url)
        self.find(self.locators.CAMPAIGN_NAME_INPUT).clear()
        self.input(self.locators.CAMPAIGN_NAME_INPUT, name)
        self.click(self.locators.AD_TYPE_BANNER_BUTTON)
        self.input(self.locators.UPLOAD_INPUT, path_to_image, hidden=True)
        self.click(self.locators.IMAGE_CROPPER_SAVE_BUTTON)
        sleep(1)
        self.click(self.locators.FINAL_CREATE_BUTTON)
        self.find(self.locators.TABLE_ELEMENT)

    def go_to_segments(self):
        self.click(self.locators.SEGMENTS_MENU)
        return SegmentsPage(self.driver)


class SegmentsPage(BasePage):
    locators = SegmentsPageLocators()

    def create_segment(self, name: str):
        try:
            self.click(self.locators.CREATE_SEGMENT_BUTTON, 5)
        except TimeoutException:
            self.click(self.locators.CREATE_SEGMENT_BUTTON_EMPTY)
        self.click(self.locators.SEGMENT_TYPE)
        self.click(self.locators.SEGMENT_CHOOSE_OPTIONS)
        self.click(self.locators.SEGMENT_ADD_BUTTON)
        self.find(self.locators.SEGMENT_NAME_INPUT).clear()
        self.input(self.locators.SEGMENT_NAME_INPUT, name)
        self.click(self.locators.FINAL_CREATE_BUTTON)
        self.find(self.locators.TABLE_HEADER)

    def delete_segment(self, name: str):
        elem = self.find(self.locators.created_segment_name_node(name))
        elem = elem.find_element(*self.locators.DELETE_SEGMENT_BUTTON_FROM_NAME)
        elem.click()
        self.click(self.locators.DELETE_SEGMENT_CONFIRM_BUTTON)
        sleep(1)
