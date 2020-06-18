import os
from shutil import rmtree
import subprocess
import json

install_dir = 'PHP'
log_file = os.path.join('log.txt')

if not os.path.exists(install_dir):
    os.makedirs(install_dir)
    os.chmod(install_dir, 0o777)

if not os.path.exists(log_file):
    with os.fdopen(os.open(log_file, os.O_WRONLY | os.O_CREAT, 0o777), 'w') as f:
        f.write('...')

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
