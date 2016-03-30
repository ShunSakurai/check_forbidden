from distutils.core import setup
import py2exe

setup(
      console=[{'script':'check_forbidden.py','version':'1.1.0',}],
      )

'''
go to the location and
py -3.4 setup.py py2exe
'''
