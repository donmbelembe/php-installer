import requests
from bs4 import BeautifulSoup
import re
from utils import *

URL = 'https://windows.php.net/downloads/releases/archives/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a')

print(parsePHPVersions(links))