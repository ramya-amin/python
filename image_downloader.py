import os
import requests
from bs4 import BeautifulSoup

# This code will download the specified word related image with specific number 

google_image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

# Creates a folder named "images" in the current directory of this script
SAVE_FOLDER = 'images'


def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()


def download_images():
    data = input('What are you looking for? ')
    n_images = int(input('How many images do you want download? '))

    print('Start searching.....')
    searchurl = google_image + 'q=' + data

    # request url, without usr_agent, the permission gets denied
    response = requests.get(searchurl, headers=usr_agent)

    # find all divs where class='rg_meta'
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.findAll('img', {'class': 'rg_i Q4LuWd'})

    # gathering requested number of list of image links with data-src attribute
    # continue the loop in case query fails for non-data-src attributes
    count = 0
    links = []
    for res in results:
        try:
            link = res['data-src']
            links.append(link)
            count += 1
            if (count >= n_images): break

        except KeyError:
            continue

    print(f'Downloading {len(links)} images....')

    # Access the data URI and download the image to a file
    for i, link in enumerate(links):
        response = requests.get(link)

        image_name = SAVE_FOLDER + '/' + data + str(i + 1) + '.jpg'
        with open(image_name, 'wb') as fh:
            fh.write(response.content)


if __name__ == '__main__':
    main()
