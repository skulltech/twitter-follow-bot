import csv
import random
import time
from configparser import ConfigParser
from getpass import getpass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def read_handles(filename):
    handles = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            handles.append(row[0])
    return handles


def login(driver, username, password):
    driver.get('https://twitter.com/login')

    username_element = driver.find_elements_by_name('session[username_or_email]')[0]
    username_element.send_keys(username)
    password_element = driver.find_elements_by_name('session[password]')[0]
    password_element.send_keys(password)
    username_element.submit()

    if 'Login on Twitter' in driver.title:
        return False
    else:
        return True


def follow(driver, handle):
    driver.get('https://twitter.com/' + handle)
    time.sleep(3)
    image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "https://pbs.twimg.com/profile_banners/")]')))
    user_id = image.get_attribute('src').split('/')[4]
    try:
        follow = driver.find_element_by_xpath(f'//div[@data-testid="{user_id}-follow"]')
    except NoSuchElementException:
        return
    else:
        follow.click()


def main():
    filename = input('[?] The filename of the csv: ') or 'input.csv'
    try:
        handles = read_handles(filename)
    except FileNotFoundError:
        print('[?] File not found! Try again...')
        return

    config_file = ConfigParser()
    config_file.read('config.ini')
    settings = config_file['SETTINGS']

    try:
        username = settings['Username']
    except KeyError:
        username = input('[?] Twitter Username: ')
    try:
        password = settings['Password']
    except KeyError:
        password = getpass('[?] Twitter Password for {}: '.format(settings['USERNAME']))

    driver = webdriver.Chrome()
    if not login(driver, username, password):
        print('[*] Could not login to Twitter. Check your credentials.')
        return

    for handle in handles:
        print('[*] Following user: {username}... '.format(username=handle), end='')
        follow(driver, handle)
        time.sleep(random.randint(int(settings['Mintime']), int(settings['Maxtime'])))
        print('Done!')


if __name__ == '__main__':
    main()
