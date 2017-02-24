'''
cd dropbox/codes/check_forbidden
py -B cf_scripts.py
'''
import setup
import csv
import datetime
import importlib
import locale
import os
import os.path
import re
import subprocess
import sys
import time
import urllib.request as ur
import webbrowser
import zipfile


def apply_update(download_path):
    print('Starting the installer...')
    print('You may have to close the current process to continue.')
    if sys.platform.startswith('win'):
        os.startfile(download_path)
    else:
        subprocess.call(['open', download_path])


def cleanup_if_mqxlz(fn_bl):
    if fn_bl[-5:] == 'mqxlz':
        path_extract = dirname_from_fname(fn_bl) + '_extract'
        os.remove(path_extract + '/document.mqxliff')
        try_rmdir(path_extract)


def convert_non_encodable(char):
    encoding_for_output = locale.getpreferredencoding()
    if char.encode(encoding_for_output, errors='ignore'):
        return char
    else:
        return '*'


def download_installer(str_newest_version, url_installer):
    print('Downloading the newest version:', str_newest_version)
    print('Your version is', setup.dict_console['version'])
    download_folder = os.path.expanduser("~") + '/downloads/'
    download_path = download_folder + url_installer.group(2)
    d = ur.urlopen('https://github.com/' + url_installer.group(0))
    with open(download_path, 'wb') as f:
        f.write(d.read())
    return download_path


def check_updates(download_function=download_installer):
    print('-' * 70)
    url_releases = 'https://github.com/ShunSakurai/check_forbidden/releases'
    try:
        str_release_page = str(ur.urlopen(url_releases).read())
    except:
        print('Check Forbidden could not connect to', url_releases)
        return
    pattern_version = re.compile(r'(?<=<span class="css-truncate-target">v)[0-9.]+(?=</span>)')
    pattern_installer = re.compile(r'/ShunSakurai/check_forbidden/releases/download/v([0-9.]+)/(check_forbidden_installer_\1.0.exe)')
    str_newest_version = pattern_version.search(str_release_page).group(0)
    url_installer = pattern_installer.search(str_release_page)
    if installed_version_is_newer(setup.dict_console['version'], str_newest_version):
        print('You are using the newest version:', setup.dict_console['version'])
    else:
        download_path = download_function(str_newest_version, url_installer)
        apply_update(download_path)
        print('Preparing to delete the installer...')
        try_removing_if_not_in_use(
            download_path, 'The installer was successfully deleted.',
            'Please go to the downloads folder and delete the installer manually.'
        )


def dir_from_str_path(str_path):
    r'''
    >>> dir_from_str_path('C:\\check_forbidden\\files\\Test.mqxlz')
    'C:/check_forbidden/files'
    '''
    if not isinstance(str_path, str):
        return ''
    str_path = str_path.replace('\\', '/')
    if str_path.endswith('/'):
        str_path_dir = str_path.rstrip('/')
    elif '.' in str_path.rsplit('/', 1)[-1]:
        str_path_dir = str_path.rsplit('/', 1)[0]
    else:
        str_path_dir = str_path
    return str_path_dir


def dirname_from_fname(fname):
    dir_name = fname.rsplit('.', 1)[0]
    return dir_name


def fname_from_str_path(str_path):
    f_name = str_path.rsplit('/', 1)[-1]
    return f_name


def installed_version_is_newer(str_installed, str_online):
    list_installed = str_installed.split('.')
    list_online = str_online.split('.')
    for i in range(3):
        if int(list_installed[i]) < int(list_online[i]):
            return False
        elif int(list_installed[i]) > int(list_online[i]):
            return True
        else:
            pass
    return True


def limit_header_range(header, dict_options):
    regex_id = re.compile('(?<=trans-unit id=")\d+(?=")')
    string_102 = 'mq:percent="102"'
    string_101 = 'mq:percent="101"'
    string_100 = 'mq:percent="100"'
    string_locked = 'mq:locked="locked"'
    seg_id = regex_id.search(header).group(0)
    if dict_options['str_rate'] == '100' and string_100 in header:
        return seg_id, False
    elif dict_options['str_rate'] == '100' and string_101 in header:
        return seg_id, False
    elif dict_options['str_rate'] == '101' and string_101 in header:
        return seg_id, False
    elif dict_options['str_rate'] == '101' and string_102 in header:
        return seg_id, False
    elif dict_options['str_locked'] == 'locked' and string_locked in header:
        return seg_id, False
    else:
        return seg_id, True


def ls_from_list_str(x):
    r'''
    >>> ls_from_list_str("['Index', 'Source', 'Target (NG)', 'Target (OK)']")
    ['Index', 'Source', 'Target (NG)', 'Target (OK)']

    >>> ls_from_list_str('Mere string')
    ['Mere string']
    '''
    list_from_str = [i.strip('\'') for i in x.strip('[]').split(', ')]
    return list_from_str


