from distutils.core import setup
import py2exe

setup(
      console=[{'script':'check_forbidden.py','version':'1.1.0',}],
      )

'''
cd dropbox/codes/check_forbidden
py -3.4 setup.py py2exe
'''
