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

ext_bl = [('mqxlz / mqxliff', '*.mqxlz;*.mqxliff'), ('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]
ext_terms = [('csv / text', '*.csv;*.txt'), ('csv', '*.csv'), ('text', '*.txt')]
ext_result = [('csv', '*.csv')]

btn_bl = tkinter.Button(text='Billingual', underline=0)
btn_terms = tkinter.Button(text='Terms', underline=0)
btn_result = tkinter.Button(text='Result', underline=0, state='disabled')
three_buttons = [btn_bl, btn_terms, btn_result]

btn_bl.grid(row=0, column=0, columnspan=2, sticky='w', padx=5)
btn_terms.grid(row=1, column=0, columnspan=2, sticky='w', padx=5)
btn_result.grid(row=2, column=0, columnspan=1, sticky='w', padx=5)

var_bl = tkinter.StringVar(frame_main)
var_terms = tkinter.StringVar(frame_main)
var_result = tkinter.StringVar(frame_main)
var_result.set('Command Prompt only.')
three_vars = [var_bl, var_terms, var_result]

ent_bl = tkinter.Entry(width=85, textvariable=var_bl)
ent_terms = tkinter.Entry(width=85, textvariable=var_terms)
ent_result = tkinter.Entry(width=85, textvariable=var_result)
three_entries = [ent_bl, ent_terms, ent_result]

for ent in three_entries:
    ent.grid(row=three_entries.index(ent), column=2, sticky='w', columnspan=2, padx=5)

path_saved_bl = tkinter.StringVar(frame_main)
path_saved_terms = tkinter.StringVar(frame_main)
path_saved_result = tkinter.StringVar(frame_main)
three_saved_paths = [path_saved_bl, path_saved_terms, path_saved_result]

for path in three_saved_paths:
    path.set('')

var_method = tkinter.StringVar()
cb_method = tkinter.Checkbutton(variable=var_method)
cb_method.select()
cb_method.grid(row=2, column=1, sticky='e')

label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=2, sticky='w')

btn_options = tkinter.Button(text='⚙', borderwidth=0, font=('', 15))
btn_options.grid(row=3, column=3, sticky='e', padx=80)

btn_run = tkinter.Button(text='Run', state='disabled', takefocus=True)
btn_run.grid(row=3, column=3, sticky='e', padx=15, pady=5)
six_buttons = three_buttons + [cb_method, btn_options, btn_run]

frame_options = tkinter.Frame(root, pady=5)
frame_options.grid(row=4, column=2, sticky='w')

label_rates = tkinter.Label(frame_options, text='\tMatch rates')
label_rates.grid(row=0, column=0, sticky='w')
label_locked = tkinter.Label(frame_options, text='\tLocked status')
label_locked.grid(row=0, column=1, sticky='w')

match_rates = [('Check all segments', 'all', 6),
                           (r'Exclude 101% matches', '101', 10),
                           (r'Exclude 100% and 101%', '100', 10)]
var_rate = tkinter.StringVar()
var_rate.set('all')
rbs_rate = []

for label, rate, ul in match_rates:
    rb_rate = tkinter.Radiobutton(frame_options, text=label, variable=var_rate, value=rate, underline=ul)
    rbs_rate.append(rb_rate)

for rb in rbs_rate:
    rb.grid(row=(rbs_rate.index(rb) + 1), column=0, sticky='w', padx=10)

locked_states = [('Include locked segments', 'all', 0),
                              ('Exclude locked segments', 'locked', 0)]
var_locked = tkinter.StringVar()
var_locked.set('all')
rbs_locked = []

for label, state, ul in locked_states:
    rb_locked = tkinter.Radiobutton(frame_options, text=label, variable=var_locked, value=state, underline=ul)
    rbs_locked.append(rb_locked)

for rb in rbs_locked:
    rb.grid(row=(rbs_locked.index(rb) + 1), column=1, sticky='w', padx=10)


def focus_off():
    label_guide.focus_set()

for ent in three_entries:
    ent.bind('<Leave>', lambda x: focus_off())


def choose_bl(self):
    path_saved_bl.set(var_bl.get())
    initial_dir = cf_scripts.dir_from_path(var_bl.get())
    f_bl = tkinter.filedialog.askopenfilenames(filetypes=ext_bl, initialdir=initial_dir)
    var_bl.set(f_bl)
    if len(var_bl.get()) is not None and var_result.get() is None:
        var_result.set(cf_scripts.dir_from_path(f_bl[0]) + '/checked_result.csv')
    if var_bl.get() == '':
        var_bl.set(path_saved_bl.get())
    focus_off()


def choose_terms(self):
    path_saved_terms.set(var_terms.get())
    initial_dir = cf_scripts.dir_from_path(var_terms.get())
    f_terms = tkinter.filedialog.askopenfilename(filetypes=ext_terms, initialdir=initial_dir)
    var_terms.set(f_terms)
    if var_terms.get() == '':
        var_terms.set(path_saved_terms.get())
    focus_off()


def choose_result(self):
    path_saved_result.set(var_result.get())
    if var_result.get() == '':
        initial_dir = cf_scripts.dir_from_path(var_bl.get())
    else:
        initial_dir = cf_scripts.dir_from_path(var_result.get())
    f_result = tkinter.filedialog.asksaveasfilename(filetypes=ext_result, initialdir=initial_dir, initialfile='checked_result.csv')
    var_result.set(f_result)
    if var_result.get() == '':
        var_result.set(path_saved_result.get())
    focus_off()

three_funcs = [choose_bl, choose_terms, choose_result]

for i in range(3):
    three_buttons[i].bind('<ButtonRelease-1>', three_funcs[i])


def toggle_method_click(self, widget):
    if var_method.get() == '0':
        path_saved_result.set(var_result.get())
        var_result.set('Command Prompt only.')
        btn_result['state'] = 'disabled'
    elif var_method.get() == '1':
        var_result.set(path_saved_result.get())
        btn_result['state'] = 'normal'

cb_method.bind('<ButtonRelease-1>', lambda x: toggle_method_click('<ButtonRelease-1>', cb_method))


def toggle_method_sc(self, widget):
    toggle_method_click('<ButtonRelease-1>', widget)
    cb_method.toggle()


def select_and_focus(self):
    self.widget.select()
    self.widget.focus()

for rb in rbs_rate:
    rb.bind('<ButtonRelease-1>', select_and_focus)

for rb in rbs_locked:
    rb.bind('<ButtonRelease-1>', select_and_focus)


def toggle_options(self, widget):
    if widget['text'] == '⚙':
        widget['text'] = '▲'
        widget['font'] = ('', 12)
        frame_options.grid(row=4, column=2, sticky='w')
    elif widget['text'] == '▲':
        widget['text'] = '⚙'
        widget['font'] = ('', 15)
        frame_options.grid_forget()

btn_options.bind('<ButtonRelease-1>', lambda x: toggle_options('<ButtonRelease-1>', btn_options))


def run(self):
    if btn_run['state'] == 'active' or btn_run['state'] == 'normal':
        cf_scripts.check_forbidden_terms(frame_main, var_bl.get(), var_terms.get(), var_result.get(), var_method.get(), var_rate.get(), var_locked.get())
btn_run.bind('<ButtonRelease-1>', run)


def enable_run_if_filled(var, unknown, w):
    if var_bl.get() and var_terms.get() and var_result.get():
        btn_run['state'] = 'normal'
        btn_run['text'] = 'Run!'
    else:
        btn_run['state'] = 'disabled'
        btn_run['text'] = 'Run'

for i in three_vars:
    i.trace('w', enable_run_if_filled)

guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Index, Source, Target (NG), Target (OK)'
guide_result = 'Can be an existing file. Results are added to the bottom.'
guide_method = 'Select this check box if you don\'t export the CSV file.'
guide_options = 'Show or hide options.'
guide_run = 'Enabled when all the three fields are filled.'


def show_guide(self, guide):
    label_guide['text'] = guide


def hide_guide(self):
    label_guide['text'] = ''

btn_bl.bind('<Enter>', lambda x: show_guide('<Enter>', guide_bl))
btn_terms.bind('<Enter>', lambda x: show_guide('<Enter>', guide_terms))
btn_result.bind('<Enter>', lambda x: show_guide('<Enter>', guide_result))
cb_method.bind('<Enter>', lambda x: show_guide('<Enter>', guide_method))
btn_options.bind('<Enter>', lambda x: show_guide('<Enter>', guide_options))
btn_run.bind('<Enter>', lambda x: show_guide('<Enter>', guide_run))
for i in range(6):
    six_buttons[i].bind('<Leave>', hide_guide)


def sc_when_out_of_ent(func):
    if type(frame_main.focus_get()) == tkinter.Entry:
        pass
    else:
        func('')


def bind_keys(key, func):
    root.bind(key, lambda x: sc_when_out_of_ent(func))

bind_keys('<space>', run)
bind_keys('o', lambda x: toggle_options('o', btn_options))
bind_keys('b', choose_bl)
bind_keys('t', choose_terms)
bind_keys('r', choose_result)
bind_keys('c', lambda x: toggle_method_sc('c', cb_method))
bind_keys('a', lambda x: rbs_rate[0].select())
bind_keys('1', lambda x: rbs_rate[1].select())
bind_keys('0', lambda x: rbs_rate[2].select())
bind_keys('i', lambda x: rbs_locked[0].select())
bind_keys('e', lambda x: rbs_locked[1].select())


def return_to_click(self):
    frame_main.focus_get().event_generate('<ButtonRelease-1>')

root.bind('<Return>', return_to_click)

top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
frame_main.mainloop()
