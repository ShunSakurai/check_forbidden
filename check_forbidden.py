'''
cd dropbox/codes/check_forbidden
py -B check_forbidden.py
'''
import cf_scripts
import setup
import datetime
import os
import pickle
import tkinter
import tkinter.filedialog

print('Loading v', setup.dict_console['version'], '...', sep='')

# Constants
root = tkinter.Tk()
frame_main = tkinter.Frame(root)

ext_bl = [
    ('mqxlz / mqxliff', '*.mqxlz;*.mqxliff'),
    ('mqxlz', '*.mqxlz'), ('mqxliff', '*.mqxliff')]
ext_terms = [
    ('csv / text', '*.csv;*.txt'), ('csv', '*.csv'), ('text', '*.txt')]
ext_function = [('Python', '*.py')]
ext_result = [('csv', '*.csv')]

ph_cp_only = 'Command Prompt only. Uncheck to export the results.'
fn_options = 'cf_options.p'

# Widgets and functions
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
var_result.set(ph_cp_only)
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

all_guided_buttons = three_buttons + three_open_buttons + [
    cb_function, cb_method, btn_options, btn_run]

frame_options = tkinter.Frame(root, pady=5)

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

label_about = tkinter.Label(frame_options, text='\t\tAbout')
label_about.grid(row=0, column=2, sticky='w')

label_version = tkinter.Label(
    frame_options, text=''.join([
        '\tVersion ', setup.dict_console['version']
    ]), justify='left')
label_author = tkinter.Label(
    frame_options, text=''.join([
        '\t©2016-', str(datetime.date.today().year), ' ', setup.dict_console['author']
    ]), justify='left')
btn_readme = tkinter.Button(
    frame_options, text='Read readme',
    command=cf_scripts.open_readme, underline=9)
btn_update = tkinter.Button(
    frame_options, text='Check for updates',
    command=cf_scripts.check_updates, underline=10)
label_version.grid(row=1, column=2, sticky='w')
label_author.grid(row=2, column=2, sticky='w')
btn_readme.grid(row=3, column=2, sticky='w', padx=55)
btn_update.grid(row=4, column=2, sticky='w', padx=55)


label_settings = tkinter.Label(frame_options, text='\tOther settings')
label_settings.grid(row=4, column=0, sticky='w')

var_open = tkinter.StringVar()
cb_open = tkinter.Checkbutton(
    frame_options, text='Open CSV after export',
    underline=3, variable=var_open)
cb_open.select()
cb_open.grid(row=5, column=0, sticky='w')

var_load = tkinter.StringVar()
cb_load = tkinter.Checkbutton(
    frame_options, text='Save last used settings',
    underline=0, variable=var_load)
cb_load.deselect()
cb_load.grid(row=6, column=0, sticky='w')

