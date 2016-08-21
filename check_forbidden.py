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

ext_bl = [
    ('mqxlz / mqxliff', '*.mqxlz;*.mqxliff'),
    ('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]
ext_terms = [
    ('csv / text', '*.csv;*.txt'), ('csv', '*.csv'), ('text', '*.txt')]
ext_function = [('Python', '*.py')]
ext_result = [('csv', '*.csv')]

btn_bl = tkinter.Button(text='Billingual', underline=0)
btn_terms = tkinter.Button(text='Terms', underline=0)
btn_result = tkinter.Button(text='Result', underline=0, state='disabled')
three_buttons = [btn_bl, btn_terms, btn_result]

btn_bl.grid(row=0, column=0, columnspan=2, sticky='w', padx=5)
btn_terms.grid(row=1, column=0, columnspan=1, sticky='w', padx=5)
btn_result.grid(row=2, column=0, columnspan=1, sticky='w', padx=5)

var_function = tkinter.StringVar()
cb_function = tkinter.Checkbutton(variable=var_function)
cb_function.deselect()
cb_function.grid(row=1, column=1, sticky='e')

var_method = tkinter.StringVar()
cb_method = tkinter.Checkbutton(variable=var_method)
cb_method.select()
cb_method.grid(row=2, column=1, sticky='e')

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
    ent.grid(
        row=three_entries.index(ent), column=2, columnspan=2, sticky='w')

path_saved_terms = tkinter.StringVar(frame_main)
path_saved_terms.set('')
path_saved_function = tkinter.StringVar(frame_main)
path_saved_function.set('')
path_saved_result = tkinter.StringVar(frame_main)
path_saved_result.set('')

btn_open_bl = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
btn_open_terms = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
btn_open_result = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
three_open_buttons = [btn_open_bl, btn_open_terms, btn_open_result]

btn_open_bl.bind(
    '<ButtonRelease-1>', lambda x: cf_scripts.open_folder(var_bl.get()))
btn_open_terms.bind(
    '<ButtonRelease-1>', lambda x: cf_scripts.open_folder(var_terms.get()))
btn_open_result.bind(
    '<ButtonRelease-1>', lambda x: cf_scripts.open_folder(var_result.get()))


for btn in three_open_buttons:
    btn.grid(row=three_open_buttons.index(btn), column=4)

label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=2, sticky='w')

btn_options = tkinter.Button(text='⚙', borderwidth=0, font=('', 15))
btn_options.grid(row=3, column=3, sticky='e', padx=80)

btn_run = tkinter.Button(text='Run', state='disabled', takefocus=True)
btn_run.grid(row=3, column=3, sticky='e', padx=15, pady=5)

all_buttons = three_buttons + three_open_buttons + [
    cb_function, cb_method, btn_options, btn_run]

frame_options = tkinter.Frame(root, pady=5)
frame_options.grid(row=4, column=2, sticky='w')

label_rates = tkinter.Label(frame_options, text='\tMatch rates')
label_rates.grid(row=0, column=0, sticky='w')
label_locked = tkinter.Label(frame_options, text='\tLocked status')
label_locked.grid(row=0, column=1, sticky='w')

match_rates = [
    ('Check all segments', 'all', 6),
    (r'Exclude 101% matches', '101', 10),
    (r'Exclude 100% and 101%', '100', 10)]
var_rate = tkinter.StringVar()
var_rate.set('all')
rbs_rate = []

for label, rate, ul in match_rates:
    rb_rate = tkinter.Radiobutton(
        frame_options,
        text=label, variable=var_rate, value=rate, underline=ul)
    rbs_rate.append(rb_rate)

for rb in rbs_rate:
    rb.grid(row=(rbs_rate.index(rb) + 1), column=0, sticky='w', padx=10)

locked_states = [
    ('Include locked segments', 'all', 0),
    ('Exclude locked segments', 'locked', 0)]
var_locked = tkinter.StringVar()
var_locked.set('all')
rbs_locked = []

for label, state, ul in locked_states:
    rb_locked = tkinter.Radiobutton(
        frame_options,
        text=label, variable=var_locked, value=state, underline=ul)
    rbs_locked.append(rb_locked)

for rb in rbs_locked:
    rb.grid(row=(rbs_locked.index(rb) + 1), column=1, sticky='w', padx=10)


def focus_off():
    label_guide.focus_set()

for ent in three_entries:
    ent.bind('<Leave>', lambda x: focus_off())


def choose_bl(self):
    path = cf_scripts.ls_from_tuple_str(var_bl.get())[0]
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = None
    f_bl = tkinter.filedialog.askopenfilenames(
        filetypes=ext_bl, initialdir=initial_dir)
    if f_bl:
        var_bl.set(f_bl)
    if f_bl and not var_result.get():
        var_result.set(
            cf_scripts.dir_from_str_path(
                cf_scripts.ls_from_tuple_str(var_bl.get())[0])
                + '/checked_result.csv')
    focus_off()


def choose_terms(self):
    path = var_terms.get()
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = None

    if var_function.get() == '1':
        extensions = ext_function
    else:
        extensions = ext_terms
    f_terms = tkinter.filedialog.askopenfilename(
        filetypes=extensions, initialdir=initial_dir)
    if f_terms:
        var_terms.set(f_terms)
    focus_off()


def choose_result(self):
    if btn_result['state'] == 'disabled':
        return
    path = var_result.get()
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = cf_scripts.dir_from_str_path(
            cf_scripts.ls_from_tuple_str(var_bl.get()))
    f_result = tkinter.filedialog.asksaveasfilename(
        filetypes=ext_result, initialdir=initial_dir,
        initialfile='checked_result.csv')
    if f_result:
        var_result.set(f_result)
    focus_off()

three_funcs = [choose_bl, choose_terms, choose_result]

for i in range(3):
    three_buttons[i].bind('<ButtonRelease-1>', three_funcs[i])


def toggle_function_click(self, widget):
    if var_function.get() == '0':
        btn_terms['text'], btn_terms['underline'] = 'Funct.', 4
        path_saved_terms.set(var_terms.get())
        if path_saved_function.get():
            var_terms.set(path_saved_function.get())
        else:
            var_terms.set('')
    elif var_function.get() == '1':
        btn_terms['text'], btn_terms['underline'] = 'Terms', 0
        path_saved_function.set(var_terms.get())
        if path_saved_terms.get():
            var_terms.set(path_saved_terms.get())
        else:
            var_terms.set('')


def toggle_method_click(self, widget):
    if var_method.get() == '0':
        path_saved_result.set(var_result.get())
        var_result.set('Command Prompt only.')
        btn_result['state'] = 'disabled'
    elif var_method.get() == '1':
        if path_saved_result.get():
            var_result.set(path_saved_result.get())
        elif not path_saved_result.get() and var_bl.get():
            path_1 = cf_scripts.ls_from_tuple_str(var_bl.get())[0]
            var_result.set(
                cf_scripts.dir_from_str_path(path_1) + '/checked_result.csv')
        else:
            var_result.set('')
        btn_result['state'] = 'normal'

cb_function.bind(
    '<ButtonRelease-1>',
    lambda x: toggle_function_click('<ButtonRelease-1>', cb_function))
cb_method.bind(
    '<ButtonRelease-1>',
    lambda x: toggle_method_click('<ButtonRelease-1>', cb_method))


def toggle_function_sck(self, widget):
    toggle_function_click('<ButtonRelease-1>', widget)
    cb_function.toggle()


def toggle_method_sck(self, widget):
    toggle_method_click('<ButtonRelease-1>', widget)
    cb_method.toggle()


def enable_open_btn_if_statement(statement, btn):
    if statement:
        btn['text'] = '➔'
        btn['state'] = 'normal'
    else:
        btn['text'] = '⇨'
        btn['state'] = 'disabled'


def enable_open_bl_if_filled(var, unknown, w):
    enable_open_btn_if_statement(var_bl.get(), btn_open_bl)


def enable_open_terms_if_filled(var, unknown, w):
    enable_open_btn_if_statement(var_terms.get(), btn_open_terms)


def enable_open_result_if_filled(var, unknown, w):
    statement = var_result.get() and var_result.get() != 'Command Prompt only.'
    enable_open_btn_if_statement(statement, btn_open_result)

three_open_funcs = [
    enable_open_bl_if_filled, enable_open_terms_if_filled,
    enable_open_result_if_filled]

for var, btn, func in zip(three_vars, three_open_buttons, three_open_funcs):
    btn.grid(row=three_open_buttons.index(btn), column=4)
    var.trace('w', func)


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

btn_options.bind(
    '<ButtonRelease-1>',
    lambda x: toggle_options('<ButtonRelease-1>', btn_options))


def run(self):
    if btn_run['state'] == 'disabled':
        return
    cf_scripts.check_forbidden_terms(
        frame_main, var_bl.get(), var_terms.get(), var_result.get(),
        var_function.get(), var_method.get(), var_rate.get(), var_locked.get())

btn_run.bind('<ButtonRelease-1>', run)


def enable_run_if_filled(var, unknown, w):
    if var_bl.get() and var_terms.get() and var_result.get():
        btn_run['state'] = 'normal'
        btn_run['text'] = 'Run!'
    else:
        btn_run['state'] = 'disabled'
        btn_run['text'] = 'Run'

for var in three_vars:
    var.trace('w', enable_run_if_filled)

guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Target (NG), Index, Source, Target (OK), etc.'
guide_result = 'Can be an existing file. Results are added to the bottom.'
guide_open = 'Open the folder.'
guide_function = 'Import function(str_target) which returns a string or None'
guide_method = 'Select this Check box if you don\'t export the CSV file.'
guide_options = 'Show or hide Options.'
guide_run = 'Enabled when all the three fields are filled.'

ul_no = -1
ul_function = 7
ul_method = 12
ul_options = 13
ul_run = 7


def show_guide(self, guide, underline):
    label_guide['text'] = guide
    label_guide['underline'] = underline


def hide_guide(self):
    label_guide['text'] = ''
    label_guide['underline'] = ul_no


def bind_show_guide(btn, guide, underline):
    btn.bind('<Enter>', lambda x: show_guide('<Enter>', guide, underline))

bind_show_guide(btn_bl, guide_bl, ul_no)
bind_show_guide(btn_terms, guide_terms, ul_no)
bind_show_guide(btn_result, guide_result, ul_no)
for btn in three_open_buttons:
    bind_show_guide(btn, guide_open, ul_no)
bind_show_guide(cb_function, guide_function, ul_function)
bind_show_guide(cb_method, guide_method, ul_method)
bind_show_guide(btn_options, guide_options, ul_options)
bind_show_guide(btn_run, guide_run, ul_run)

for btn in all_buttons:
    btn.bind('<Leave>', hide_guide)


def sc_only_when_out_of_ent(func):
    if type(frame_main.focus_get()) == tkinter.Entry:
        pass
    else:
        func('')


def bind_keys(key, func):
    root.bind(key, lambda x: sc_only_when_out_of_ent(func))

bind_keys('<space>', run)
bind_keys('o', lambda x: toggle_options('o', btn_options))
bind_keys('b', choose_bl)
bind_keys('t', choose_terms)
bind_keys('r', choose_result)
bind_keys('f', lambda x: toggle_function_sck('f', cb_function))
bind_keys('c', lambda x: toggle_method_sck('c', cb_method))
bind_keys('a', lambda x: rbs_rate[0].select())
bind_keys('1', lambda x: rbs_rate[1].select())
bind_keys('0', lambda x: rbs_rate[2].select())
bind_keys('i', lambda x: rbs_locked[0].select())
bind_keys('e', lambda x: rbs_locked[1].select())


def press_return_key_to_click(self):
    frame_main.focus_get().event_generate('<ButtonRelease-1>')

root.bind('<Return>', press_return_key_to_click)

top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
frame_main.mainloop()
