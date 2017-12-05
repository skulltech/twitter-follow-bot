import csv
import random
import time
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_usernames(filename):
    usernames = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            usernames.append(row[0])
    return usernames


def login(driver, settings):
    driver.get('https://twitter.com/')
    driver.find_element_by_class_name('StreamsLogin').click()

    username = driver.find_element_by_name('session[username_or_email]')
    username.send_keys(settings['Username'])
    password = driver.find_element_by_name('session[password]')
    password.send_keys(settings['Password'])

    username.submit()


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
        filename = input('[?] The filename of the csv: ')
        try:
            usernames = read_usernames(filename)
        except FileNotFoundError:
            print('[!] File not found! Try again...')
            continue
        else:
            break

    urls = ['https://twitter.com/' + username for username in usernames]
    config_file = ConfigParser()
    config_file.read('config.ini')
    settings = config_file['SETTINGS']

    login(driver, settings)
    for username in usernames:
        print('Following user: {username}'.format(username=username))
        follow(driver, username)
        time.sleep(random.randint(int(settings['Mintime']), int(settings['Maxtime'])))


if __name__=='__main__':
    main()
