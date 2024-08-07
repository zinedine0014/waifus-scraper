
import requests
import sys
import os
from termcolor import cprint
from urllib.parse import urlparse

# add "nsfw": ["waifu", "neko", "trap", "blowjob"] to the categories array and add 'nsfw' to the types array
# to be able to use the nsfw type
# thats if u want

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

def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    
    with open(filename, 'wb') as file:
        file.write(response.content)

def get_anime_girls(image_type, category, count):
    if image_type not in TYPES:
        raise ValueError(f"Invalid type. Expected one of {TYPES}")
    if category not in CATEGORIES[image_type]:
        raise ValueError(f"Invalid category for type '{image_type}'. Expected one of {CATEGORIES[image_type]}")
    
    images_url = []
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    for i in range(count):
        response = requests.get(BASE_URL.format(image_type, category))
        response.raise_for_status()
        url = response.json().get('url')
        images_url.append(url)
        filename = os.path.join(OUTPUT_FOLDER, f"{i + 1}_{os.path.basename(urlparse(url).path)}")
        print(f"[{i + 1}] {url}")
        download_image(url, filename)
    
    return images_url

def main():
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <type> <category> <count>")
        sys.exit(1)

    image_type = sys.argv[1]
    category = sys.argv[2]
    count = int(sys.argv[3])

    try:
        get_anime_girls(image_type, category, count)
    except ValueError as e:
        cprint(str(e), 'yellow')
        sys.exit(1)

if __name__ == "__main__":
    main()
