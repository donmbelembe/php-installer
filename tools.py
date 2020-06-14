from win32file import GetLongPathName
import os
from shutil import rmtree
import subprocess
from setenv import manage_registry_env_vars
import json

if not os.path.exists("PHP/"):
    os.makedirs("PHP/")

def getPHPPackageInfoFromString(text):
    info = {
        'nts': False,
        'version': text.split("-")[1],
    }

    if 'nts' in text:
        info['nts'] = True

    return info

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
            ['php', os.path.join('config.php')],    # program and arguments
            stdout=subprocess.PIPE,  # capture stdout
            check=True               # raise exception if program fails
        )
        return json.loads(result.stdout.decode('utf-8'))
    except:
        return None
