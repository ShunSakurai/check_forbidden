'''
cd dropbox/codes/check_forbidden
py -3.4 setup.py py2exe

Libraries used:
import tkinter
import tkinter.filedialog
import csv
import datetime
import os
import re
import subprocess
import sys
import time
import zipfile
import doctest
'''
import os
import shutil

dict_console = {
    'author': 'Shun Sakurai',
    'dest_base': 'Check Forbidden',
    'icon_resources': [(1, './icons/check_forbidden_icon.ico')],
    'script': 'check_forbidden.py',
    'version': '1.6.9',
}

dict_options = {
    'bundle_files': 2,
    'compressed': True,
    'excludes': [
        '_bz2', '_hashlib', '_frozen_importlib', '_lzma', '_ssl'  'argparse',
        'calendar', 'difflib', 'doctest' 'inspect', 'locale', 'optparse',
        'pdb', 'pickle', 'pydoc', 'pyexpat', 'pyreadline']
}

if __name__ == "__main__":
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    from distutils.core import setup
    import py2exe

    setup(
        console=[dict_console],
        options={'py2exe': dict_options}
    )

    shutil.rmtree('__pycache__')
    print('.exe file v' + dict_console['version'], 'created.')
