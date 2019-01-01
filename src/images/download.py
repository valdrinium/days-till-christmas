import os
import sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.env import env
from src.utils.config import config
from src.utils.storage import download

base_url = env('UNSPLASH_API_BASE_URL')
access_token = env('UNSPLASH_API_ACCESS_TOKEN')
authorization_header = {'Authorization': 'Bearer ' + access_token}

try:
    query = config('images.query')
    image_index = config('images.index')
    images_per_page = config('images.perPage')

    page = 1 + int(image_index / images_per_page)
    response = requests.get(base_url + '/search/photos' + 
        f'?query={query}&page={page}', headers=authorization_header)

    response_data = response.json()
    response_image = response_data['results'][image_index % images_per_page]

    download(response_image['urls']['regular'], os.path.join('images', 'original.jpg'))

    config('images.index', image_index + 1)
except:
    print('Cannot download today\'s image from Unsplash :(')
