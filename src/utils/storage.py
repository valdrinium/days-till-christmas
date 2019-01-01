import os

from urllib.parse import urlparse
from urllib.request import urlretrieve


def find_storage(filename='storage', raise_error_if_not_found=True):
    for dirname in walk_to_root(os.path.realpath(__file__)):
        check_path = os.path.join(dirname, filename)
        if os.path.isdir(check_path):
            return check_path

    if raise_error_if_not_found:
        raise IOError('Config not found')

    return None


def walk_to_root(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir

        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


storage_path = find_storage()


def download(path, filename):
    if is_url(path):
        filesystem_path =  os.path.join(storage_path, filename)
        os.makedirs(os.path.dirname(filesystem_path), exist_ok=True)

        urlretrieve(path, filesystem_path)

        return True

    return False


def is_url(path):
    try:
        result = urlparse(path)

        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def path_to(filename):
    return os.path.join(storage_path, filename)
