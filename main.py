from tools import *

URL = 'https://windows.php.net/downloads/releases/archives/'


links = extractLinks(URL)
releases = clearData(links)
print(releases)

