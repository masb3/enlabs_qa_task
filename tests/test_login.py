import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from common.login_form_elements import (MAIN_PAGE_LOGIN_BTN, EMAIL_FIELD, PWD_FIELD, LOGIN_BTN,
                                        EMAIL_VALIDATION_ERROR, PWD_VALIDATION_ERROR, INVAL_EMAIL_PWD_ERROR,
                                        FORGOT_PWD_BTN, SIGNUP_BTN)


URL = 'https://www.optibet.lt/'


class TestLoginForm:
    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.get(URL)
        time.sleep(3)
        # Open login form
        cls.driver.find_element_by_xpath(MAIN_PAGE_LOGIN_BTN).click()
        time.sleep(1)
        cls.initial_url = cls.driver.current_url

        cls.email_field = cls.driver.find_element_by_name(EMAIL_FIELD)
        cls.pwd_field = cls.driver.find_element_by_name(PWD_FIELD)
        cls.login_button = cls.driver.find_element_by_css_selector(LOGIN_BTN)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @classmethod
    def clear_fields(cls):
        cls.email_field.send_keys(Keys.CONTROL + 'a')
        cls.email_field.send_keys(Keys.DELETE)
        cls.pwd_field.send_keys(Keys.CONTROL + 'a')
        cls.pwd_field.send_keys(Keys.DELETE)

    @pytest.mark.parametrize('email_field_text,pwd_field_text', [('asadadaaa@', 'qwerty'),
                                                                 ('qqqqqqqqqqqqq', '   '),
                                                                 ('@gmail.com', '')])
    def test_invalid_email(self, email_field_text, pwd_field_text):
        self.clear_fields()

        self.email_field.send_keys(email_field_text)
        self.pwd_field.send_keys(pwd_field_text)

        time.sleep(1)

        try:
            email_validation_error = self.driver.find_element_by_xpath(EMAIL_VALIDATION_ERROR)
        except NoSuchElementException:
            email_validation_error = None

        try:
            pwd_validation_error = self.driver.find_element_by_xpath(PWD_VALIDATION_ERROR)
        except NoSuchElementException:
            pwd_validation_error = None

        assert email_validation_error is not None
        assert pwd_validation_error is None if pwd_field_text else not None

    @pytest.mark.parametrize('email_field_text,pwd_field_text', [('asadadaaa@ee.ee', ''),
                                                                 ('qqqqqqqqqqqqq@qwe.ro', ' '),
                                                                 ('1@gmail.com', 'asas7')])
    def test_valid_email(self, email_field_text, pwd_field_text):
        self.clear_fields()

        self.email_field.send_keys(email_field_text)
        self.pwd_field.send_keys(pwd_field_text)

        time.sleep(1)

        try:
            email_validation_error = self.driver.find_element_by_xpath(EMAIL_VALIDATION_ERROR)
        except NoSuchElementException:
            email_validation_error = None

        try:
            pwd_validation_error = self.driver.find_element_by_xpath(PWD_VALIDATION_ERROR)
        except NoSuchElementException:
            pwd_validation_error = None

        assert email_validation_error is None
        assert pwd_validation_error is None if pwd_field_text else not None

    def test_login_fails(self):
        self.clear_fields()

        valid_email = 'qwerty@gmail.com'
        valid_pwd = 'dfP1a'
        self.email_field.send_keys(valid_email)
        self.pwd_field.send_keys(valid_pwd)

        self.login_button.click()
        time.sleep(2)

        try:
            invalid_email_pwd_error = self.driver.find_element_by_xpath(INVAL_EMAIL_PWD_ERROR)
        except NoSuchElementException:
            invalid_email_pwd_error = None

        assert invalid_email_pwd_error is not None
        assert self.driver.current_url == self.initial_url


def test_forgot_pwd_button():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(3)
    # Open login form
    driver.find_element_by_xpath(MAIN_PAGE_LOGIN_BTN).click()
    time.sleep(1)

    forgot_pwd_button = driver.find_element_by_xpath(FORGOT_PWD_BTN)

    forgot_pwd_button.click()
    time.sleep(1)

    try:
        assert 'forgot-password' in driver.current_url
    finally:
        driver.quit()


def test_signup_button():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(3)
    # Open login form
    driver.find_element_by_xpath(MAIN_PAGE_LOGIN_BTN).click()
    time.sleep(1)

    signup_button = driver.find_element_by_xpath(SIGNUP_BTN)

    signup_button.click()
    time.sleep(1)

    try:
        assert 'signup' in driver.current_url
    finally:
        driver.quit()
