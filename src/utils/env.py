import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))


def env(variable):
    return os.getenv(variable)
