import csv
import random
import time
from configparser import ConfigParser
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException



def read_usernames(filename):
    usernames = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            usernames.append(row[0])
    return usernames


def login(driver, settings):
    driver.get('https://twitter.com/login')

    login_forms = driver.find_elements_by_name('session[username_or_email]')
    for idx, username in enumerate(login_forms):
        try:
            username.send_keys(settings['Username'])
        except ElementNotVisibleException:
            continue
        else:
            password = driver.find_elements_by_name('session[password]')[idx]
            password.send_keys(settings['Password'])
            username.submit()
            break

    if 'Login on Twitter' in driver.title:
        return False
    else:
        return True


def follow(driver, username):
    driver.get('https://twitter.com/' + username)
    wait = WebDriverWait(driver, 10)
    follow = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'follow-button')))
    
    if 'Following' in follow.text:
        return
    elif 'Follow' in follow.text:
        follow.click()


def main():
    driver = webdriver.Chrome()

    while True:
        filename = input('[*] The filename of the csv: ') or 'input.csv'
        try:
            usernames = read_usernames(filename)
        except FileNotFoundError:
            print('[*] File not found! Try again...')
            continue
        else:
            break

    urls = ['https://twitter.com/' + username for username in usernames]
    config_file = ConfigParser()
    config_file.read('config.ini')
    settings = config_file['SETTINGS']

    try:
        settings['USERNAME']
    except KeyError:
        settings['USERNAME'] = input('[*] Twitter Username: ')
    try:
        settings['PASSWORD']
    except KeyError:
        settings['PASSWORD'] = getpass('[*] Twitter Password for {}: '.format(settings['USERNAME']))

    if not login(driver, settings):
        print('[*] Could not login to Twitter. Check your credentials.')
        return

    first = True
    for username in usernames:
        if not first:
            time.sleep(random.randint(int(settings['Mintime']), int(settings['Maxtime'])))
        else:
            first = False

        print('[*] Following user: {username}... '.format(username=username), end='')
        follow(driver, username)
        print('Done!')
        

if __name__=='__main__':
    main()
