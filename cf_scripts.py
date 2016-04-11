import csv
import os
import re
from time import sleep
import zipfile


def mqxlz_path_fname(fn):
    path_export = fn.rsplit(r'.', 1)[0] + '_export'
    z1 = zipfile.ZipFile(fn)
    fn_actual = z1.extract('document.mqxliff', path=path_export)
    return path_export, fn_actual


def filter_segments(raw, str_rate, str_locked):
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
            print('Please check the bilingual file location and delete the _export folder manually.')


def ls_str_to_ls(x):
    l_f_s = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return l_f_s


def tp_str_to_ls(x):
    l_f_s = [i.strip().strip(', ').strip('"').strip("'") for i in x.strip('()').split(', ')]
    return l_f_s


def check(frame, str_bl, str_csv, str_export, str_rate, str_locked):
    print('-' * 40)
    fn1_list = tp_str_to_ls(str_bl)
    fn2 = str_csv
    f2 = open(fn2, encoding='utf-8')
    f3w = []
    list_delete = []
    list_found = []
    regex_pattern = re.compile('<target xml:space="preserve">.*?</target>')

    for fn1 in fn1_list:
        if fn1[-5:] == 'mqxlz':
            list_delete.append(mqxlz_path_fname(fn1)[0])
            fn1_actual = mqxlz_path_fname(fn1)[1]
        else:
            fn1_actual = fn1

        fn1_actual = fn1_actual.replace('\\', '/')
        f1 = open(fn1_actual, encoding='utf-8')
        f1r_raw = f1.read()
        f1r_filtered_list = filter_segments(f1r_raw, str_rate, str_locked)
        f1r = '\n'.join([regex_pattern.findall(i)[0][29:-9] for i in f1r_filtered_list])
        print_and_append(fn1, [fn1], f3w)

        f2.seek(0)
        f2r = csv.reader(f2)
        for row in f2r:
            col_to_check = return_col_num(row)
            if f1r.find(row[col_to_check]) != -1:
                sl = [row[i] for i in range(len(row))]
                print_and_append(sl, sl, f3w)
                list_found.append(sl)
            else:
                continue

        f1.close()

    f2.close()

    if list_found:
        print_and_append('\n' + 'Summary', ['Summary'], f3w)
        list_reduced = list({str(i) for i in list_found})
        for i in list_reduced:
            print_and_append(i, ls_str_to_ls(i), f3w)
        print_and_append('', [''], f3w)

        fn3 = str_export
        f3 = open(fn3, 'a', encoding='utf-8')
        f3wc = csv.writer(f3, lineterminator='\n')
        f3wc.writerows(f3w)
        f3.close()
        print(str_export.rsplit('/')[-1].rsplit('\\')[-1] + ' was successfully created.')
    else:
        print('No forbidden term was found!')

    if list_delete:
        for i in list_delete:
            os.remove(i+r'/document.mqxliff')
        for i in list_delete:
            try_to_rmdir(i)

    print('Focus on this screen and Press Enter key to exit.')
    try:
        input('\n')
    except:
        pass

    frame.quit()
