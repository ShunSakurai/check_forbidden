'''
cd dropbox/codes/check_forbidden
py -3.4 setup.py py2exe

rmdir /s __pycache__
rmdir /s dist

Libraries used:
import tkinter
import tkinter.filedialog
import csv
import datetime
import os
import re
from time import sleep
import zipfile
import doctest
'''
from distutils.core import setup
import py2exe

setup(
    console=[{
        'author': 'Shun Sakurai',
        'dest_base': 'Check Forbidden',
        'icon_resources': [(1, './icons/check_forbidden_icon.ico')],
        'script': 'check_forbidden.py',
        'version': '1.5.6',
    }],
    options={'py2exe': {
        'bundle_files': 2,
        'compressed': True,
        'excludes': ['_bz2', '_hashlib', '_frozen_importlib', '_lzma', '_ssl'  'argparse', 'calendar', 'difflib', 'doctest' 'inspect', 'locale', 'optparse', 'pdb', 'pickle', 'pydoc', 'pyexpat', 'pyreadline'],
    }}
)
