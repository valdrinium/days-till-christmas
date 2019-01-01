# Introduction

This collection of tiny scripts works like this:
1. Firstly, the script `download.py` downloads the next christmasy image from 
<a href="https://unsplash.com">Unsplash</a>. The `images.json` config file 
specifies which search query to perform and which image to download from the 
list, according to the current index. The index gets incremented every time 
the script is run, so it will always be a new high quality image.
![](https://raw.githubusercontent.com/valdrinium/days-till-christmas/master/sample/original.jpg)
0. Secondly, the script `edit.py` reads that image and edits it, using the 
number of days left till Christmas, as given by https://days.to/until/christmas.
The result will look similar to this (Romanian text):
![](https://raw.githubusercontent.com/valdrinium/days-till-christmas/master/sample/edited.png)
0. Thirdly, the script `spam.py` takes a contact name as an argument and sends 
to it the previously edited image using WhatsApp Web in Selenium.
0. Lastly, the script `repeat.py` schedules the downloading, editing and 
sending of a new image daily, at the time and to the contacts specified in 
the `spam.json` config file.

# Requirements

- `Python 3.7` with the following packages:
    - `Pillow`
    - `selenium`
    - `requests`
    - `schedule`
    - `python-dotenv`
    - `requests_futures`
- `Google Chrome` & `Chrome Selenium Webdriver`
    - `chromedriver` downloadable from http://chromedriver.chromium.org/downloads
- A phone that is permanently connected to the internet.

# Setup

## Env

1. Rename `.env.example` to `.env`.
0. Go to https://unsplash.com/documentation#creating-a-developer-account and set up an 
application. Make sure to check the `read_photos` permission. You will need to create a 
permanent access token for `UNSPLASH_API_ACCESS_TOKEN`.
0. Copy the full path to the selenium webdriver into `CHROMEDRIVER_PATH`.
0. Login into https://web.whatsapp.com and copy the following 4 `localStorage` variables 
to `.env`: `WABrowserId`, `WAToken1`, `WAToken2`, `WASecretBundle`. Make sure to put them 
in between `''`, for example: `'"WABrowserId"'`, or `'{"secret": "bundle"}'`.

## Config

1. In `config/spam.json`, change the array of victims to match the exact name of your 
contacts, or the time of the automated spam.
0. In `config/images.json`, change the index to match the index of the photo you wish 
to download, or the query in order to search for something else.

## Schedule on Startup

1. Right click the `start.bat` file and create a shortcut.
0. Press `Win+R`, type `shell:startup` and paste the shortcut in the folder that just 
poped up and reboot.

# Happy spamming! xD
