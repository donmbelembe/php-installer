import os
from shutil import rmtree
import subprocess
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
