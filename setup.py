import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyqt5", "subprocess", 'json', 'win32file'],
    "include_files": ["design.ui", "logo_icon.ico", "logo.png", "post-install.txt", "config.php"],
    "excludes": ["tkinter", "PyQt5.QtSql", "sqlite3",
                 "scipy.lib.lapack.flapack",
                 "PyQt5.QtNetwork",
                 "PyQt5.QtScript",
                 "numpy.core._dotblas",
                 "autopep8"],
    "optimize": 2
}

# build_msi_options = {
#     "add_to_path": False,
#     "initial_target_dir": os.environ["ProgramFiles(x86)"],
#     "install_icon": "logo_icon.ico",
# }

setup(name="PHP installer",
      version="0.1",
      description="My GUI application!",
      options={
          "build_exe": build_exe_options,
        #   "bdist_msi": build_msi_options
        },
      executables=[Executable("main.py", base="Win32GUI", targetName="php-installer.exe", icon="logo_icon.ico")])
