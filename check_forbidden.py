'''
cd /d z:
cd dropbox/codes/check_forbidden
py -B check_forbidden.py
'''
import cf_scripts
import setup
import datetime
import os
import pickle
import sys
import tkinter
import tkinter.filedialog
import tkinter.messagebox

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
ext_result = [('html', '*.html')]
fn_result = 'checked_result.html'

ph_cp_only = 'Command Prompt only. Uncheck to export the results.'
if sys.platform.startswith('win'):
    fn_options = os.getenv('APPDATA') + r'\Check Forbidden\cf_options.p'
else:
    fn_options = 'cf_options.p'

dict_cb_hover = {
    'function': False,
    'export': False
}

# Widgets
btn_bl = tkinter.Button(text='Billingual', underline=0)
btn_terms = tkinter.Button(text='Terms', underline=0)
btn_result = tkinter.Button(text='Result', underline=0)
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
cb_export.deselect()
cb_export.grid(row=2, column=1, sticky='e')

var_str_bl = tkinter.StringVar(frame_main)
var_str_terms = tkinter.StringVar(frame_main)
var_str_result = tkinter.StringVar(frame_main)
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

btn_clear = tkinter.Button(text='✗', borderwidth=0, font=('', 15))
btn_clear.grid(row=3, column=3, sticky='e', padx=50)

btn_run = tkinter.Button(text='Run', state='disabled', takefocus=True)
btn_run.grid(row=3, column=3, sticky='e', padx=15, pady=5)

all_guided_ui = three_buttons + three_folder_buttons + [
    cb_function, cb_export, btn_options, btn_clear, btn_run]

frame_options = tkinter.Frame(root, pady=5)

label_exclude = tkinter.Label(frame_options, text='\tExclude')

var_bool_ex_101 = tkinter.BooleanVar()
cb_ex_101 = tkinter.Checkbutton(
    frame_options, text='101% matches',
    underline=2, variable=var_bool_ex_101
)
cb_ex_101.deselect()

var_bool_ex_100 = tkinter.BooleanVar()
cb_ex_100 = tkinter.Checkbutton(
    frame_options, text='100% matches',
    underline=2, variable=var_bool_ex_100
)
cb_ex_100.deselect()

var_bool_ex_locked = tkinter.BooleanVar()
cb_ex_locked = tkinter.Checkbutton(
    frame_options, text='Locked',
    underline=0, variable=var_bool_ex_locked
)
cb_ex_locked.deselect()

var_bool_ex_same = tkinter.BooleanVar()
cb_ex_same = tkinter.Checkbutton(
    frame_options, text='Same as source',
    underline=0, variable=var_bool_ex_same
)
cb_ex_same.deselect()

label_exclude.grid(row=0, column=0, sticky='w')
cb_ex_101.grid(row=1, column=0, sticky='w', padx=20)
cb_ex_100.grid(row=2, column=0, sticky='w', padx=20)
cb_ex_locked.grid(row=3, column=0, sticky='w', padx=20)
cb_ex_same.grid(row=4, column=0, sticky='w', padx=20)


label_settings = tkinter.Label(frame_options, text='\tOther settings')

var_bool_open = tkinter.BooleanVar()
cb_open = tkinter.Checkbutton(
    frame_options, text='Open HTML after export',
    underline=3, variable=var_bool_open)
cb_open.select()

var_bool_save = tkinter.BooleanVar()
cb_save = tkinter.Checkbutton(
    frame_options, text='Save last used settings',
    underline=2, variable=var_bool_save)
cb_save.deselect()

btn_default = tkinter.Button(
    frame_options, text='Restore settings to default', underline=20,
    takefocus=True
)

label_settings.grid(row=0, column=1, sticky='w')
cb_open.grid(row=1, column=1, sticky='w', padx=20)
cb_save.grid(row=2, column=1, sticky='w', padx=20)
btn_default.grid(row=3, column=1, sticky='w', padx=20)


label_about = tkinter.Label(frame_options, text='\tAbout')

label_version = tkinter.Label(
    frame_options, text=''.join([
        'Version ', setup.dict_console['version']
    ]), justify='left')
label_author = tkinter.Label(
    frame_options, text=''.join([
        '©2016-', str(datetime.date.today().year), ' ', setup.dict_console['author']
    ]), justify='left')
btn_readme = tkinter.Button(frame_options, text='Read readme', underline=9)
btn_update = tkinter.Button(frame_options, text='Check for updates', underline=10)

label_about.grid(row=0, column=2, sticky='w')
label_version.grid(row=1, column=2, sticky='w', padx=20)
label_author.grid(row=2, column=2, sticky='w', padx=20)
btn_readme.grid(row=3, column=2, sticky='w', padx=20)
btn_update.grid(row=4, column=2, sticky='w', padx=20)


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


