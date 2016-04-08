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
        sleep(0.05)
        os.rmdir(i)


def ls_str_to_ls(x):
    l_f_s = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return l_f_s


def tp_str_to_ls(x):
    l_f_s = [i.strip().strip(', ').strip('"').strip("'") for i in x.strip('()').split(', ')]
    return l_f_s


def check(frame, var_bl, var_csv, var_export):
    print('-' * 40)
    fn1_list = tp_str_to_ls(var_bl.get())
    fn2 = var_csv.get()
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
        f1r = regex_pattern.findall(f1r_raw)

        print_and_append(fn1, [fn1], f3w)

        f2.seek(0)
        f2r = csv.reader(f2)
        for row in f2r:
            col_to_check = return_col_num(row)
            for match in f1r:
                if match.find(row[col_to_check]) != -1:
                    sl = [row[i] for i in range(len(row))]
                    print_and_append(sl, sl, f3w)
                    list_found.append(sl)
                    break
                else:
                    continue

        f1.close()

    f2.close()
    if list_delete:
        for i in list_delete:
            os.remove(i+r'/document.mqxliff')
        sleep(0.01)
        for i in list_delete:
            try_to_rmdir(i)

    if list_found:
        print_and_append('\n' + 'Summary', ['Summary'], f3w)
        list_reduced = list({str(i) for i in list_found})
        for i in list_reduced:
            print_and_append(i, ls_str_to_ls(i), f3w)

        fn3 = var_export.get()
        f3 = open(fn3, 'a', encoding='utf-8')
        f3wc = csv.writer(f3, lineterminator='\n')
        f3wc.writerows(f3w)
        f3.close()

        print(var_export.get().rsplit('/')[-1].rsplit('\\')[-1]+' was successfully created.\nPress Enter key to exit.')
    else:
        print('No forbidden term was found!\nPress Enter key to exit.')

    try:
        input('\n')
    except:
        pass

    frame.quit()
