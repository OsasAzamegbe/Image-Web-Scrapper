import requests
import sys
import os
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image


def image_scrapper(user_search):
# search for the images on bing.com

    params = {"q": user_search}
    r = requests.get("https://www.bing.com/images/search", params=params)

    # create the name of the folder directory
    dir_name = user_search

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    # Parse through the html for the search page to get the image href
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.findAll("a", {"class": "thumb"}) 
  

    for item in links:
        # use requests to get the binary data from the image href and get the image name
        img_href = item.attrs["href"]
        img_request = requests.get(img_href)
        img_title = img_href.split('/')[-1].split(".")[0]

        #convert the binary data to an image and store it in an image file with the appropriate image type
        #use os to create a directory for the images and save then
        print("Getting:", img_href)
        
        try:
            img = Image.open(BytesIO(img_request.content))
            img.save('./'+ dir_name + '/' + img_title + '.' + img.format.lower(), img.format)
        except IOError:
            print("Cannot save image...")
        
    if not links:
        image_scrapper(user_search)
    else:
        sys.exit(0)


search = input("what images do you need? ")
image_scrapper(search)