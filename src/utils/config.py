import os
import json


def load_config(config_path):
    config = {}
    for file in os.listdir(config_path):
        with open(os.path.join(config_path, file), 'rb') as f:
            config[os.path.splitext(file)[0]] = json.load(f)

    return config 


def find_config(filename='config', raise_error_if_not_found=True):
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


config_path = find_config()
config_data = load_config(config_path)


def config(path, value=None):
    words = path.split('.');
    if len(words) < 0:
        return None

    result = config_data[words[0]]
    if value is None:
        for word in words[1:]:
            result = result[word]

        return result
    else:
        for word in words[1:-1]:
            result = result[word]
        result[words[-1]] = value

        with open(os.path.join(config_path, words[0] + '.json'), 'w') as f:
            json.dump(config_data[words[0]], f, indent=4)

        return True
