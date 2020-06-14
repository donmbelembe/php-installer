# from requests import get as requests_get
from bs4 import BeautifulSoup
from packaging.version import Version, parse
from win32file import GetLongPathName
import os
from zipfile import ZipFile
from shutil import copyfile, rmtree
import subprocess
from setenv import manage_registry_env_vars
import json

if not os.path.exists("PHP/"):
    os.makedirs("PHP/")

installDir = "PHP"
installedPHP = list(filter(lambda x: os.path.isdir(os.path.join(installDir, x)), os.listdir(installDir)))


def extractLinks(HTML):
    soup = BeautifulSoup(HTML, 'html.parser')

    links = soup.find_all('a')
    links = [link.get('href').split('/')[-1] for link in links]
    return links

def filterWindowsItems(data):
    data = [d for d in data if "Win" in d and d.endswith(".zip")]
    # remove .zip at the end     
    data = [d[:-4] for d in data]
    # transform to list of name, version
    newList = list()
    for i, d in enumerate(data):
        newList.append((d, d.split("-")[1]))
    # only keep those who have valid version
    newList = [i for i in newList if isinstance(parse(i[1]), Version)]
    # add minor version
    for i, d in enumerate(newList):
        newList[i] = d[0], d[1], "{}.{}".format(parse(d[1]).major,parse(d[1]).minor)
    return newList

def groupByMinorRelease(data, patch=True):
    # group by minor version
    Output = {} 
    for x, y, z in data: 
        if z in Output: 
            if patch:
                if parse(y) == parse(Output[z][0][1]):
                    Output[z].append((x, y)) 
                elif parse(y) > parse(Output[z][0][1]):
                    Output[z] = [(x, y)]
            else:
                Output[z].append((x, y)) 
        else: 
            Output[z] = [(x, y)]
    return Output

def clearData(data, latestPath = True):
    links = filterWindowsItems(data)
    links = groupByMinorRelease(links, latestPath) 
    return links

def getPHPPackageInfoFromString(text):
    info = {
        'nts': False
    }

    if 'nts' in text:
        info['nts'] = True

    return info

def saveFile(data, name):
    path = 'PHP/' + name
    with open(path + '.zip', 'wb') as f:
        for chunk in data:
            # print('Writing chunk') # Uncomment this to show that the file is being written chunk-by-chunk when parts of the data is received
            f.write(chunk) # Write each chunk received to a file
        # f.write(r.content)
    with ZipFile(path + '.zip', 'r') as zip_ref:
        zip_ref.extractall(path)

    os.remove(path + '.zip')
    copyfile(path + '/php.ini-development', path + '/php.ini')

def remove(name):
    path = 'PHP/' + name
    rmtree(path)

def removePathItem(path, item):
    indexFound = 0
    for i, p in enumerate(path, 1):
        try:
            p1 = os.path.normcase(GetLongPathName(r'{}'.format(p))).rstrip('\\')
            if p1 == item: 
                indexFound = i
                break
        except:
            pass
    if indexFound:
        del path[indexFound-1]
        # try again
        removePathItem(path, item)
    return path

def cleanPath():
    result = subprocess.run(['where', 'php'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    if result:
        installedPath = result.splitlines()
        for i, p in enumerate(installedPath):
            p = os.path.normcase(p.strip()[:-7]).rstrip('\\')

            path = manage_registry_env_vars('PATH')['value'].split(';')
            NEW_PATH = ';'.join(removePathItem(path, p))
            manage_registry_env_vars('PATH', NEW_PATH)

def currentConfig():
    try:
        result = subprocess.run(
            ['php', 'phpinfo.php'],    # program and arguments
            stdout=subprocess.PIPE,  # capture stdout
            check=True               # raise exception if program fails
        )
        return json.loads(result.stdout.decode('utf-8'))
    except:
        return None

