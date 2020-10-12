from selenium.webdriver.common.by import By


class BasePageLocators(object):
    pass


class IndexPageLocators(BasePageLocators):
    LOGIN_BUTTON = (By.XPATH, "//div[contains(@class, 'responseHead-module-button')]")
    INPUT_EMAIL = (By.NAME, 'email')
    INPUT_PASSWORD = (By.NAME, 'password')
    INPUT_BUTTON = (By.XPATH, "//div[contains(@class, 'authForm-module-button')]")


class DashboardPageLocators(BasePageLocators):
    CREATE_CAMPAIGN_BUTTON_EMPTY = (By.XPATH, "//a[text()='Создайте рекламную кампанию']")
    CREATE_CAMPAIGN_BUTTON = (By.XPATH, "//div[text()='Создать кампанию']/parent::div")

    CHOOSE_TYPE_BUTTON = (By.XPATH, "//div[text()='Трафик']/parent::div")
    INPUT_URL = (By.XPATH, "//input[@placeholder='Введите ссылку']")
    AD_TYPE_BANNER_BUTTON = (By.XPATH, "//span[text()='Баннер']/parent::div")
    UPLOAD_INPUT = (By.XPATH, "//div[contains(@class, 'roles-module-buttonWrap')]/div/input")
    IMAGE_CROPPER_SAVE_BUTTON = (By.XPATH, "//input[contains(@class, 'image-cropper__save')]")
    CAMPAIGN_NAME_INPUT = (By.XPATH, "//div[contains(@class, 'input_campaign-name')]/div/input")
    FINAL_CREATE_BUTTON = (By.XPATH, "//div[text()='Создать кампанию']/parent::button")

    TABLE_ELEMENT = (By.XPATH, "//div[contains(@class, 'nameCell') and text()='Итого']")

    SEGMENTS_MENU = (By.XPATH, "//a[@href='/segments']")


class SegmentsPageLocators(BasePageLocators):
    CREATE_SEGMENT_BUTTON_EMPTY = (By.XPATH, "//a[text()='Создайте']")
    CREATE_SEGMENT_BUTTON = (By.CLASS_NAME, 'button_submit')
    SEGMENT_TYPE = (By.XPATH, "//div[text()='Приложения и игры в соцсетях']")
    SEGMENT_CHOOSE_OPTIONS = (By.CLASS_NAME, 'adding-segments-source__checkbox')
    SEGMENT_ADD_BUTTON = (By.XPATH, "//div[text()='Добавить сегмент']/parent::button")
    SEGMENT_NAME_INPUT = (By.XPATH, "//div[contains(@class, 'input_create-segment-form')]//div//input")
    FINAL_CREATE_BUTTON = (By.XPATH, "//div[text()='Создать сегмент']/parent::button")

    @staticmethod
    def created_segment_name_node(name: str):
        return By.XPATH, f"//a[text()='{name}']/parent::div/parent::div"

    DELETE_SEGMENT_BUTTON_FROM_NAME = (By.XPATH, ".//following-sibling::div[4]//span")
    DELETE_SEGMENT_CONFIRM_BUTTON = (By.XPATH, "//div[text()='Удалить']/parent::button")

    TABLE_HEADER = (By.XPATH, "//div[contains(@class, 'page_segments__title')]")
