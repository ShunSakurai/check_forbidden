'''
cd dropbox/codes/check_forbidden
py check_forbidden.py
'''

import csv
import zipfile
import os
import tkinter
import tkinter.filedialog
import re
from time import sleep

tk_F = tkinter.Frame()

args_bl = {'filetypes' : [('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]}
args_csv = {'filetypes' : [('csv', '*.csv'), ('text', '*.txt')]}

btn_bl = tkinter.Button(text='Billingual file')
btn_csv = tkinter.Button(text='CSV file')
btn_export = tkinter.Button(text='Export file')

var_bl = tkinter.StringVar(tk_F)
var_csv = tkinter.StringVar(tk_F)
var_export = tkinter.StringVar(tk_F)

three_buttons = [btn_bl, btn_csv, btn_export]
for i in three_buttons:
    i.grid(row=three_buttons.index(i), column=0, columnspan=2, sticky=tkinter.W, padx=5)

btn_csv.grid(columnspan=1)


def import_bl(self):
    f_bl = tkinter.filedialog.askopenfilenames(**args_bl)
    var_bl.set(f_bl)
    if len(var_bl.get()) >= 1 and len(var_export.get()) == 0:
        var_export.set(f_bl[0].rsplit(r'/', 1)[0]+r'/result.csv')


def import_csv(self):
    f_csv = tkinter.filedialog.askopenfilename(**args_csv)
    var_csv.set(f_csv)


def export_result(self):
    f_export = tkinter.filedialog.asksaveasfilename(initialfile='result.csv', **args_csv)
    var_export.set(f_export)


btn_bl.bind('<ButtonRelease-1>', import_bl)
btn_csv.bind('<ButtonRelease-1>', import_csv)
btn_export.bind('<ButtonRelease-1>', export_result)

ent_bl = tkinter.Entry(width=65, textvariable=var_bl)
ent_csv = tkinter.Entry(width=65, textvariable=var_csv)
ent_export = tkinter.Entry(width=65, textvariable=var_export)

three_entries = [ent_bl, ent_csv, ent_export]
for i in three_entries:
    i.grid(row=three_entries.index(i), column=2, columnspan=2, padx=5)

message = 'CSV format: 0(Index), Source, Target (NG), Target (OK)'
label_csv = tkinter.Label(text='')
label_csv.grid(row=3, column=0, columnspan=3)


def show_format(self):
    label_csv['text'] = message


def hide_format(self):
    label_csv['text'] = ''

help_csv = tkinter.Label(text='?')
help_csv.grid(row=1, column=1)
help_csv.bind('<Enter>', show_format)
help_csv.bind('<Leave>', hide_format)


def str_to_ls(x):
    l_f_s = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return l_f_s


def check():
    print('-' * 40)
    fn1_list_raw = var_bl.get().strip('()').split(', ')
    fn1_list = [i.strip().strip(', ').strip('"').strip("'") for i in fn1_list_raw]
    fn2 = var_csv.get()
    f2 = open(fn2, encoding='utf-8')
    f3w = []
    list_delete = []
    list_found = []
    regex_pattern = re.compile('<target xml:space="preserve">.*?</target>')

    for fn1 in fn1_list:
        if fn1[-5:] == 'mqxlz':
            path_export = fn1.rsplit(r'.', 1)[0]+'_export'
            list_delete.append(path_export)
            z1 = zipfile.ZipFile(fn1)
            fn1_actual = z1.extract('document.mqxliff', path=path_export)
        else:
            fn1_actual = fn1

        fn1_actual = fn1_actual.replace('\\', '/')
        f1 = open(fn1_actual, encoding='utf-8')
        f1r_raw = f1.read()
        f1r = regex_pattern.findall(f1r_raw)

        f3w.append([fn1])
        print(fn1)

        f2.seek(0)
        f2r = csv.reader(f2)
        for row in f2r:
            if len(row) >= 3:
                col_to_check = 2
            else:
                col_to_check = 0

            for match in f1r:
                if match.find(row[col_to_check]) != -1:
                    sl = [row[i] for i in range(len(row))]
                    f3w.append(sl)
                    print(sl)
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
            try:
                os.rmdir(i)
            except:
                sleep(0.05)
                os.rmdir(i)

    if list_found:
        f3w.append(['Summary'])
        print('\nSummary')
        set_found = {str(i) for i in list_found}
        list_reduced = list(set_found)
        for i in list_reduced:
            f3w.append(str_to_ls(i))
            print(i)

        fn3 = var_export.get()
        f3 = open(fn3, 'a', encoding='utf-8')
        f3wc = csv.writer(f3, lineterminator='\n')
        f3wc.writerows(f3w)
        f3.close()

        print('\n'+var_export.get().rsplit('/')[-1].rsplit('\\')[-1]+' was successfully created.\nPress Enter key to exit.')
    else:
        print('\nNo forbidden term was found!\nPress Enter key to exit.')

    try:
        input('\n')
    except:
        pass

    tk_F.quit()


def run(self):
    if btn_run['state'] == 'normal' or 'active':
        check()

btn_run = tkinter.Button(text='Run', state='disabled')
btn_run.grid(row=3, column=3, sticky=tkinter.E, padx=15, pady=5)
btn_run.bind('<ButtonRelease-1>', run)


def true_false(var, unknown, w):
    if var_bl.get() and var_csv.get() and var_export.get():
        btn_run['state'] = 'normal'
        btn_run['text'] = 'Run!'
    else:
        btn_run['state'] = 'disabled'
        btn_run['text'] = 'Run'

three_vars = [var_bl, var_csv, var_export]
for i in three_vars:
    i.trace('w', true_false)

top = tk_F.winfo_toplevel()
top.resizable(False, False)
tk_F.mainloop()