def ls_from_tuple_str(tuple_str):
    r'''
    >>> ls_from_tuple_str(r'/Users/path/mqxliff.mqxliff {/Users/path/mqxlz.mqxlz}')
    ['/Users/path/mqxliff.mqxliff', '/Users/path/mqxlz.mqxlz']

    >>> ls_from_tuple_str(r' C:/Users/path/mqxliff1.mqxliff {C:/Users/path/mqxliff2.mqxliff} {C:\Users\path\mqxlz1.mqxlz} {C:\Users\path\mqxlz2.mqxlz}')
    ['C:/Users/path/mqxliff1.mqxliff', 'C:/Users/path/mqxliff2.mqxliff', 'C:\\Users\\path\\mqxlz1.mqxlz', 'C:\\Users\\path\\mqxlz2.mqxlz']
    '''
    tuple_str_split = tuple_str.replace('{', ',').strip('(),').split(',')
    list_from_str = [i.strip(' {},"\'') for i in tuple_str_split]
    return list_from_str


def open_file(str_file_path):
    print('Opening the file...')
    if sys.platform.startswith('win'):
        os.startfile(str_file_path)
    else:
        subprocess.call(['open', str_file_path])


def open_folder(tuple_path):
    if tuple_path and tuple_path != 'Command Prompt only.':
        str_path_1 = ls_from_tuple_str(tuple_path)[0]
        str_path_dir = dir_from_str_path(str_path_1)
        if sys.platform.startswith('win'):
            os.startfile(str_path_dir)
        else:
            subprocess.call(['open', str_path_dir])


def open_readme():
    webbrowser.open_new_tab(
        'https://github.com/ShunSakurai/check_forbidden/blob/master/README.md')


def print_and_append(to_print, to_write, file_to_write_in, dict_options):
    try_printing(to_print)
    if dict_options['str_method'] == '0':
        file_to_write_in.append(to_write)
    else:
        pass


def print_and_append_metadata(f_result_w, fpath_terms, dict_options):
    print('-' * 70)
    date_time_version = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S v') + setup.dict_console['version']
    print_and_append(
        'Time and version: ' + date_time_version,
        [date_time_version], f_result_w, dict_options)
    list_name = fname_from_str_path(fpath_terms)
    if dict_options['str_function'] == '0':
        f_terms = open(fpath_terms, encoding='utf-8')
        header = f_terms.readline().rstrip('\n')
        f_terms.close()
        print_and_append('Terms: ' + list_name, [list_name], f_result_w, dict_options)
    else:
        print_and_append('Function: ' + list_name, [list_name], f_result_w, dict_options)
    settings = str_from_settings(dict_options)
    print_and_append('Options: ' + settings, [settings], f_result_w, dict_options)
    if dict_options['str_function'] == '0':
        print_and_append(
            'Header: [' + header + '] + Segment Number',
            header.split(',') + ['ID', 'Target'] , f_result_w, dict_options)
    print('-' * 70)


def remove_tags(segment):
    regex_tag = re.compile('<[^/].*?>.*?</.*?>', re.S)
    segment_clean = regex_tag.sub('', segment)
    return segment_clean


def replace_back_slash(str_path):
    return str_path.replace('\\', '/')


def str_from_settings(dict_options):
    if dict_options['str_rate'] == 'all':
        setting_rate = 'Check all match rates'
    elif dict_options['str_rate'] == '101':
        setting_rate = r'Exclude 101% matches'
    elif dict_options['str_rate'] == '100':
        setting_rate = r'Exclude 100% / 101%'
    if dict_options['str_locked'] == 'all':
        setting_locked = 'Include locked segments'
    else:
        setting_locked = 'Exclude locked segments'
    settings = setting_rate + '; ' + setting_locked
    return settings


def try_printing(to_print):
    try:
        print(to_print)
    except UnicodeError:
        to_print_encodable = ''.join([convert_non_encodable(i) for i in to_print])
        try:
            print(to_print_encodable)
        except:
            print('**Error occurred in printing characters.**')
    except:
        print('**Error occurred in printing characters.**')
        print(sys.exc_info()[1], '\n', sys.exc_info()[0])


def try_rmdir(i):
    try:
        os.rmdir(i)
    except:
        try:
            time.sleep(0.01)
            os.rmdir(i)
        except:
            print('Please go to the bilingual file location and delete the _extract folder manually.')


def try_removing_if_not_in_use(path_file, message_success, message_fail):
    if not sys.platform.startswith('win'):
        print(message_fail)
        return
    try:
        while True:
            try:
                time.sleep(5)
                os.remove(path_file)
                print(message_success)
                break
            except:
                time.sleep(5)
    except:
        print(message_fail)


def unzip_if_mqxlz(fn_bl):
    if fn_bl[-5:] == 'mqxlz':
        path_extract = dirname_from_fname(fn_bl) + '_extract'
        fn_actual = zipfile.ZipFile(fn_bl).extract(
            'document.mqxliff', path=path_extract)
        return fn_actual
    else:
        return fn_bl


