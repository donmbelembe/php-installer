import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyqt5", "subprocess", 'json', 'win32file'], 
    "excludes": ["tkinter"],
    "include_files": ["design.ui","logo_icon.ico","logo.png", "post-install.txt", "config.php"],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PHP installer",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])