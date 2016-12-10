import csv
import random
import time
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


def read_usernames(filename):
    usernames = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            usernames.append(row[0])
    return usernames


def twitter_login(driver, settings):
    driver.get('https://twitter.com/')
    login_button = driver.find_element_by_class_name('StreamsLogin')
    login_button.click()

    username = driver.find_element_by_name('session[username_or_email]')
    username.send_keys(settings['Username'])
    password = driver.find_element_by_name('session[password]')
    password.send_keys(settings['Password'])

    username.submit()


def follow_user(driver, username):
    url = 'https://twitter.com/' + username
    driver.get(url)
    follow_button = driver.find_element_by_class_name('follow-button')
    while True:
        if follow_button.text == 'Following':
            return
        elif follow_button.text == 'Follow':
            follow_button.click()

driver = webdriver.Chrome()

while True:
    filename = input('Enter the filename of the csv list [with the .csv extension]: ')
    try:
        usernames = read_usernames(filename)
    except FileNotFoundError:
        print('File not found! Try again...')
        continue
    else:
        break

urls = ['https://twitter.com/' + username for username in usernames]
config_file = ConfigParser()
config_file.read('config.ini')

settings = config_file['SETTINGS']

twitter_login(driver, settings)

for username in usernames:
    print('Following user: {username}'.format(username=username))
    follow_user(driver, username)
    time.sleep(random.randint(int(settings['Mintime']), int(settings['Maxtime'])))