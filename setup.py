'''
cd dropbox/codes/check_forbidden
py -3.4 setup.py py2exe

Libraries used:
import tkinter
import tkinter.filedialog
import csv
import os
import re
from time import sleep
import zipfile
'''
from distutils.core import setup
import py2exe

setup(
      console=[{'author': 'Shun Sakurai',
                       'dest_base': 'Check Forbidden',
                       'script': 'check_forbidden.py',
                       'version': '1.4.0',
                       }],
      options={'py2exe': {
                     'bundle_files': 2,
                     'compressed': True,
                     'excludes': ['_hashlib', '_frozen_importlib', 'argparse', '_lzma', '_bz2', '_ssl', 'calendar', 'datetime', 'difflib', 'doctest', 'inspect', 'locale', 'optparse', 'pdb', 'pickle', 'pydoc', 'pyexpat', 'pyreadline'],
                     }}
     )
