'''
cd dropbox/codes/check_forbidden
py cf_scripts.py
'''
import csv
import datetime
import os
import re
from time import sleep
import zipfile


def dir_from_path(path):
    if path:
        path = replace_back_slash(path)
        path_first = ls_from_tuple_str(path)[0]
        path_no_slash = path_first.rstrip('/')
        if '.' in path_no_slash.rsplit('/', 1)[-1]:
            path_dir = path_no_slash.rsplit('/', 1)[0]
        else:
            path_dir = path_no_slash
    else:
        path_dir = None
    return path_dir


def dirname_from_fname(fname):
    dir_name = fname.rsplit('.', 1)[0]
    return dir_name


def fname_from_path(path):
    f_name = path.rsplit('/', 1)[-1]
    return f_name


def limit_range(raw, str_rate, str_locked):
    regex_unit = re.compile('<trans-unit id=".*?</trans-unit>', re.S)
    regex_header = re.compile('<trans-unit id=".*?>')
    string_101 = 'mq:percent="101"'
    string_100 = 'mq:percent="100"'
    string_locked = 'mq:locked="locked"'
    string_to_search = []
    for unit_mo in regex_unit.finditer(raw):
        unit = unit_mo.group(0)
        header_mo = regex_header.search(unit)
        header = header_mo.group(0)
        if str_rate == '100' and string_100 in header:
            continue
        elif str_rate == '100' and string_101 in header:
            continue
        elif str_rate == '101' and string_101 in header:
            continue
        elif str_locked == 'locked' and string_locked in header:
            continue
        else:
            string_to_search.append(unit)
    return string_to_search


def ls_from_list_str(x):
    r'''
    >>> ls_from_list_str("['Index', 'Source', 'Target (NG)', 'Target (OK)']")
    ['Index', 'Source', 'Target (NG)', 'Target (OK)']
    '''
    list_from_str = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return list_from_str


def ls_from_tuple_str(x):
    r'''
    >>> ls_from_tuple_str(r'/Users/path/mqxliff.mqxliff {/Users/path/mqxlz.mqxlz}')
    ['/Users/path/mqxliff.mqxliff', '/Users/path/mqxlz.mqxlz']

    >>> ls_from_tuple_str(r' C:/Users/path/mqxliff1.mqxliff {C:/Users/path/mqxliff2.mqxliff} {C:\Users\path\mqxlz1.mqxlz} {C:\Users\path\mqxlz2.mqxlz}')
    ['C:/Users/path/mqxliff1.mqxliff', 'C:/Users/path/mqxliff2.mqxliff', 'C:\\Users\\path\\mqxlz1.mqxlz', 'C:\\Users\\path\\mqxlz2.mqxlz']
    '''
    x_split = x.replace('{', ',').strip('(),').split(',')
    list_from_str = [i.strip(' {},"\'') for i in x_split]
    return list_from_str


def mqxlz_dir_fname(fn):
    path_extract = dirname_from_fname(fn) + '_extract'
    fn_actual = zipfile.ZipFile(fn).extract('document.mqxliff', path=path_extract)
    return path_extract, fn_actual


def print_and_append(str_method, to_print, to_write, file_to_write_in):
    print(to_print)
    if str_method == '0':
        file_to_write_in.append(to_write)
    else:
        pass


def remove_tags(segment):
    regex_tag = re.compile('<.*?>.*?</.*?>', re.S)
    segment_clean = regex_tag.sub('', segment)
    return segment_clean


def replace_back_slash(path):
    path.replace('\\', '/')
    return path


def return_col_num(row):
    if len(row) >= 3:
        col_to_check = 2
    else:
        col_to_check = 0
    return col_to_check


