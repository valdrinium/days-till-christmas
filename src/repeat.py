import subprocess
import schedule
import time
import os

from utils.config import config


def spam(arg):
    real_dir_path = os.path.realpath(os.path.dirname(__file__))

    subprocess.run(['python', '-B', os.path.join(real_dir_path, 'images', 'download.py')])
    subprocess.run(['python', '-B', os.path.join(real_dir_path, 'images', 'edit.py')])
    for victim in config('spam.victims'):
        subprocess.run(['python', '-B', os.path.join(real_dir_path, 'spam.py'), victim])


schedule.every().day.at(config('spam.spamAt')).do(spam, 'Let there be Christmas')

while True:
    schedule.run_pending()
    time.sleep(30)