def clear_fields():
    var_str_bl.set('')
    var_str_terms.set('')
    if not btn_result['state'] == 'disabled':
       var_str_result.set('')
    path_saved_terms.set('')
    path_saved_function.set('')
    path_saved_result.set('')


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

    if var_bool_function.get():
        turn_on_function()
    else:
        turn_off_function()


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
    else:
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


def turn_on_options(widget):
    widget.config(text='▼', font=('', 12))
    frame_options.grid(
        row=4, column=0, columnspan=4, sticky='w', padx=20
    )


def turn_off_options(widget):
        widget.config(text='⚙', font=('', 15))
        frame_options.grid_forget()


def toggle_options(widget):
    if widget['text'] == '⚙':
        turn_on_options(widget)
    elif widget['text'] == '▼':
        turn_off_options(widget)


def get_options():
    dict_options = {
        'bool_function': var_bool_function.get(),
        'bool_export': var_bool_export.get(),
        'bool_ex_101': var_bool_ex_101.get(),
        'bool_ex_100': var_bool_ex_100.get(),
        'bool_ex_locked': var_bool_ex_locked.get(),
        'bool_ex_same': var_bool_ex_same.get(),
        'bool_open': var_bool_open.get(),
        'bool_save': var_bool_save.get()
    }
    return dict_options


def disable_101_when_100(var, unknown, w):
    if var_bool_ex_100.get():
        cb_ex_101['state'] = 'disabled'
    else:
        cb_ex_101['state'] = 'normal'


def disable_open_when_result(var, unknown, w):
    if var_bool_export.get():
        cb_open['state'] = 'disabled'
    else:
        cb_open['state'] = 'normal'


var_bool_ex_100.trace('w', disable_101_when_100)
var_bool_export.trace('w', disable_open_when_result)


def restore_default(*event):
    if var_bool_function.get():
        toggle_cb_function()
    if var_bool_export.get():
        toggle_cb_export()
    var_bool_function.set(False)
    var_bool_export.set(False)
    var_bool_ex_101.set(False)
    var_bool_ex_100.set(False)
    var_bool_ex_locked.set(False)
    var_bool_ex_same.set(False)
    var_bool_open.set(True)
    var_bool_save.set(False)


def set_if_in_dict(dictionary, key, var):
    loaded = cf_scripts.return_if_in_dict(dictionary, key)
    if loaded is not None:
        var.set(loaded)


def load_options():
    message_loaded = 'Saved options have been loaded.'
    message_not_loaded = 'Saved options have not been loaded.'
    if not os.path.exists(fn_options):
        print(message_not_loaded)
        return

    with open(fn_options, 'rb') as f_loaded_options:
        try:
            dict_loaded = pickle.load(f_loaded_options)
        except:
            os.remove(fn_options)
            print(message_not_loaded)
            return

    if not cf_scripts.return_if_in_dict(dict_loaded, 'bool_save'):
        print(message_not_loaded)
        return
    else:
        turn_on_options(btn_options)
        set_if_in_dict(dict_loaded, 'bool_function', var_bool_function)
        set_if_in_dict(dict_loaded, 'bool_export', var_bool_export)
        set_if_in_dict(dict_loaded, 'bool_ex_101', var_bool_ex_101)
        set_if_in_dict(dict_loaded, 'bool_ex_100', var_bool_ex_100)
        set_if_in_dict(dict_loaded, 'bool_ex_locked', var_bool_ex_locked)
        set_if_in_dict(dict_loaded, 'bool_ex_same', var_bool_ex_same)
        set_if_in_dict(dict_loaded, 'bool_open', var_bool_open)
        set_if_in_dict(dict_loaded, 'bool_save', var_bool_save)
        if var_bool_function.get():
            turn_on_function()
        if var_bool_export.get():
            turn_on_export()
        print(message_loaded)


def save_options():
    dict_options = get_options()
    with open(fn_options, 'wb') as f_to_save_options:
        pickle.dump(dict_options, f_to_save_options)


def ask_question(title, message):
    answer = tkinter.messagebox.askquestion(title, message)
    return answer == 'yes'


def display_toast(message, also_print=False):
    if also_print:
        print(message)
    toast_tk = tkinter.Tk()
    toast_message = tkinter.Message(toast_tk, text=message)
    toast_message.pack()
    # destroy works but quit doesn't
    alarm_id = toast_tk.after(3000, toast_tk.destroy)
    toast_tk.protocol(
        'WM_DELETE_WINDOW',
        lambda: (toast_tk.after_cancel(alarm_id), toast_tk.quit())
    )
    toast_tk.mainloop()


