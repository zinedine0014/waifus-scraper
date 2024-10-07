import requests
import sys
import os
from termcolor import cprint
from urllib.parse import urlparse
import time


TYPES = ['sfw']
CATEGORIES = {
    "sfw": [
        "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss",
        "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold",
        "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"
    ]
}


BASE_URL = 'https://api.waifu.pics/{}/{}'
OUTPUT_FOLDER = 'waifus'

# saves the image into the file-system
def download_image(url:str, filename:str):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)

# fetch's pictures from the api and download them
def get_anime_girls(image_type:str, category:str, count:int, output_folder:str):
    if image_type not in TYPES:
        raise ValueError(f"Invalid type. Expected one of {TYPES}")
    if category not in CATEGORIES[image_type]:
        raise ValueError(f"Invalid category for type '{image_type}'. Expected one of {CATEGORIES[image_type]}")
    if count <= 0:
        raise ValueError("Count must be a positive integer")

    os.makedirs(output_folder, exist_ok=True) # create the output directory if it does't exist

    for i in range(count):
        # get a random picture from the api
        response = requests.get(BASE_URL.format(image_type, category))
        response.raise_for_status()

        # Check for the 'url' in response
        data = response.json()
        if 'url' not in data:
            cprint(f"API error: No URL found in response {i + 1}", 'red')
            continue

        url = data['url'] # get the url of the picture
        filename = os.path.join(output_folder, f"{i + 1}_{int(time.time())}_{os.path.basename(urlparse(url).path)}")
        print(f"[{i + 1}] {url}")
        download_image(url, filename) # save the picture


def main():
    if len(sys.argv) != 5:
        print(f"Usage: python {sys.argv[0]} <type> <category> <count> <output_directory>")
        sys.exit(1)

    image_type = sys.argv[1]
    category = sys.argv[2]
    count = int(sys.argv[3])
    output_directory = sys.argv[4]

    try:
        get_anime_girls(image_type, category, count, output_directory)
    except ValueError as error:
        cprint(error, 'red')
        sys.exit(1)

if __name__ == "__main__":
    main()
