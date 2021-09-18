import datetime

from selenium.webdriver import ActionChains
import time

from . import paths

def load_full_content(driver, url, scroll_times=5):
    """Perform certain operations on loaded page to get its full content"""
    driver.get(url)
    driver.implicitly_wait(time_to_wait=5)
    actions = ActionChains(driver)
    scroll = driver.find_element_by_xpath(paths.SCROLL)
    popup = driver.find_element_by_xpath(paths.POPUP)
    popup_btn = driver.find_element_by_xpath(paths.POPUP_BTN)

    def check_popup():
        """Check if cookie div appeared and close if true"""
        if popup.is_displayed():
            popup_btn.click()

    # In order to load all tennis matches script have
    # to scroll down and wait to load more content,
    # each scroll loads up to 50 new events. Try/Except
    # block needed to prevent missing elements exceptions.

    while scroll_times:
        try:
            check_popup()
            # Navigate to bottom element of scrollable div
            actions.move_to_element(scroll).perform()
            scroll_times -= 1
            time.sleep(1.7)
        except Exception:
            check_popup()
            scroll_times -= 1
            time.sleep(1)
            continue
    return driver.page_source


def get_now_utc():
    """return timezone aware datetime object in UTC tz"""
    return datetime.datetime.now(tz=datetime.timezone.utc)


def update_parser(data):
    """Convert timezone aware datetime object to string"""
    return data.strftime('%Y-%m-%d %H:%M')


def event_date_parser(data, data2=None):
    if data2:
        return f"{data} {data2}"
    else:
        return f"{data}"


def t_name_parser(data):
    """Parse tournaments names"""
    return data.split('-')[0].strip()


def players_parser(data):
    """Parse players names, strip and create event_name variable"""
    player1 = data[0].strip()
    player2 = data[1].strip()
    event_name = f"{player1} vs {player2}"
    return event_name, player1, player2