btn_default = tkinter.Button(
    frame_options, text='Restore default settings', underline=8,
    takefocus=True
)
btn_default.grid(row=7, column=0, sticky='w')


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
    path = cf_scripts.ls_from_tuple_str(var_terms.get())[0]
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = None
    if var_function.get() == '1':
        extensions = ext_function
    else:
        extensions = ext_terms
    f_terms = tkinter.filedialog.askopenfilenames(
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


def turn_off_function():
    btn_terms.config(text='Terms', underline=0)
    path_saved_function.set(var_terms.get())
    if path_saved_terms.get():
        var_terms.set(path_saved_terms.get())
    else:
        var_terms.set('')


def turn_on_function():
    btn_terms.config(text='Funct.', underline=4)
    path_saved_terms.set(var_terms.get())
    if path_saved_function.get():
        var_terms.set(path_saved_function.get())
    else:
        var_terms.set('')


def toggle_function_click(self, widget):
    if var_function.get() == '0':
        turn_on_function()
    elif var_function.get() == '1':
        turn_off_function()


def turn_on_method():
    path_saved_result.set(var_result.get())
    var_result.set(ph_cp_only)
    btn_result['state'] = 'disabled'


def turn_off_method():
    if path_saved_result.get():
        var_result.set(path_saved_result.get())
    elif not path_saved_result.get() and var_bl.get():
        path_1 = cf_scripts.ls_from_tuple_str(var_bl.get())[0]
        var_result.set(
            cf_scripts.dir_from_str_path(path_1) + '/checked_result.csv')
    else:
        var_result.set('')
    btn_result['state'] = 'normal'


def toggle_method_click(self, widget):
    if var_method.get() == '1':
        turn_off_method()
    elif var_method.get() == '0':
        turn_on_method()


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
        btn.config(text='➔', state='normal')
    else:
        btn.config(text='⇨', state='disabled')


def enable_open_bl_if_filled(var, unknown, w):
    enable_open_btn_if_statement(var_bl.get(), btn_open_bl)


def enable_open_terms_if_filled(var, unknown, w):
    enable_open_btn_if_statement(var_terms.get(), btn_open_terms)


def enable_open_result_if_filled(var, unknown, w):
    statement = var_result.get() and var_result.get() != ph_cp_only
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


def turn_on_options(widget):
    widget.config(text='▲', font=('', 12))
    frame_options.grid(
        row=4, column=0, columnspan=4, sticky='w', padx=30
    )


def turn_off_options(widget):
        widget.config(text='⚙', font=('', 15))
        frame_options.grid_forget()


def toggle_options(self, widget):
    if widget['text'] == '⚙':
        turn_on_options(widget)
    elif widget['text'] == '▲':
        turn_off_options(widget)


btn_options.bind(
    '<ButtonRelease-1>',
    lambda x: toggle_options('<ButtonRelease-1>', btn_options))


def get_options():
    dict_options = {
        'str_function': var_function.get(),
        'str_method': var_method.get(),
        'str_rate': var_rate.get(),
        'str_locked': var_locked.get(),
        'str_open': var_open.get(),
        'str_load': var_load.get()
    }
    return dict_options


def restore_default(self):
    var_function.set('0')
    var_method.set('1')
    var_rate.set('all')
    var_locked.set('all')
    var_open.set('1')
    var_load.set('0')


btn_default.bind('<ButtonRelease-1>', restore_default)


def load_options():
    if not os.path.exists(fn_options):
        print('Saved options are not loaded.')
        return

    f_loaded_options = open(fn_options, 'rb')
    dict_loaded_options = pickle.load(f_loaded_options)
    f_loaded_options.close()

    if dict_loaded_options['str_load'] != '1':
        print('Saved options are not loaded.')
        return
    else:
        turn_on_options(btn_options)
        var_function.set(dict_loaded_options['str_function'])
        var_method.set(dict_loaded_options['str_method'])
        var_rate.set(dict_loaded_options['str_rate'])
        var_locked.set(dict_loaded_options['str_locked'])
        var_open.set(dict_loaded_options['str_open'])
        var_load.set(dict_loaded_options['str_load'])
        if var_method.get() == '0':
            turn_off_method()
        print('Saved options are loaded.')


def save_options():
    dict_options = get_options()
    f_to_save_options = open(fn_options, 'wb')
    pickle.dump(dict_options, f_to_save_options)
    f_to_save_options.close()


def run(self):
    if btn_run['state'] == 'disabled':
        return
    dict_options = get_options()
    cf_scripts.check_forbidden_terms(
        var_bl.get(), var_terms.get(), var_result.get(), dict_options)
    cf_scripts.ask_quit(frame_main)


btn_run.bind('<ButtonRelease-1>', run)


def enable_run_if_filled(var, unknown, w):
    if var_bl.get() and var_terms.get() and var_result.get():
        btn_run.config(state='normal', text='Run!')
    else:
        btn_run.config(state='disabled', text='Run')


for var in three_vars:
    var.trace('w', enable_run_if_filled)

guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Target (NG), Index, Source, Target (OK), etc.'
guide_result = 'Can be an existing file. Results are added to the bottom.'
guide_open = 'Open the folder.'
guide_function = 'function(int_id, str_target) that returns a 2D list or None'
guide_method = 'Select this Check box if you don\'t export the CSV file.'
guide_options = 'Show or hide Options.'
guide_run = 'Enabled when all the three fields are filled. (space bar)'

ul_no = -1
ul_function = 0
ul_method = 12
ul_options = 13
ul_run = 7


def show_guide(self, guide, underline):
    label_guide.config(text=guide, underline=underline)


def hide_guide(self):
    label_guide.config(text='', underline=ul_no)


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

for btn in all_guided_buttons:
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
bind_keys('m', lambda x: cf_scripts.open_readme())
bind_keys('u', lambda x: cf_scripts.check_updates())
bind_keys('a', lambda x: rbs_rate[0].select())
bind_keys('1', lambda x: rbs_rate[1].select())
bind_keys('0', lambda x: rbs_rate[2].select())
bind_keys('i', lambda x: rbs_locked[0].select())
bind_keys('e', lambda x: rbs_locked[1].select())
bind_keys('n', lambda x: cb_open.toggle())
bind_keys('s', lambda x: cb_load.toggle())
bind_keys('d', restore_default)


def press_return_key_to_click(self):
    frame_main.focus_get().event_generate('<ButtonRelease-1>')


root.bind('<Return>', press_return_key_to_click)


def close_callback():
    save_options()
    root.destroy()


# Initiating the program
top = frame_main.winfo_toplevel()
top.resizable(False, False)
frame_options.grid_forget()
load_options()
print('tk window is ready to use.')
root.protocol('WM_DELETE_WINDOW', close_callback)
frame_main.mainloop()
