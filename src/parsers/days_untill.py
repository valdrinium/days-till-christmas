from src.utils.config import config
import os
import sys
import re

from requests_futures.sessions import FuturesSession
from html.parser import HTMLParser

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    stripper = MLStripper()
    stripper.feed(html)

    return stripper.get_data()


def get_days_untill(event):
    url = config('parsers.days_untill.url') + event
    future = FuturesSession().get(url)
    result = future.result()

    regex = config('parsers.days_untill.regex')
    text = result.content.decode('ISO-8859-1')
    matches = re.findall(regex, text.replace('\r\n', ''))

    if not matches or len(matches) != 1:
        return None

    sentence = strip_tags(matches[0]).strip()
    numbers = [int(s) for s in sentence.split() if s.isdigit()]

    if not numbers or len(numbers) != 1:
        return None

    return numbers[0]
