import wikipedia
import requests
import shutil
from bs4 import BeautifulSoup
from PIL import Image 
from io import BytesIO

title = input("What do you want to look up?: ")
print(wikipedia.WikipediaPage(title).summary)

my_url = (wikipedia.page(title).images[0])
response = requests.get(my_url, stream=True)
with open('my_image.png', 'wb') as file:
    shutil.copyfileobj(response.raw, file)
del response

img = Image.open('my_image.png')
img.show()