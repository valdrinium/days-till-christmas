# Motivation

Do you also have that one friend 👪 who keeps talking about Christmas 🎅 since 
July ☃️ and sends you pictures of how many days are left till December 24th 🎄 
since November 🧦? Well then, you came to the right place 🎁 ;)

This collection of `Python` scripts is here to inspire Christmas spirit 
daily to those friends, with as little as `0 effort` from your side.

# Introduction

This collection of tiny scripts works like this:

1. Firstly, the script `download.py` downloads the next christmasy image from 
<a href="https://unsplash.com">Unsplash</a>. The `images.json` config file 
specifies which search query to perform and which image to download according 
to the current index. The index gets incremented every time the script is run, 
so it will always be a new high quality image.
![](https://raw.githubusercontent.com/valdrinium/days-till-christmas/master/sample/original.jpg)
0. Secondly, the script `edit.py` reads that image and edits it, using the 
number of days left till the date specified in the `edit.json` config file. 
In addition, you must also specify which strings to put according to which 
condition, based on the following format:
    ```
    [
        ...
        {
            "condition": "gt",
            "comparedTo": 25,
            "value": [
                "AU MAI RĂMAS DOAR",
                "  :days ZILE  ",
                "pănă la Crăciun"
            ]
        },
        ...
    ]
    ```
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
- A phone that is connected to the internet.

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

In `config/spam.json`, you can configure:

- `hidesWindow`: show/hide the Selenium window.
- `victims`: the array of contact names to be spammed, exactly as they appear in 
    WhatsApp Web.
- `spamAt`: the hour of the daily spam, in 24-hour format.

In `config/images.json`, you can configure:

- `query`: the serach query to be performed on Unsplash when looking for a new image.
- `index`: the index of the image to download from that search.
- `perPage`: this, together with the `index`, helps determine the page that the image 
    we have to download will be on.

In `config/edit.json`, you can configure:

- `targetDate`: specify the day and month (eg: `{ "day": 24, "month": 12 }`). We will 
    then compute how many days are left till that date (be it this or next year).
- `texts`: the array of objects that contain the text information neccessary to edit 
    the photo. The program will compare the number of days left till `targetDate` with 
    each object's `comparedTo` value, based on the `condition`. The texts corresponding 
    to the first condition that holds true will apper in the edited image.


## Schedule on Startup

1. Right click the `start.bat` file and create a shortcut.
0. Press `Win+R`, type `shell:startup` and paste the shortcut in the folder that just 
poped up and reboot.

# Happy spamming! xD