def check_for_each_term(list_fn_bl_tuple, fpath_terms, fpath_result, dict_options):
    f_result_w = []
    list_matched_rows = []
    print_and_append_metadata(f_result_w, fpath_terms, dict_options)
    regex_pattern = re.compile(
        '(?<=<target xml:space="preserve">).*?(?=</target>)', re.S)
    for fn_bl_tuple in list_fn_bl_tuple:
        f_result_w.append([''])
        print_and_append(fn_bl_tuple[0], [fn_bl_tuple[0]], f_result_w, dict_options)
        f_bl = open(fn_bl_tuple[1], encoding='utf-8')
        f_bl_line_range_list = []
        not_historical = True
        for f_bl_line in f_bl:
            if '<mq:historical-unit ' in f_bl_line:
                not_historical = False
            elif '</mq:historical-unit>' in f_bl_line:
                not_historical = True
            elif f_bl_line.startswith('<trans-unit id="') and not_historical:
                seg_id, is_range = limit_header_range(f_bl_line, dict_options)
            elif f_bl_line.startswith('<target xml:space="preserve">') and not_historical:
                if is_range:
                    while '</target>' not in f_bl_line:
                        f_bl_line += next(f_bl)
                    f_bl_line_with_tag = regex_pattern.search(f_bl_line).group(0)
                    if f_bl_line_with_tag:
                        f_bl_line_clean = remove_tags(f_bl_line_with_tag)
                        f_bl_line_range_list.append((seg_id, f_bl_line_clean))
            else:
                continue

        f_terms = open(fpath_terms, encoding='utf-8')
        f_terms_read = csv.reader(f_terms)
        if dict_options['str_function'] == '0':
            for row in f_terms_read:
                if not row or row[0] is None:
                    continue
                else:
                    pass
                for seg_id, line in f_bl_line_range_list:
                    match = re.search(row[0], line)
                    if match:
                        print_and_append(str(row), row + [seg_id, line], f_result_w, dict_options)
                        print(seg_id)
                        try_printing(line + '\n')
                        list_matched_rows.append(row)
                    else:
                        continue
        else:
            mdir, mfile = fpath_terms.rsplit('/', 1)
            mname = mfile.rsplit('.', 1)[0]
            sys.path.append(mdir)
            external_script = importlib.import_module(mname)
            for (seg_id, target) in f_bl_line_range_list:
                result = external_script.function(seg_id, target)
                if result:
                    for ls in result:
                        print_and_append(ls, ls, f_result_w, dict_options)
                        list_matched_rows.append(ls)
        print('\n')
        f_bl.close()

    f_terms.close()

    if list_matched_rows and dict_options['str_function'] == '0':
        f_result_w.append([''])
        print_and_append('Summary', ['Summary'], f_result_w, dict_options)
        list_reduced = []
        for i in range(len(list_matched_rows)):
            if str(list_matched_rows[i]) not in list_reduced:
                list_reduced.append(str(list_matched_rows[i]))
        for i in list_reduced:
            print_and_append(i, ls_from_list_str(i), f_result_w, dict_options)
        print_and_append('', [''], f_result_w, dict_options)
    elif dict_options['str_function'] == '0':
        print('No forbidden term was found!')

    if list_matched_rows and dict_options['str_method'] == '0':
        f_result = open(fpath_result, 'a', encoding='utf-8-sig')
        f_result_wc = csv.writer(f_result, lineterminator='\n')
        f_result_wc.writerows(f_result_w)
        f_result.close()
        print(fname_from_str_path(fpath_result), 'was successfully created.')
    elif list_matched_rows and dict_options['str_method'] == '1':
        print('The search was successfully finished.')
    if list_matched_rows and dict_options['str_function'] == '0':
        print(str(len(list_matched_rows)), 'matches.')


def check_forbidden_terms(tuple_str_bl, tuple_str_terms, str_result, dict_options):
    # For testing
    dict_options = dict_options or {
        'str_function': '0', 'str_method': '1',
        'str_rate': 'all', 'str_locked': 'all',
        'str_open': '1', 'str_load': '0'
    }
    start = time.time()
    list_fpath_bl = ls_from_tuple_str(tuple_str_bl)
    list_fpath_terms = ls_from_tuple_str(tuple_str_terms)
    fpath_result = replace_back_slash(str_result)

    list_fn_bl_tuple = []
    for fn_bl in list_fpath_bl:
        fn_actual = replace_back_slash(unzip_if_mqxlz(fn_bl))
        list_fn_bl_tuple.append((fn_bl, fn_actual))

    for fpath_terms in list_fpath_terms:
        check_for_each_term(
            list_fn_bl_tuple, fpath_terms, fpath_result, dict_options
        )

    for fn_bl in list_fpath_bl:
        cleanup_if_mqxlz(fn_bl)

    elapsed = time.time() - start
    print(str(elapsed)[:10], 'seconds.\n\n')

    if dict_options['str_method'] == '0' and dict_options['str_open'] == '1':
        open_file(str_result)


def ask_quit(frame):
    print('Click [x] on the tk window or press [Enter] on this screen to exit.')
    try:
        input('\n')
    except:
        pass
    frame.quit()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
