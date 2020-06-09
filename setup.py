# import sys, os, shutil
# from cx_Freeze import setup, Executable

# # work around https://github.com/anthony-tuininga/cx_Freeze/issues/331#issuecomment-479371469
# if not os.path.exists(os.path.join(sys.base_prefix,"DLLs")) and hasattr(sys,"real_prefix"):
#     shutil.copytree(os.path.join(sys.real_prefix,"DLLs"), os.path.join(sys.base_prefix,"DLLs"))

# # Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {
#     "include_files": ["LICENSE","logo_icon.ico","logo.png"],
#     "optimize": 2,
# }

# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# setup(  name = "php-windows-installer",
#         version = "0.1",
#         description = "Manage PHP instalation on windows",
#         options = {"build_exe": build_exe_options},
#         executables = [Executable("main.py", base=base)])

from cx_Freeze import setup, Executable
import subprocess
import sys


NAME = 'PHP_Windows_Installer'
VERSION = '1.0'
# PACKAGES = ['pygame', ('import_name', 'package_name')]
PACKAGES = [
    'pandas', 'numpy',
    'idna', 'requests', 'urllib3', 'queue', 'chardet', 'certifi'
]
# if names are same just have a string not a tuple
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
installed_packages = installed_packages.split('\r\n')
EXCLUDES = {pkg.split('==')[0] for pkg in installed_packages if pkg != ''}
EXCLUDES.add('tkinter')
for pkg in PACKAGES:
    if pkg in EXCLUDES:
        if type(pkg) == str: 
            EXCLUDES.remove(pkg)
        else: EXCLUDES.remove(pkg[1])


executables = [Executable('main.py', base='Win32GUI', icon='logo_icon.ico', targetName=NAME)]

pkgs = []
for i, pkg in enumerate(PACKAGES):
    if type(pkg == str):
        pkgs.append(pkg)
    else:
        pkgs.append(PACKAGES[0])

setup(
    name=NAME,
    version=VERSION,
    description=f'{NAME} Copyright 2019 on mbelembe',
    options={'build_exe': {'packages': pkgs,
                           'include_files': ["LICENSE","logo_icon.ico","logo.png"],
                           'excludes': EXCLUDES,
                           'optimize': 2}},
    executables=executables)