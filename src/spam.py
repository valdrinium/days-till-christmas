#coding=utf-8
import os

from time import sleep
from random import randint
from argparse import ArgumentParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from storage import LocalStorage
from utils.env import env
from utils.config import config
from utils.storage import path_to

# Instantiate the parser
parser = ArgumentParser(description='Just tell me who you want to spam')
parser.add_argument('target')
args = parser.parse_args()

# Create the Chrome Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome(env('CHROMEDRIVER_PATH'), options=options)

# Access WhatsApp Web for the first time to configure the storage
driver.get(env('WHATSAPP_WEB_URL'))

# Set the application storage key-value pairs from env
storage = LocalStorage(driver)
storage.set('WABrowserId', env('WHATSAPP_WEB_BROWSER_ID'))
storage.set('WAToken1', env('WHATSAPP_WEB_TOKEN_1'))
storage.set('WAToken2', env('WHATSAPP_WEB_TOKEN_2'))
storage.set('WASecretBundle', env('WHATSAPP_WEB_SECRET_BUNDLE'))

# It's a kind of magic, magic ...
driver.refresh()

# Note that the content in the site is genertated dynamically by the JS engine
wait = WebDriverWait(driver, randint(60, 180) * 1000)

# Waits for the desired contact to load and selects it
targetXpath = '//span[contains(@title,"' + args.target + '")]'
targetContact = wait.until(EC.presence_of_element_located((By.XPATH, targetXpath)))

sleep(randint(2, 4))
targetContact.click()

# Specifies the location of the attach button in the page
attachXpath = '//div[@role="button"][@title="Attach"]'
attachButton = wait.until(EC.presence_of_element_located((By.XPATH, attachXpath)))

sleep(randint(2, 4))
attachButton.click()

# Specifies the location of the image input field in the page
inputXpath = '//input[@type="file"][@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
imageInput = wait.until(EC.presence_of_element_located((By.XPATH, inputXpath)))

sleep(randint(2, 4))
imageInput.send_keys(path_to(os.path.join('images', 'today.png')))

# Debugging
# sleep(randint(2, 4))
# driver.get_screenshot_as_file("capture.png")

# Specifies the location of the send button in the page
sendXpath = '//div[@role="button" and descendant::span[@data-icon="send-light"]]'
sendButton = wait.until(EC.presence_of_element_located((By.XPATH, sendXpath)))

sleep(randint(2, 4))
sendButton.click()

# Bye-bye
sleep(randint(60, 180))
driver.quit()
