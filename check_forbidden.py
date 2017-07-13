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
fn_result = 'checked_result.csv'

ph_cp_only = 'Command Prompt only. Uncheck to export the results.'
fn_options = 'cf_options.p'

dict_cb_hover = {
    'function': False,
    'export': False,
    'open': False,
    'save': False
}

# Widgets
btn_bl = tkinter.Button(text='Billingual', underline=0)
btn_terms = tkinter.Button(text='Terms', underline=0)
btn_result = tkinter.Button(text='Result', underline=0, state='disabled')
three_buttons = [btn_bl, btn_terms, btn_result]

btn_bl.grid(row=0, column=0, columnspan=2, sticky='w', padx=5)
btn_terms.grid(row=1, column=0, columnspan=1, sticky='w', padx=5)
btn_result.grid(row=2, column=0, columnspan=1, sticky='w', padx=5)

var_bool_function = tkinter.BooleanVar()
cb_function = tkinter.Checkbutton(variable=var_bool_function)
cb_function.deselect()
cb_function.grid(row=1, column=1, sticky='e')

var_bool_export = tkinter.BooleanVar()
cb_export = tkinter.Checkbutton(variable=var_bool_export)
cb_export.select()
cb_export.grid(row=2, column=1, sticky='e')

var_str_bl = tkinter.StringVar(frame_main)
var_str_terms = tkinter.StringVar(frame_main)
var_str_result = tkinter.StringVar(frame_main)
var_str_result.set(ph_cp_only)
three_vars = [var_str_bl, var_str_terms, var_str_result]

ent_bl = tkinter.Entry(width=85, textvariable=var_str_bl)
ent_terms = tkinter.Entry(width=85, textvariable=var_str_terms)
ent_result = tkinter.Entry(width=85, textvariable=var_str_result)
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

btn_folder_bl = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
btn_folder_terms = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
btn_folder_result = tkinter.Button(
    text='⇨', state='disabled', takefocus=True, borderwidth=0, padx=5)
three_folder_buttons = [btn_folder_bl, btn_folder_terms, btn_folder_result]

for btn in three_folder_buttons:
    btn.grid(row=three_folder_buttons.index(btn), column=4)


label_guide = tkinter.Label(text='')
label_guide.grid(row=3, column=2, sticky='w')

btn_options = tkinter.Button(text='⚙', borderwidth=0, font=('', 15))
btn_options.grid(row=3, column=3, sticky='e', padx=80)

btn_run = tkinter.Button(text='Run', state='disabled', takefocus=True)
btn_run.grid(row=3, column=3, sticky='e', padx=15, pady=5)

all_guided_ui = three_buttons + three_folder_buttons + [
    cb_function, cb_export, btn_options, btn_run]

frame_options = tkinter.Frame(root, pady=5)

label_rates = tkinter.Label(frame_options, text='\tMatch rates')
label_rates.grid(row=0, column=0, sticky='w')
label_locked = tkinter.Label(frame_options, text='\tLocked status')
label_locked.grid(row=0, column=1, sticky='w')

match_rates = [
    ('Check all segments', 'all', 6),
    (r'Exclude 101% matches', '101', 10),
    (r'Exclude 100% and 101%', '100', 10)]
var_str_rate = tkinter.StringVar()
var_str_rate.set('all')
rbs_rate = []

for label, rate, ul in match_rates:
    rb_rate = tkinter.Radiobutton(
        frame_options,
        text=label, variable=var_str_rate, value=rate, underline=ul)
    rbs_rate.append(rb_rate)

for rb in rbs_rate:
    rb.grid(row=(rbs_rate.index(rb) + 1), column=0, sticky='w', padx=10)

locked_states = [
    ('Include locked segments', 'all', 0),
    ('Exclude locked segments', 'locked', 0)]
var_str_locked = tkinter.StringVar()
var_str_locked.set('all')
rbs_locked = []

for label, state, ul in locked_states:
    rb_locked = tkinter.Radiobutton(
        frame_options,
        text=label, variable=var_str_locked, value=state, underline=ul)
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
btn_readme = tkinter.Button(frame_options, text='Read readme', underline=9)
btn_update = tkinter.Button(frame_options, text='Check for updates', underline=10)
label_version.grid(row=1, column=2, sticky='w')
label_author.grid(row=2, column=2, sticky='w')
btn_readme.grid(row=3, column=2, sticky='w', padx=55)
btn_update.grid(row=4, column=2, sticky='w', padx=55)

