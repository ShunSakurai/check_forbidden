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
btn_result = tkinter.Button(text='Result', underline=0)

three_buttons = [btn_bl, btn_terms, btn_result]
for btn in three_buttons:
    btn.grid(row=three_buttons.index(btn), column=0, sticky=tkinter.W, padx=5)

var_bl = tkinter.StringVar(frame_main)
var_terms = tkinter.StringVar(frame_main)
var_result = tkinter.StringVar(frame_main)

ent_bl = tkinter.Entry(width=85, textvariable=var_bl)
ent_terms = tkinter.Entry(width=85, textvariable=var_terms)
ent_result = tkinter.Entry(width=85, textvariable=var_result)


def focus_off():
    label_guide.focus_set()

three_entries = [ent_bl, ent_terms, ent_result]
for ent in three_entries:
    ent.grid(row=three_entries.index(ent), column=1, sticky=tkinter.W, columnspan=2, padx=5)
    ent.bind('<Leave>', lambda x: focus_off())


def choose_bl(self):
    f_bl = tkinter.filedialog.askopenfilenames(filetypes=ext_bl)
    var_bl.set(f_bl)
    if len(var_bl.get()) >= 1 and len(var_result.get()) == 0:
        var_result.set(f_bl[0].rsplit(r'/', 1)[0]+r'/checked_result.csv')
    focus_off()


def choose_terms(self):
    f_terms = tkinter.filedialog.askopenfilename(filetypes=ext_terms)
    var_terms.set(f_terms)
    focus_off()


def choose_result(self):
    f_result = tkinter.filedialog.asksaveasfilename(filetypes=ext_result, initialfile='checked_result.csv')
    var_result.set(f_result)
    focus_off()

func_buttons = [choose_bl, choose_terms, choose_result]
for i in range(3):
    three_buttons[i].bind('<ButtonRelease-1>', func_buttons[i])

label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=1, sticky=tkinter.W)

guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Index, Source, Target (NG), Target (OK)'
guide_result = 'Can be an existing file. Results are added to the bottom.'
guide_options = 'Show or hide options.'
guide_run = 'Enabled when all the three fields are filled.'
guides_buttons = [guide_bl, guide_terms, guide_result]


def show_guide(self, guide):
    label_guide['text'] = guide


def hide_guide(self):
    label_guide['text'] = ''

btn_bl.bind('<Enter>', lambda x: show_guide('<Enter>', guide_bl))
btn_terms.bind('<Enter>', lambda x: show_guide('<Enter>', guide_terms))
btn_result.bind('<Enter>', lambda x: show_guide('<Enter>', guide_result))
for i in range(3):
    three_buttons[i].bind('<Leave>', hide_guide)

frame_options = tkinter.Frame(root, pady=5)
frame_options.grid(row=4, column=1, sticky=tkinter.W)

label_rates = tkinter.Label(frame_options, text='\tMatch rates')
label_rates.grid(row=0, column=0, sticky=tkinter.W)
label_locked = tkinter.Label(frame_options, text='\tLocked status')
label_locked.grid(row=0, column=1, sticky=tkinter.W)


def select_and_focus(self):
    self.widget.select()
    self.widget.focus()

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
    rb.grid(row=(rbs_rate.index(rb) + 1), column=0, sticky=tkinter.W, padx=10)
    rb.bind('<ButtonRelease-1>', select_and_focus)

locked_states = [('Include locked segments', 'all', 0),
                              ('Exclude locked segments', 'locked', 0)]
var_locked = tkinter.StringVar()
var_locked.set('all')
rbs_locked = []
for label, state, ul in locked_states:
    rb_locked = tkinter.Radiobutton(frame_options, text=label, variable=var_locked, value=state, underline=ul)
    rbs_locked.append(rb_locked)
for rb in rbs_locked:
    rb.grid(row=(rbs_locked.index(rb) + 1), column=1, sticky=tkinter.W, padx=10)
    rb.bind('<ButtonRelease-1>', select_and_focus)


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


def run(self):
    if btn_run['state'] == 'active' or btn_run['state'] == 'normal':
        cf_scripts.check(frame_main, var_bl.get(), var_terms.get(), var_result.get(), var_rate.get(), var_locked.get())

btn_run = tkinter.Button(text='Run', state='disabled', takefocus=True)
btn_run.grid(row=3, column=2, sticky=tkinter.E, padx=15, pady=5)
btn_run.bind('<ButtonRelease-1>', run)
btn_run.bind('<Enter>', lambda x: show_guide('<Enter>', guide_run))
btn_run.bind('<Leave>', hide_guide)


def enable_run_if_filled(var, unknown, w):
    if var_bl.get() and var_terms.get() and var_result.get():
        btn_run['state'] = 'normal'
        btn_run['text'] = 'Run!'
    else:
        btn_run['state'] = 'disabled'
        btn_run['text'] = 'Run'

three_vars = [var_bl, var_terms, var_result]
for i in three_vars:
    i.trace('w', enable_run_if_filled)


def run_when_out_of_ent(func):
    if type(frame_main.focus_get()) == tkinter.Entry:
        pass
    else:
        func('')


def bind_keys(key, func):
    root.bind(key, lambda x: run_when_out_of_ent(func))

bind_keys('<space>', run)
bind_keys('o', lambda y: show_hide_options('o', btn_options))
bind_keys('b', choose_bl)
bind_keys('t', choose_terms)
bind_keys('r', choose_result)
bind_keys('a', lambda y: rbs_rate[0].select())
bind_keys('1', lambda y: rbs_rate[1].select())
bind_keys('0', lambda y: rbs_rate[2].select())
bind_keys('i', lambda y: rbs_locked[0].select())
bind_keys('e', lambda y: rbs_locked[1].select())


def return_to_click(self):
    frame_main.focus_get().event_generate('<ButtonRelease-1>')

root.bind('<Return>', return_to_click)

top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
frame_main.mainloop()
