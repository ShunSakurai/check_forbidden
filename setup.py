from distutils.core import setup
import py2exe

setup(
      console=[{'script': 'check_forbidden.py', 'version': '1.3.0', }],
      options={'py2exe': {'bundle_files': 2}}
      )

'''
cd dropbox/codes/check_forbidden
py -3.4 setup.py py2exe
'''