label_settings = tkinter.Label(frame_options, text='\tOther settings')
label_settings.grid(row=4, column=0, sticky='w')

var_bool_open = tkinter.BooleanVar()
cb_open = tkinter.Checkbutton(
    frame_options, text='Open CSV after export',
    underline=3, variable=var_bool_open)
cb_open.select()
cb_open.grid(row=5, column=0, sticky='w')

var_bool_save = tkinter.BooleanVar()
cb_save = tkinter.Checkbutton(
    frame_options, text='Save last used settings',
    underline=0, variable=var_bool_save)
cb_save.deselect()
cb_save.grid(row=6, column=0, sticky='w')

btn_default = tkinter.Button(
    frame_options, text='Restore default settings', underline=8,
    takefocus=True
)
btn_default.grid(row=7, column=0, sticky='w')


# Functions
def focus_off():
    label_guide.focus_set()


def choose_bl(*event):
    path = cf_scripts.ls_from_tuple_str(var_str_bl.get())[0]
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = None
    f_bl = tkinter.filedialog.askopenfilenames(
        filetypes=ext_bl, initialdir=initial_dir)
    if f_bl:
        var_str_bl.set(f_bl)
    if f_bl and not var_str_result.get():
        var_str_result.set(
            cf_scripts.dir_from_str_path(
                cf_scripts.ls_from_tuple_str(var_str_bl.get())[0])
                + '/' + fn_result)
    focus_off()


def choose_terms(*event):
    path = cf_scripts.ls_from_tuple_str(var_str_terms.get())[0]
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = None
    if var_bool_function.get():
        extensions = ext_function
    else:
        extensions = ext_terms
    f_terms = tkinter.filedialog.askopenfilenames(
        filetypes=extensions, initialdir=initial_dir)
    if f_terms:
        var_str_terms.set(f_terms)
    focus_off()


def choose_result(*event):
    if btn_result['state'] == 'disabled':
        return
    path = var_str_result.get()
    if path:
        initial_dir = cf_scripts.dir_from_str_path(path)
    else:
        initial_dir = cf_scripts.dir_from_str_path(
            cf_scripts.ls_from_tuple_str(var_str_bl.get()))
    f_result = tkinter.filedialog.asksaveasfilename(
        filetypes=ext_result, initialdir=initial_dir,
        initialfile=fn_result)
    if f_result:
        var_str_result.set(f_result)
    focus_off()


def turn_off_function():
    btn_terms.config(text='Terms', underline=0)
    path_saved_function.set(var_str_terms.get())
    if path_saved_terms.get():
        var_str_terms.set(path_saved_terms.get())
    else:
        var_str_terms.set('')


def turn_on_function():
    btn_terms.config(text='Funct.', underline=4)
    path_saved_terms.set(var_str_terms.get())
    if path_saved_function.get():
        var_str_terms.set(path_saved_function.get())
    else:
        var_str_terms.set('')


def toggle_cb_function(*event):
    if root.focus_get() == cb_function or dict_cb_hover['function']:
        pass
    else:
        cb_function.toggle()

    if not var_bool_function.get():
        turn_off_function()
    elif var_bool_function.get():
        turn_on_function()


def turn_on_export():
    path_saved_result.set(var_str_result.get())
    var_str_result.set(ph_cp_only)
    btn_result['state'] = 'disabled'


def turn_off_export():
    if path_saved_result.get():
        var_str_result.set(path_saved_result.get())
    elif not path_saved_result.get() and var_str_bl.get():
        path_1 = cf_scripts.ls_from_tuple_str(var_str_bl.get())[0]
        var_str_result.set(
            cf_scripts.dir_from_str_path(path_1) + '/' + fn_result)
    else:
        var_str_result.set('')
    btn_result['state'] = 'normal'


def toggle_cb_export(*event):
    if root.focus_get() == cb_export or dict_cb_hover['export']:
        pass
    else:
        cb_export.toggle()

    if var_bool_export.get():
        turn_on_export()
    elif not var_bool_export.get():
        turn_off_export()


def enable_folder_btn_if(statement, btn):
    if statement:
        btn.config(text='➔', state='normal')
    else:
        btn.config(text='⇨', state='disabled')


def enable_folder_bl_if_filled(var, unknown, w):
    enable_folder_btn_if(var_str_bl.get(), btn_folder_bl)


