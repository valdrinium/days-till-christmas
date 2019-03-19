import subprocess
import os

from utils.config import config


real_dir_path = os.path.realpath(os.path.dirname(__file__))

for victim in config('spam.victims'):
    subprocess.run(['pythonw', '-B', os.path.join(real_dir_path, 'spam.py'), victim])
