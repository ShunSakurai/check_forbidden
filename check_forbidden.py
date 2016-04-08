'''
cd dropbox/codes/check_forbidden
py check_forbidden.py
'''

import cf_scripts
import tkinter
import tkinter.filedialog

tk_F = tkinter.Frame()

args_bl = {'filetypes' : [('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]}
args_csv = {'filetypes' : [('csv', '*.csv'), ('text', '*.txt')]}

btn_bl = tkinter.Button(text='Billingual')
btn_csv = tkinter.Button(text='CSV')
btn_export = tkinter.Button(text='Result')

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
        var_export.set(f_bl[0].rsplit(r'/', 1)[0]+r'/checked_result.csv')


def import_csv(self):
    f_csv = tkinter.filedialog.askopenfilename(**args_csv)
    var_csv.set(f_csv)


def export_result(self):
    f_export = tkinter.filedialog.asksaveasfilename(initialfile='checked_result.csv', **args_csv)
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


def run(self):
    if btn_run['state'] == 'normal' or 'active':
        cf_scripts.check(tk_F, var_bl, var_csv, var_export)

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
