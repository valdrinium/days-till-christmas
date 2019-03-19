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


def get_quotes(num=10):
    url = config('parsers.quotes.url')
    session = FuturesSession()

    futures = []
    for _ in range(num):
        futures.append(session.get(url))

    quotes = []
    for future in futures:
        result = future.result()

        regex = config('parsers.quotes.regex')
        text = result.content.decode('ISO-8859-1')

        matches = re.findall(regex, text)
        if not matches or len(matches) < 1:
            continue

        quote = strip_tags(matches[0])

        regex = config('parsers.quotes.authors.regex')

        author = re.search(regex, text)
        if author:
            author = strip_tags(author.group(1))

        quotes.append((quote, author))

    return quotes
