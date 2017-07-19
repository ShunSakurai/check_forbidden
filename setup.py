'''
cd /d z:
cd dropbox/codes/check_forbidden
py -B setup.py
'''

# Installing PyInstaller that supports Python 3.6
'''
git clone https://github.com/pyinstaller/pyinstaller.git
cd pyinstaller
py setup.py install
'''
# Verpatch is needed to supplement PyInstaller's bug for version info in Python 3
# Dictionary names and keys taken from py2exe settings

dict_console = {
    'author': 'Shun Sakurai',
    'dest_base': 'Check Forbidden',
    'icon_resources': [(1, './icons/check_forbidden_icon.ico')],
    'version': '1.9.11'
}

dict_options = {
    'excludes': [
        '_bz2', '_frozen_importlib', '_lzma', 'argparse',
        'pdb', 'pydoc', 'pyexpat', 'pyreadline']
}


def print_with_border(message):
    border = '='
    length = 20
    print(border * length, message, border * length)


def zero_pad(str_ver):
    list_ver = str_ver.split('.')
    str_ver2 = str_ver + '.0' * (4 - len(list_ver))
    return str_ver2


list_excluded = []
for lib in dict_options['excludes']:
    list_excluded.append('--exclude-module')
    list_excluded.append(lib)

list_pyinstaller = [
    'pyinstaller', '--onefile',
    '--icon', './icons/check_forbidden_icon.ico',
    '--name', 'Check Forbidden'
] + list_excluded + ['check_forbidden.py']
list_verpatch = [
    'verpatch', 'dist/Check Forbidden.exe', zero_pad(dict_console['version']),
    '/va', '/pv', zero_pad(dict_console['version']),
    '/s', 'copyright', '©2016-2017 ' + dict_console['author']
]
list_iscc = ['C:\Program Files (x86)\Inno Setup 5\iscc', 'setup_installer.iss']

if __name__ == "__main__":
    import os
    import shutil
    import subprocess

    if os.path.exists('dist'):
        shutil.rmtree('dist')

    print_with_border('Running PyInstaller')
    subprocess.run(list_pyinstaller)
    print_with_border('Running Verpatch')
    subprocess.run(list_verpatch)
    print_with_border('Running Inno Setup')
    subprocess.run(list_iscc)

    print_with_border('Cleaning')
    shutil.rmtree('__pycache__')
    shutil.rmtree('build')
    os.remove('Check Forbidden.spec')

    print('Executable and installer for v' + dict_console['version'], 'created.')