def str_from_settings(str_rate, str_locked):
    if str_rate == 'all':
        setting_rate = 'Check all match rates'
    elif str_rate == '101':
        setting_rate = r'Exclude 101% matches'
    elif str_rate == '100':
        setting_rate = r'Exclude 100% / 101%'
    if str_locked == 'all':
        setting_locked = 'Include locked segments'
    else:
        setting_locked = 'Exclude locked segments'
    settings = setting_rate + ', ' + setting_locked
    return settings


def try_rmdir(i):
    try:
        os.rmdir(i)
    except:
        try:
            sleep(0.01)
            os.rmdir(i)
        except:
            print('Please go to the bilingual file location and delete the _extract folder manually.')


def check_forbidden_terms(frame, str_bl, str_terms, str_result, str_method, str_rate, str_locked):
    fn_bl_list = ls_from_tuple_str(str_bl)
    fn_terms = replace_back_slash(str_terms)
    fn_result = replace_back_slash(str_result)
    f_terms = open(fn_terms, encoding='utf-8')
    f_result_w = []
    list_mqxlz_dir = []
    list_found_rows = []
    regex_pattern = re.compile('<target xml:space="preserve">.*?</target>', re.S)

    print('-' * 70)
    date_and_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    list_name = fname_from_path(fn_terms)
    settings = str_from_settings(str_rate, str_locked)
    print_and_append(str_method, date_and_time, [date_and_time], f_result_w)
    print_and_append(str_method, list_name, [list_name], f_result_w)
    print_and_append(str_method, settings, [settings], f_result_w)
    print('-' * 70)

    for fn_bl in fn_bl_list:
        if fn_bl[-5:] == 'mqxlz':
            list_mqxlz_dir.append(mqxlz_dir_fname(fn_bl)[0])
            fn_bl_actual = mqxlz_dir_fname(fn_bl)[1]
        else:
            fn_bl_actual = fn_bl

        fn_bl_actual = replace_back_slash(fn_bl_actual)
        f_bl = open(fn_bl_actual, encoding='utf-8')
        f_bl_r_raw = f_bl.read()
        f_bl_r_limit_list = limit_range(f_bl_r_raw, str_rate, str_locked)
        f_bl_r_with_tag = [regex_pattern.findall(i)[0][29:-9] for i in f_bl_r_limit_list]
        f_bl_r = [remove_tags(i) for i in f_bl_r_with_tag]
        print_and_append(str_method, fn_bl, [fn_bl], f_result_w)

        f_terms.seek(0)
        f_terms_r = csv.reader(f_terms)
        for row in f_terms_r:
            if len(row) == 0:
                continue
            else:
                col_to_check = return_col_num(row)
            if row[col_to_check] is None:
                continue
            for line in f_bl_r:
                if re.search(row[col_to_check], line) is not None:
                    print_and_append(str_method, row, row, f_result_w)
                    list_found_rows.append(row)
                else:
                    continue

        f_bl.close()

    f_terms.close()

    if list_mqxlz_dir:
        for i in list_mqxlz_dir:
            os.remove(i + r'/document.mqxliff')
        for i in list_mqxlz_dir:
            try_rmdir(i)

    if list_found_rows:
        print_and_append(str_method, '\n' + 'Summary', ['Summary'], f_result_w)
        list_reduced = list({str(i) for i in list_found_rows})
        for i in list_reduced:
            print_and_append(str_method, i, ls_from_list_str(i), f_result_w)
        print_and_append(str_method, '', [''], f_result_w)
    else:
        print('No forbidden term was found!')

    if list_found_rows and str_method == '0':
        f_result = open(fn_result, 'a', encoding='utf-8')
        f_result_wc = csv.writer(f_result, lineterminator='\n')
        f_result_wc.writerows(f_result_w)
        f_result.close()
        print(fname_from_path(fn_result) + ' was successfully created.')

    if list_found_rows and str_method == '1':
        print('The search was successfully finished.')

    print('Click [x] on the tk window or press [Enter] on this screen to exit.')
    try:
        input('\n')
    except:
        pass

    frame.quit()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
