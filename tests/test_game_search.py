import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from common.game_search_elements import SEARCH_BOX, GAMES


URL = 'https://www.isoftbet.com/portfolio/'


def test_search_uppercase():
    """ Searches all games one-by-one in uppercase, validates if it is displayed. Window maximized. Launches game """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.maximize_window()
    time.sleep(3)

    search_box = driver.find_element_by_id(SEARCH_BOX)
    try:
        for game in GAMES:
            search_box.send_keys(Keys.CONTROL + 'a')
            search_box.send_keys(Keys.DELETE)

            game_name = driver.find_element_by_xpath(game.name_xpath).get_attribute('innerHTML')
            search_box.send_keys(game_name.upper())
            time.sleep(1)
            assert driver.find_element_by_xpath(game.xpath).is_displayed() is True

            # Launch game, opens in new tab
            launcher = WebDriverWait(driver, 5).\
                until(EC.element_to_be_clickable((By.XPATH, game.play_btn_xpath)))
            ActionChains(driver).move_to_element(launcher).perform()
            driver.find_element_by_xpath(game.image_click_xpath).click()
            # Move to new tab
            driver.switch_to.window(driver.window_handles[-1])
            assert 'game-launcher-lux' in driver.current_url
            # Close tab and move to parent
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
    finally:
        driver.quit()


def test_search_lowercase():
    """ Searches all games one-by-one in lowercase, validates if it is displayed. Window minimized. Launches game. """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.minimize_window()
    time.sleep(3)

    search_box = driver.find_element_by_id(SEARCH_BOX)
    try:
        for game in GAMES:
            search_box.send_keys(Keys.CONTROL + 'a')
            search_box.send_keys(Keys.DELETE)

            game_name = driver.find_element_by_xpath(game.name_xpath).get_attribute('innerHTML')
            search_box.send_keys(game_name.lower())
            time.sleep(1)
            assert driver.find_element_by_xpath(game.xpath).is_displayed() is True

            # Launch game, opens in new tab
            launcher = WebDriverWait(driver, 5).\
                until(EC.element_to_be_clickable((By.XPATH, game.play_btn_xpath)))
            ActionChains(driver).move_to_element(launcher).perform()
            driver.find_element_by_xpath(game.image_click_xpath).click()
            # Move to new tab
            driver.switch_to.window(driver.window_handles[-1])
            assert 'game-launcher-lux' in driver.current_url
            # Close tab and move to parent
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
    finally:
        driver.quit()


def test_search_mixedcase():
    """ Searches all games one-by-one in mixedcase, validates if it is displayed. Window minimized. Launches game. """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    driver.minimize_window()
    time.sleep(3)

    search_box = driver.find_element_by_id(SEARCH_BOX)
    try:
        for game in GAMES:
            search_box.send_keys(Keys.CONTROL + 'a')
            search_box.send_keys(Keys.DELETE)

            game_name = driver.find_element_by_xpath(game.name_xpath).get_attribute('innerHTML')
            mixed_name = ''
            now_lower = True
            for char in game_name:
                mixed_name += char.lower() if now_lower else char.upper()
                now_lower ^= True
            search_box.send_keys(mixed_name)
            time.sleep(1)
            assert driver.find_element_by_xpath(game.xpath).is_displayed() is True

            # Launch game, opens in new tab
            launcher = WebDriverWait(driver, 5).\
                until(EC.element_to_be_clickable((By.XPATH, game.play_btn_xpath)))
            ActionChains(driver).move_to_element(launcher).perform()
            driver.find_element_by_xpath(game.image_click_xpath).click()
            # Move to new tab
            driver.switch_to.window(driver.window_handles[-1])
            assert 'game-launcher-lux' in driver.current_url
            # Close tab and move to parent
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
    finally:
        driver.quit()


@pytest.mark.xfail(reason="All games are visible if search by symbols as '/*+)'. Need to verify with requirements.")
@pytest.mark.parametrize('dummy_name', ['(/*+#', '0000'])
def test_search_no_match(dummy_name):
    """ Searches for non-matching game name, validates if all games are not displayed. """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    time.sleep(3)

    search_box = driver.find_element_by_id(SEARCH_BOX)

    search_box.send_keys(dummy_name)
    time.sleep(2)

    try:
        for game in GAMES:
            assert driver.find_element_by_xpath(game.xpath).is_displayed() is False
    finally:
        driver.quit()
