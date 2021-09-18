from selenium.webdriver import ActionChains
import time

from . import paths

def load_full_content(driver, url, scroll_times=5):
    """Perform certain operations on loaded page to get it's full content"""
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)
    actions = ActionChains(driver)
    scroll = driver.find_element_by_xpath(paths.SCROLL)
    popup = driver.find_element_by_xpath(paths.POPUP)
    popup_btn = driver.find_element_by_xpath(paths.POPUP_BTN)

    def check_popup():
        if popup.is_displayed():
            popup_btn.click()

    while scroll_times:
        try:
            check_popup()
            actions.move_to_element(scroll).perform()
            scroll_times -= 1
            time.sleep(1.7)
        except Exception:
            check_popup()
            scroll_times -= 1
            time.sleep(1)
            continue
    return driver.page_source


def extract_name(text):
    return text.split('-')[0].strip()


def players_parser(data):
    player1 = data[0].strip()
    player2 = data[1].strip()
    event_name = f"{player1} vs {player2}"
    return event_name, player1, player2