def enable_folder_terms_if_filled(var, unknown, w):
    enable_folder_btn_if(var_str_terms.get(), btn_folder_terms)


def enable_folder_result_if_filled(var, unknown, w):
    statement = var_str_result.get() and var_str_result.get() != ph_cp_only
    enable_folder_btn_if(statement, btn_folder_result)


three_open_funcs = [
    enable_folder_bl_if_filled, enable_folder_terms_if_filled,
    enable_folder_result_if_filled]

for var, btn, func in zip(three_vars, three_folder_buttons, three_open_funcs):
    btn.grid(row=three_folder_buttons.index(btn), column=4)
    var.trace('w', func)


def select_and_focus(event):
    event.widget.select()
    event.widget.focus()


def turn_on_options(widget):
    widget.config(text='▲', font=('', 12))
    frame_options.grid(
        row=4, column=0, columnspan=4, sticky='w', padx=30
    )


def turn_off_options(widget):
        widget.config(text='⚙', font=('', 15))
        frame_options.grid_forget()


def toggle_options(widget):
    if widget['text'] == '⚙':
        turn_on_options(widget)
    elif widget['text'] == '▲':
        turn_off_options(widget)


def toggle_cb_open(*event):
    if root.focus_get() == cb_open or dict_cb_hover['open']:
        pass
    else:
        cb_open.toggle()


def toggle_cb_save(*event):
    if root.focus_get() == cb_save or dict_cb_hover['save']:
        pass
    else:
        cb_save.toggle()


def get_options():
    dict_options = {
        'bool_function': var_bool_function.get(),
        'bool_export': var_bool_export.get(),
        'str_rate': var_str_rate.get(),
        'str_locked': var_str_locked.get(),
        'bool_open': var_bool_open.get(),
        'bool_save': var_bool_save.get()
    }
    return dict_options


def restore_default(*event):
    var_bool_function.set(0)
    var_bool_export.set(1)
    var_str_rate.set('all')
    var_str_locked.set('all')
    var_bool_open.set(1)
    var_bool_save.set(0)


def set_if_in_dict(dicionary, key, var):
    loaded = cf_scripts.return_if_in_dict(dicionary, key)
    if loaded:
        var.set(loaded)


def load_options():
    message_not_loaded = 'Saved options are not loaded.'
    if not os.path.exists(fn_options):
        print(message_not_loaded)
        return

    f_loaded_options = open(fn_options, 'rb')
    dict_loaded = pickle.load(f_loaded_options)
    f_loaded_options.close()

    if not cf_scripts.return_if_in_dict(dict_loaded, 'bool_save'):
        print(message_not_loaded)
        return
    else:
        turn_on_options(btn_options)
        set_if_in_dict(dict_loaded, 'bool_function', var_bool_function)
        set_if_in_dict(dict_loaded, 'bool_export', var_bool_export)
        set_if_in_dict(dict_loaded, 'str_rate', var_str_rate)
        set_if_in_dict(dict_loaded, 'str_locked', var_str_locked)
        set_if_in_dict(dict_loaded, 'bool_open', var_bool_open)
        set_if_in_dict(dict_loaded, 'bool_save', var_bool_save)
        if not var_bool_export.get():
            turn_off_export()
        print('Saved options are loaded.')


def save_options():
    dict_options = get_options()
    f_to_save_options = open(fn_options, 'wb')
    pickle.dump(dict_options, f_to_save_options)
    f_to_save_options.close()


def run(*event):
    if btn_run['state'] == 'disabled':
        return
    dict_options = get_options()
    cf_scripts.check_forbidden_terms(
        var_str_bl.get(), var_str_terms.get(), var_str_result.get(), dict_options)


def enable_run_if_filled(var, unknown, w):
    if var_str_bl.get() and var_str_terms.get() and var_str_result.get():
        btn_run.config(state='normal', text='Run!')
    else:
        btn_run.config(state='disabled', text='Run')


for var in three_vars:
    var.trace('w', enable_run_if_filled)

# Binding
three_funcs = [choose_bl, choose_terms, choose_result]
for i in range(3):
    three_buttons[i]['command'] = three_funcs[i]

for ent in three_entries:
    ent.bind('<Leave>', lambda x: focus_off())

btn_folder_bl['command'] = lambda: cf_scripts.open_folder(var_str_bl.get())
btn_folder_terms['command'] = lambda: cf_scripts.open_folder(var_str_terms.get())
btn_folder_result['command'] = lambda: cf_scripts.open_folder(var_str_result.get())

