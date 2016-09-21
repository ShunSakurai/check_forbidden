'''
cd dropbox/codes/check_forbidden/Test
py -B semi-automated_test.py
'''
import os
import os.path
import sys
upper_dir = os.path.dirname(os.getcwd())
sys.path.append(upper_dir)
os.chdir(upper_dir)

import cf_scripts

cf_scripts.check_forbidden_terms(
    frame=None, tuple_str_bl='./check_forbidden.wiki/README.md_jpn.mqxlz',
    tuple_str_terms='./check_forbidden.wiki/forbidden_terms.csv', str_result='',
    str_function='0', str_method='1', str_rate='all', str_locked='all'
)
