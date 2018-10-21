'''
cd dropbox/codes/check_forbidden
cd Test
py -B semi-automated_test.py
cd ../
'''
import os
import os.path
import sys
upper_dir = os.path.dirname(os.getcwd())
sys.path.append(upper_dir)
os.chdir(upper_dir)

import check_forbidden
import cf_scripts

dict_options = cf_scripts.default_dict_options
dict_options['bool_export'] = False

check_forbidden.main(
    str_tuple_bl='{./check_forbidden.wiki/README.md_jpn.mqxlz} {./check_forbidden.wiki/README.md_jpn2.mqxlz}',
    str_tuple_terms='{./check_forbidden.wiki/forbidden_terms.csv} {./check_forbidden.wiki/forbidden_terms2.csv}',
    str_result='./check_forbidden.wiki/result.html',
    dict_options=dict_options
)
