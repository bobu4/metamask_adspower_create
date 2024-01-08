import traceback

import requests
from consts.xpaths import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
from fix import *


def start_profile(profile_id=None):
    url = 'http://local.adspower.net:50325/api/v1/browser/start'
    payload = {"user_id": profile_id}
    return requests.request('GET', url, params=payload).json()


def stop_profile(profile_id=None):
    url = 'http://local.adspower.net:50325/api/v1/browser/stop'
    payload = {"user_id": profile_id}
    return requests.request('GET', url, params=payload).json()


def get_profiles():
    profiles_list = []
    url = 'http://local.adspower.net:50325/api/v1/user/list'
    headers = {
      'Content-Type': 'application/json'
    }
    for page in range(1, 100):
        payload = {'page_size': 100, 'page': page}
        profiles = requests.request("GET", url, params=payload).json()
        if profiles['data']['list']:
            profiles_list[:0] = sorted(profiles['data']['list'],  key=lambda d: int(d['serial_number']))
            time.sleep(1.1)
        else:
            break
    return profiles_list


def click_on_xpath(drive, wait_time, str_path):
    WebDriverWait(drive, wait_time).until(EC.presence_of_element_located((By.XPATH, str_path)))
    WebDriverWait(drive, wait_time).until(EC.element_to_be_clickable((By.XPATH, str_path))).click()


def input_text_xpath(drive, wait_time, send_data, str_path):
    WebDriverWait(drive, wait_time).until(EC.element_to_be_clickable((By.XPATH, str_path))).send_keys(send_data)


profiles = get_profiles()
password = '12345678'
with open('../metamask_upd/seeds.txt', 'a') as seeds:
    for num, prof in enumerate(profiles):
        fix(prof['user_id'])
        resp = start_profile(prof['user_id'])
        time.sleep(4)
        ser = Service(resp["data"]["webdriver"])
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=ser, options=chrome_options)
        driver.get(EXTENSION_URL)
        time.sleep(3)
        click_on_xpath(driver, 10, CONFIRM_TERM)
        time.sleep(1.5)
        click_on_xpath(driver, 10, CREATE_NEW_BUTTON)
        time.sleep(2.1)
        click_on_xpath(driver, 10, CONFIRM_TERMS_BUTTON)
        time.sleep(1.5)
        input_text_xpath(driver, 10, password, INPUT_PASS_FIELD)
        time.sleep(0.6)
        input_text_xpath(driver, 10, 'jackden1', REPEAT_PASS_FIELD)
        time.sleep(0.6)
        click_on_xpath(driver, 10, PASSWORD_CHECKBOX)
        time.sleep(0.9)
        click_on_xpath(driver, 10, PASSWORD_CONFIRM_BUTTON)
        time.sleep(2.4)
        click_on_xpath(driver, 10, SECURE_BUTTON)
        time.sleep(2.8)
        click_on_xpath(driver, 10, REVEAL_MNEMONIC_BUTTON)
        time.sleep(1.4)
        pyperclip.copy(' ')
        while len(pyperclip.paste()) < 30:
            click_on_xpath(driver, 20, COPY_MNEMONIC_BUTTON)
            time.sleep(3)
        print(f'''{num + 1}. {pyperclip.paste()}''')
        seeds.write(f'''\n{num + 1}. {pyperclip.paste()}''')
        mnem = pyperclip.paste().split(' ')
        click_on_xpath(driver, 10, MNEMONIC_NEXT_BUTTON)
        time.sleep(1.2)
        input_text_xpath(driver, 10, mnem[2], THIRD_WORD_FIELD)
        time.sleep(0.6)
        input_text_xpath(driver, 10, mnem[3], FOURTH_WORD_FIELD)
        time.sleep(0.6)
        input_text_xpath(driver, 10, mnem[7], EIGTH_WORD_FIELD)
        time.sleep(0.6)
        click_on_xpath(driver, 10, CONFIRM_MNEMONIC_BUTTON)
        time.sleep(1.5)
        click_on_xpath(driver, 10, OKAY_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, NEXT_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, DONE_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, GOT_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, TRY_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, NO_BUTTON)
        time.sleep(2.6)
        click_on_xpath(driver, 10, CANCEL_SWAP_BUTTON)
        time.sleep(2.6)
        click_on_xpath(driver, 10, OK_BUTTON)
        time.sleep(1.6)
        pyperclip.copy(' ')
        while len(pyperclip.paste()) < 30:
            click_on_xpath(driver, 20, COPY_BUTTON)
            time.sleep(3)
        print(f'''{num + 1}. {pyperclip.paste()}''')
        wallet = pyperclip.paste()
        click_on_xpath(driver, 10, DETAILS_BUTTON)
        time.sleep(0.6)
        click_on_xpath(driver, 10, DETAIL_WALLET)
        time.sleep(0.6)
        click_on_xpath(driver, 10, PRIV_KEY_BUTTON)
        time.sleep(0.6)
        input_text_xpath(driver, 10, 'jackden1', INP_PASS)
        time.sleep(0.6)
        click_on_xpath(driver, 10, CONFIRM_KEY_BUTTON)
        time.sleep(0.6)
        # click_on_xpath(driver, 10, DETAIL_WALLET)
        # time.sleep(0.6)
        pyperclip.copy(' ')
        while len(pyperclip.paste()) < 30:
            click_on_xpath(driver, 20, COPY_KEY_BUTTON)
            time.sleep(3)
        print(f'''{num + 1}. {pyperclip.paste()}''')
        key = pyperclip.paste()
        with open('../metamask_upd/wallets.txt', 'a') as wallets:
            wallets.write(f'''\n{wallet} {key}''')
        while 1:
            try:
                click_on_xpath(driver, 10, CLOSE_BUTTON)
                break
            except:
                print(traceback.format_exc())
                time.sleep(1.1)
                continue
        resp = stop_profile(prof['user_id'])
        fix(prof['user_id'])
        time.sleep(1.2)
