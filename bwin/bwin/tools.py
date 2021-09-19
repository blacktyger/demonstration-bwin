from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timezone, timedelta
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from timestring import Date
from decimal import *
import tzlocal
import pytz
import time

from twisted.conch.telnet import EC

from . import paths

def load_full_content(driver, url, scroll_times=3):
    """Perform certain operations on loaded page to get its full content"""
    driver.get(url)
    # driver.implicitly_wait(time_to_wait=10)
    actions = ActionChains(driver)

    # Try to find loading element on page, if false no need to scroll
    try:
        more_items = driver.find_element_by_xpath(paths.MORE_ITEMS)

    except NoSuchElementException:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, paths.MORE_ITEMS))).click()
        more_items = driver.find_element_by_xpath(paths.MORE_ITEMS)

    def check_popup():
        """Check if cookie div appeared and close if true"""
        try:
            popup = driver.find_element_by_xpath(paths.POPUP)
            popup_btn = driver.find_element_by_xpath(paths.POPUP_BTN)
            if popup.is_displayed():
                popup_btn.click()
        except NoSuchElementException:
            pass

    # In order to load all tennis matches, script have
    # to scroll down and wait to load more content,
    # each scroll loads up to 50 new events. Try/Except
    # block as sometimes loading element is missing.
    while scroll_times:
        try:
            check_popup()
            # Navigate to bottom element of scrollable div
            actions.move_to_element(more_items).perform()
            scroll_times -= 1
            time.sleep(0.2)
        except Exception:
            check_popup()
            scroll_times -= 1
            time.sleep(0.2)
            continue
    return driver.page_source


def get_now_utc():
    """return timezone aware datetime object in UTC tz"""
    return datetime.now(tz=timezone.utc)


def convert_dt_to_str(data):
    """Convert datetime object to string and format"""
    if isinstance(data, datetime):
        return data.strftime('%Y-%m-%d %H:%M')
    else:
        return None


def t_name_parser(data):
    """Parse tournaments names"""
    return data.split('-')[0].strip()


def odds_parser(data):
    """Convert fractional odds to decimal with Decimal library"""
    try:
        getcontext().prec = 2
        num1, num2 = data.split('/')
        dec = (Decimal(num1) / Decimal(num2)) + 1
        return dec
    except Exception:
        return None


def date_parser(data, data2=None):
    """Get machine local tz, parse dates from page and convert to UTC tz"""
    # Sometimes page is dividing event date in to 2 elements, join them here
    data = f"{data}{data2}"

    # Get local tz and set desired output tz
    local_tz = pytz.timezone(tzlocal.get_localzone().key)
    output_tz = pytz.timezone('UTC')

    # There are 2 types of event dates, we have to use different parsing
    if any(x in data for x in ['Tomorrow', 'Today']):
        # Convert variety of strings dates in to timestring objects
        # thanks to timestring package (https://pypi.org/project/timestring/)
        # and convert them to standard python datetime objects
        date = Date(data.replace('/', ''))
        date_dt = datetime.fromtimestamp(date.to_unixtime(), tz=local_tz)
        date_dt = date_dt.astimezone(output_tz)
    elif 'Starting' in data:
        if 'Starting now' in data:
            return None
        # Calculate timedelta for upcoming events and convert tz's
        minutes_left = int(data.split(' ')[-2])
        now = datetime.now(tz=local_tz)
        date_dt = (now + timedelta(minutes=minutes_left)).astimezone(output_tz)
    else:
        # Something went wrong
        date_dt = None
        print(f"\n"
                    f"\n"
                    f"-----------------  {data}"
                    f"\n")
    return convert_dt_to_str(date_dt)


def players_parser(data):
    """Parse players names, strip and create event_name variable"""
    try:
        player1 = data[0].strip()
        player2 = data[1].strip()
        event_name = f"{player1} vs {player2}"
        return event_name, player1, player2
    except IndexError:
        return None, None, None