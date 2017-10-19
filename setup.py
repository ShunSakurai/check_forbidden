'''
cd /d z:
cd dropbox/codes/check_forbidden
py -B setup.py
'''

# Verpatch is needed to supplement PyInstaller's Python 3 version info bug
# Dictionary names and keys are taken from py2exe settings

dict_console = {
    'author': 'Shun Sakurai',
    'dest_base': 'Check Forbidden',
    'icon_resources': [(1, './icons/check_forbidden_icon.ico')],
    'script': 'check_forbidden.py',
    'version': '2.1.1'
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


folder_dist = 'dist'

list_excluded = []
for lib in dict_options['excludes']:
    list_excluded.append('--exclude-module')
    list_excluded.append(lib)

list_pyinstaller = [
    'pyinstaller', '--onefile',
    '--icon', dict_console['icon_resources'][0][1],
    '--name', dict_console['dest_base']
] + list_excluded + [dict_console['script']]
list_verpatch = [
    'verpatch', ''.join([folder_dist, '/', dict_console['dest_base'], '.exe']),
    zero_pad(dict_console['version']),
    '/va', '/pv', zero_pad(dict_console['version']),
    '/s', 'copyright', '©2016-2017 ' + dict_console['author']
]
list_iscc = ['C:\Program Files (x86)\Inno Setup 5\iscc', 'setup_installer.iss']

if __name__ == "__main__":
    import os
    import shutil
    import subprocess

    if os.path.exists(folder_dist):
        shutil.rmtree(folder_dist)

    print_with_border('Running PyInstaller')
    subprocess.run(list_pyinstaller)
    print_with_border('Running Verpatch')
    subprocess.run(list_verpatch)
    print_with_border('Running Inno Setup')
    subprocess.run(list_iscc)

    print_with_border('Cleaning')
    shutil.rmtree('__pycache__')
    shutil.rmtree('build')
    os.remove(''.join([dict_console['dest_base'], '.spec']))

    print('Executable and installer for v' + dict_console['version'], 'created.')
