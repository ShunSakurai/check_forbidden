'''
cd dropbox/codes/check_forbidden
py -B check_forbidden.py
'''

import cf_scripts
import tkinter
import tkinter.filedialog

frame_main = tkinter.Frame()

args_bl = {'filetypes' : [('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]}
args_csv = {'filetypes' : [('csv', '*.csv'), ('text', '*.txt')]}

btn_bl = tkinter.Button(text='Billingual')
btn_csv = tkinter.Button(text='CSV')
btn_export = tkinter.Button(text='Result')

var_bl = tkinter.StringVar(frame_main)
var_csv = tkinter.StringVar(frame_main)
var_export = tkinter.StringVar(frame_main)

btn_bl.grid(row=0, column=0, sticky=tkinter.W, padx=5)
btn_csv.grid(row=1, column=0, sticky=tkinter.W, padx=5)
btn_export.grid(row=2, column=0, sticky=tkinter.W, padx=5)


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

ent_bl = tkinter.Entry(width=70, textvariable=var_bl)
ent_csv = tkinter.Entry(width=70, textvariable=var_csv)
ent_export = tkinter.Entry(width=70, textvariable=var_export)

three_entries = [ent_bl, ent_csv, ent_export]
for i in three_entries:
    i.grid(row=three_entries.index(i), column=1, sticky=tkinter.W, columnspan=2, padx=5)

bl_guide = 'Billingual files: .mqxlz or .mqxliff'
csv_guide = 'CSV format: 0(Index), Source, Target (NG), Target (OK)'
export_guide = ''
options_guide = 'Show / hide options'
label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=1, sticky=tkinter.W)


def show_guide(self, guide):
    label_guide['text'] = guide


def hide_guide(self):
    label_guide['text'] = ''

btn_bl.bind('<Enter>', lambda guide: show_guide('<Enter>', bl_guide))
btn_bl.bind('<Leave>', hide_guide)
btn_csv.bind('<Enter>', lambda guide: show_guide('<Enter>', csv_guide))
btn_csv.bind('<Leave>', hide_guide)
btn_export.bind('<Enter>', lambda guide: show_guide('<Enter>', export_guide))
btn_export.bind('<Leave>', hide_guide)


def run(self):
    if btn_run['state'] == 'active':
        cf_scripts.check(frame_main, var_bl, var_csv, var_export)

btn_run = tkinter.Button(text='Run', state='disabled')
btn_run.grid(row=3, column=2, sticky=tkinter.E, padx=15, pady=5)
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

frame_options = tkinter.Frame(borderwidth=10, pady=5)
frame_options.grid(row=4, column=1, sticky=tkinter.W)
match_rates = [('Check all segments', None), ('Exclude 101% matches', '101'), ('Exclude 101% and 100 %', '100')]
v = tkinter.StringVar()
v.set(None)
label_options = tkinter.Label(frame_options, text='Options')
label_options.grid(sticky=tkinter.W)
for label, rate in match_rates:
    rb = tkinter.Radiobutton(frame_options, text=label, variable=v, value=rate)
    rb.grid(sticky=tkinter.W)


def show_hide_options(self):
    if self.widget['text'] == '▼':
        self.widget['text'] = '△'
        frame_options.grid(row=4, column=1, sticky=tkinter.W)
    elif self.widget['text'] == '△':
        self.widget['text'] = '▼'
        frame_options.grid_forget()

btn_options = tkinter.Button(text='▼', borderwidth=0)
#Triangles ▽▼△▲
btn_options.grid(row=3, column=2, sticky=tkinter.E, padx=65)
btn_options.bind('<ButtonRelease-1>', show_hide_options)
btn_options.bind('<Enter>', lambda guide: show_guide('<Enter>', options_guide))
btn_options.bind('<Leave>', hide_guide)

top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
frame_main.mainloop()
