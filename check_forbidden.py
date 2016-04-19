'''
cd dropbox/codes/check_forbidden
py -B check_forbidden.py
'''

import cf_scripts
import tkinter
import tkinter.filedialog

print('Loading...')

root = tkinter.Tk()
frame_main = tkinter.Frame(root)

args_bl = {'filetypes' : [('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]}
args_csv = {'filetypes' : [('csv', '*.csv'), ('text', '*.txt')]}

btn_bl = tkinter.Button(text='Billingual', underline=0)
btn_csv = tkinter.Button(text='CSV', underline=0)
btn_export = tkinter.Button(text='Result', underline=0)

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

ent_bl = tkinter.Entry(width=85, textvariable=var_bl)
ent_csv = tkinter.Entry(width=85, textvariable=var_csv)
ent_export = tkinter.Entry(width=85, textvariable=var_export)

three_entries = [ent_bl, ent_csv, ent_export]
for i in three_entries:
    i.grid(row=three_entries.index(i), column=1, sticky=tkinter.W, columnspan=2, padx=5)

guide_bl = 'Billingual files: .mqxlz or .mqxliff'
guide_csv = 'CSV format: 0(Index), Source, Target (NG), Target (OK)'
guide_export = 'Can be an existing file. Results are added to the bottom.'
guide_options = 'Show / hide options'
guide_run = 'Run button is enabled when all the three fields are filled.'
label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=1, sticky=tkinter.W)


def show_guide(self, guide):
    label_guide['text'] = guide


def hide_guide(self):
    label_guide['text'] = ''

btn_bl.bind('<Enter>', lambda x: show_guide('<Enter>', guide_bl))
btn_bl.bind('<Leave>', hide_guide)
btn_csv.bind('<Enter>', lambda x: show_guide('<Enter>', guide_csv))
btn_csv.bind('<Leave>', hide_guide)
btn_export.bind('<Enter>', lambda x: show_guide('<Enter>', guide_export))
btn_export.bind('<Leave>', hide_guide)


def run(self):
    if btn_run['state'] == 'active' or btn_run['state'] == 'normal':
        cf_scripts.check(frame_main, var_bl.get(), var_csv.get(), var_export.get(), var_rate.get(), var_locked.get())

btn_run = tkinter.Button(text='Run', state='disabled')
btn_run.grid(row=3, column=2, sticky=tkinter.E, padx=15, pady=5)
btn_run.bind('<ButtonRelease-1>', run)
btn_run.bind('<Enter>', lambda x: show_guide('<Enter>', guide_run))
btn_run.bind('<Leave>', hide_guide)


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

frame_options = tkinter.Frame(root, pady=5)
frame_options.grid(row=4, column=1, sticky=tkinter.W)

label_rates = tkinter.Label(frame_options, text='\tMatch rates')
label_rates.grid(row=0, column=0, sticky=tkinter.W)
label_locked = tkinter.Label(frame_options, text='\tLocked status')
label_locked.grid(row=0, column=1, sticky=tkinter.W)

match_rates = [('Check all segments', 'all', 6),
                           ('Exclude 101% matches', '101', 10),
                           ('Exclude 100% and 101 %', '100', 10)]
var_rate = tkinter.StringVar()
var_rate.set('all')
rbs_rate = []
for label, rate, ul in match_rates:
    rb_rate = tkinter.Radiobutton(frame_options, text=label, variable=var_rate, value=rate, underline=ul)
    rb_rate.grid(row=match_rates.index((label, rate, ul)) + 1, column=0, sticky=tkinter.W, padx=10)
    rbs_rate.append(rb_rate)

locked_states = [('Include locked segments', 'all', 0),
                              ('Exclude locked segments', 'locked', 0)]
var_locked = tkinter.StringVar()
var_locked.set('all')
rbs_locked = []
for label, state, ul in locked_states:
    rb_locked = tkinter.Radiobutton(frame_options, text=label, variable=var_locked, value=state, underline=ul)
    rb_locked.grid(row=locked_states.index((label, state, ul)) + 1, column=1, sticky=tkinter.W, padx=10)
    rbs_locked.append(rb_locked)


def show_hide_options(self, widget):
    if widget['text'] == '⚙':
        widget['text'] = '▲'
        widget['font'] = ('', 12)
        frame_options.grid(row=4, column=1, sticky=tkinter.W)
    elif widget['text'] == '▲':
        widget['text'] = '⚙'
        widget['font'] = ('', 15)
        frame_options.grid_forget()

btn_options = tkinter.Button(text='⚙', borderwidth=0, font=('', 15))
btn_options.grid(row=3, column=2, sticky=tkinter.E, padx=80)
btn_options.bind('<ButtonRelease-1>', lambda x: show_hide_options('<ButtonRelease-1>', btn_options))
btn_options.bind('<Enter>', lambda x: show_guide('<Enter>', guide_options))
btn_options.bind('<Leave>', hide_guide)

root.bind('<Return>', run)
root.bind('<space>', run)
root.bind('o', lambda x: show_hide_options('<o>', btn_options))
root.bind('b', import_bl)
root.bind('c', import_csv)
root.bind('r', export_result)
root.bind('a', lambda x: rbs_rate[0].select())
root.bind('1', lambda x: rbs_rate[1].select())
root.bind('0', lambda x: rbs_rate[2].select())
root.bind('i', lambda x: rbs_locked[0].select())
root.bind('e', lambda x: rbs_locked[1].select())

top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
frame_main.mainloop()
