import csv
import os
import re
from time import sleep
import zipfile


def mqxlz_dir_fname(fn):
    path_extract = fn.rsplit(r'.', 1)[0] + '_extract'
    fn_actual = zipfile.ZipFile(fn).extract('document.mqxliff', path=path_extract)
    return path_extract, fn_actual


def limit_range(raw, str_rate, str_locked):
    regex_unit = re.compile('<trans-unit id=".*?</trans-unit>', re.S)
    units = regex_unit.findall(raw)
    regex_header = re.compile('<trans-unit id=".*?>')
    string_101 = 'mq:percent="101"'
    string_100 = 'mq:percent="100"'
    string_locked = 'mq:locked="locked"'
    string_to_search = []
    for unit in units:
        header = regex_header.findall(unit)[0]
        if str_rate == '100' and header.find(string_100) != -1:
            continue
        elif str_rate == '100' and header.find(string_101) != -1:
            continue
        elif str_rate == '101' and header.find(string_101) != -1:
            continue
        elif str_locked == 'locked' and header.find(string_locked) != -1:
            continue
        else:
            string_to_search.append(unit)
    return string_to_search


def print_and_append(to_print, to_write, file_to_write_in):
    file_to_write_in.append(to_write)
    print(to_print)


def return_col_num(row):
    if len(row) >= 3:
        col_to_check = 2
    else:
        col_to_check = 0
    return col_to_check


def try_to_rmdir(i):
    try:
        os.rmdir(i)
    except:
        try:
            sleep(0.01)
            os.rmdir(i)
        except:
            print('Please go to the bilingual file location and delete the _extract folder manually.')


def list_str_to_list(x):
    list_from_str = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return list_from_str


def tuple_str_to_ls(x):
    list_from_str = [i.strip().strip(', ').strip('"').strip("'") for i in x.strip('()').split(', ')]
    return list_from_str


def check(frame, str_bl, str_csv, str_result, str_rate, str_locked):
    print('-' * 40)
    fn_bl_list = tuple_str_to_ls(str_bl)
    fn_csv = str_csv
    f_csv = open(fn_csv, encoding='utf-8')
    f_result_w = []
    list_mqxlz_dir = []
    list_found_rows = []
    regex_pattern = re.compile('<target xml:space="preserve">.*?</target>')

    for fn_bl in fn_bl_list:
        if fn_bl[-5:] == 'mqxlz':
            list_mqxlz_dir.append(mqxlz_dir_fname(fn_bl)[0])
            fn_bl_actual = mqxlz_dir_fname(fn_bl)[1]
        else:
            fn_bl_actual = fn_bl

        fn_bl_actual = fn_bl_actual.replace('\\', '/')
        f_bl = open(fn_bl_actual, encoding='utf-8')
        f_bl_r_raw = f_bl.read()
        f_bl_r_range_list = limit_range(f_bl_r_raw, str_rate, str_locked)
        f_bl_r = '\n'.join([regex_pattern.findall(i)[0][29:-9] for i in f_bl_r_range_list])
        print_and_append(fn_bl, [fn_bl], f_result_w)

        f_csv.seek(0)
        f_csv_r = csv.reader(f_csv)
        for row in f_csv_r:
            col_to_check = return_col_num(row)
            if f_bl_r.find(row[col_to_check]) != -1:
                row_found = [row[i] for i in range(len(row))]
                print_and_append(row_found, row_found, f_result_w)
                list_found_rows.append(row_found)
            else:
                continue

        f_bl.close()

    f_csv.close()

    if list_found_rows:
        print_and_append('\n' + 'Summary', ['Summary'], f_result_w)
        list_reduced = list({str(i) for i in list_found_rows})
        for i in list_reduced:
            print_and_append(i, list_str_to_list(i), f_result_w)
        print_and_append('', [''], f_result_w)

        fn_result = str_result
        f_result = open(fn_result, 'a', encoding='utf-8')
        f_result_wc = csv.writer(f_result, lineterminator='\n')
        f_result_wc.writerows(f_result_w)
        f_result.close()
        print(str_result.rsplit('/')[-1].rsplit('\\')[-1] + ' was successfully created.')
    else:
        print('No forbidden term was found!')

    if list_mqxlz_dir:
        for i in list_mqxlz_dir:
            os.remove(i+r'/document.mqxliff')
        for i in list_mqxlz_dir:
            try_to_rmdir(i)

    print('Focus on this screen and Press Enter key to exit the program.')
    try:
        input('\n')
    except:
        pass

    frame.quit()