def main(tuple_str_bl, tuple_str_terms, str_result, dict_options):
    message_no_export = 'The search was successfully finished.'
    message_no_result = 'No forbidden term was found!'
    snippet_file_created = ' was successfully created.'
    f_result_w, fpath_result, list_fpath_bl = cf_scripts.check_forbidden_terms(
            tuple_str_bl, tuple_str_terms, str_result, dict_options)
    for fn_bl in list_fpath_bl:
        cf_scripts.cleanup_if_mqxlz(fn_bl)

    if not f_result_w:
        display_toast(message_no_result, also_print=True)
    else:
        if dict_options['bool_export']:
            display_toast(message_no_export, also_print=True)
        else:
            file_existing = os.path.exists(fpath_result)
            if file_existing:
                overwrite_file = ask_question(
                    'Warning', 'Overwrite ' + fpath_result + '?')
                if not overwrite_file:
                    display_toast(message_no_export, also_print=True)
            if not file_existing or overwrite_file:
                fname_result = cf_scripts.write_result(
                    f_result_w, fpath_result, dict_options)
                print('\n' + fname_result + snippet_file_created)

                if dict_options['bool_open']:
                    cf_scripts.open_file(fpath_result)
                elif not file_existing:
                    display_toast(fname_result + snippet_file_created)

    print('To exit, click [x].\n')


def run(*event):
    if btn_run['state'] == 'disabled':
        return
    dict_options = get_options()
    main(var_str_bl.get(), var_str_terms.get(), var_str_result.get(), dict_options)


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
btn_clear['command'] = clear_fields
btn_run['command'] = run

cb_function['command'] = toggle_cb_function
cb_export['command'] = toggle_cb_export

btn_default['command'] = restore_default

btn_readme['command'] = cf_scripts.open_readme
btn_update['command'] = cf_scripts.check_updates

guide_bl = '.mqxlz or .mqxliff'
guide_terms = 'Text or CSV: Target (NG), Index, Source, Target (OK), etc.'
guide_result = 'Export the result in a filterable and searchable HTML file.'
guide_folder = 'Open the folder.'
guide_function = 'function(int_id, str_target) that returns a 2D list or None'
guide_export = 'Select this check box if you don\'t Export the CSV file.'
guide_options = 'Show or hide Options.'
guide_clear = 'Clear all three fields.'
guide_run = 'Enabled when all the three fields are filled. (Alt + Return)'

ul_no = -1
ul_function = 0
ul_export = 35
ul_options = 13
ul_clear = 0


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
bind_show_guide(btn_clear, guide_clear, ul_clear)
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


for cb, enter, leave in zip(
    [cb_function, cb_export],
    [enter_cb_function, enter_cb_export],
    [leave_cb_function, leave_cb_export]
):
    cb.bind('<Enter>', enter)
    cb.bind('<Leave>', leave)


def toggle_101_if_enabled(*event):
    if cb_ex_101['state'] != 'disabled':
        cb_ex_101.toggle()


def toggle_open_if_enabled(*event):
    if cb_open['state'] != 'disabled':
        cb_open.toggle()


def bind_keys(key, func):
    root.bind(key, lambda x: func(''))
    if len(key) == 1 and key.upper() != key:
        root.bind(key.upper(), lambda x: func(''))


bind_keys('<Alt-Return>', run)
bind_keys('<Alt-c>', lambda x: clear_fields())
bind_keys('<Alt-o>', lambda x: toggle_options(btn_options))
bind_keys('<Alt-b>', choose_bl)
bind_keys('<Alt-t>', choose_terms)
bind_keys('<Alt-r>', choose_result)
bind_keys('<Alt-f>', toggle_cb_function)
bind_keys('<Alt-e>', toggle_cb_export)
bind_keys('<Alt-m>', cf_scripts.open_readme)
bind_keys('<Alt-u>', cf_scripts.check_updates)
bind_keys('<Alt-1>', toggle_101_if_enabled)
bind_keys('<Alt-0>', lambda x: cb_ex_100.toggle())
bind_keys('<Alt-l>', lambda x: cb_ex_locked.toggle())
bind_keys('<Alt-s>', lambda x: cb_ex_same.toggle())
bind_keys('<Alt-n>', toggle_open_if_enabled)
bind_keys('<Alt-v>', lambda x: cb_save.toggle())
bind_keys('<Alt-d>', restore_default)

# Initiating the program
if __name__ == "__main__":
    top = frame_main.winfo_toplevel()
    top.resizable(False, False)
    load_options()
    print('tk window is ready to use.')
    root.protocol('WM_DELETE_WINDOW', lambda: (save_options(), root.destroy()))
    frame_main.mainloop()