btn_options['command'] = lambda: toggle_options(btn_options)
btn_run['command'] = run

cb_function['command'] = toggle_cb_function
cb_export['command'] = toggle_cb_export

for rb in rbs_rate + rbs_locked:
    rb.bind('<ButtonRelease-1>', select_and_focus)

btn_readme['command'] = cf_scripts.open_readme
btn_update['command'] = cf_scripts.check_updates

cb_open['command'] = toggle_cb_open
cb_save['command'] = toggle_cb_save
btn_default['command'] = restore_default


guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Target (NG), Index, Source, Target (OK), etc.'
guide_result = 'Can be an existing file. Results are added to the bottom.'
guide_folder = 'Open the folder.'
guide_function = 'function(int_id, str_target) that returns a 2D list or None'
guide_export = 'Select this Check box if you don\'t export the CSV file.'
guide_options = 'Show or hide Options.'
guide_run = 'Enabled when all the three fields are filled. (Return key)'

ul_no = -1
ul_function = 0
ul_export = 12
ul_options = 13


def show_guide(event, guide, underline):
    label_guide.config(text=guide, underline=underline)


def hide_guide(*event):
    label_guide.config(text='', underline=ul_no)


def bind_show_guide(btn, guide, underline):
    btn.bind('<Enter>', lambda x: show_guide('<Enter>', guide, underline))


bind_show_guide(btn_bl, guide_bl, ul_no)
bind_show_guide(btn_terms, guide_terms, ul_no)
bind_show_guide(btn_result, guide_result, ul_no)
for btn in three_folder_buttons:
    bind_show_guide(btn, guide_folder, ul_no)
bind_show_guide(btn_options, guide_options, ul_options)
bind_show_guide(btn_run, guide_run, ul_no)

for btn in all_guided_ui:
    btn.bind('<Leave>', hide_guide)


def enter_cb_function(*event):
    dict_cb_hover['function'] = True
    show_guide('<Enter>', guide_function, ul_function)


def leave_cb_function(*event):
    dict_cb_hover['function'] = False
    hide_guide('<Leave>')


def enter_cb_export(*event):
    dict_cb_hover['export'] = True
    show_guide('<Enter>', guide_export, ul_export)


def leave_cb_export(*event):
    dict_cb_hover['export'] = False
    hide_guide('<Leave>')


def enter_cb_open(*event):
    dict_cb_hover['open'] = True


def leave_cb_open(*event):
    dict_cb_hover['open'] = False


def enter_cb_save(*event):
    dict_cb_hover['save'] = True


def leave_cb_save(*event):
    dict_cb_hover['save'] = False


all_cbs = [cb_function, cb_export, cb_open, cb_save]
all_keys = ['function', 'export', 'open', 'save']
all_enter_funcs = [
    enter_cb_function, enter_cb_export, enter_cb_open, enter_cb_save
]
all_leave_funcs = [
    leave_cb_function, leave_cb_export, leave_cb_open, leave_cb_save
]

for cb, key, enter, leave in zip(all_cbs, all_keys, all_enter_funcs, all_leave_funcs):
    cb.bind('<Enter>', enter)
    cb.bind('<Leave>', leave)


def sc_only_when_out_of_ent(func):
    if type(frame_main.focus_get()) == tkinter.Entry:
        pass
    else:
        func('')


def bind_keys(key, func):
    root.bind(key, lambda x: sc_only_when_out_of_ent(func))


bind_keys('<Return>', run)
bind_keys('o', lambda x: toggle_options(btn_options))
bind_keys('b', choose_bl)
bind_keys('t', choose_terms)
bind_keys('r', choose_result)
bind_keys('f', toggle_cb_function)
bind_keys('c', toggle_cb_export)
bind_keys('m', cf_scripts.open_readme)
bind_keys('u', cf_scripts.check_updates)
bind_keys('a', lambda x: rbs_rate[0].select())
bind_keys('1', lambda x: rbs_rate[1].select())
bind_keys('0', lambda x: rbs_rate[2].select())
bind_keys('i', lambda x: rbs_locked[0].select())
bind_keys('e', lambda x: rbs_locked[1].select())
bind_keys('n', lambda x: cb_open.toggle())
bind_keys('s', lambda x: cb_save.toggle())
bind_keys('d', restore_default)


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
