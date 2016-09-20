'''
cd dropbox/codes/check_forbidden
py cf_scripts.py
'''
import setup
import csv
import datetime
import importlib
import os
import os.path
import re
import subprocess
import sys
import time
import urllib.request as ur
import webbrowser
import zipfile


def download_update(str_newest_version, url_installer):
    print('Downloading the newest version', str_newest_version)
    print('Your version is', setup.dict_console['version'])
    download_folder = os.path.expanduser("~")+'/downloads/'
    download_path = download_folder + url_installer.group(2)
    d = ur.urlopen('https://github.com/' + url_installer.group(0))
    with open(download_path, 'wb') as f:
        f.write(d.read())
    print('Starting the installer.')
    if sys.platform.startswith('win'):
        os.startfile(download_path)
    else:
        subprocess.call(['open', download_path])
    return


def check_updates(download_function=download_update):
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
        return
    else:
        download_function(str_newest_version, url_installer)


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
        if list_installed[i] < list_online[i]:
            return False
        else:
            pass
    return True


def limit_header_range(header, str_rate, str_locked):
    regex_id = re.compile('(?<=trans-unit id=")\d+(?=")')
    string_101 = 'mq:percent="101"'
    string_100 = 'mq:percent="100"'
    string_locked = 'mq:locked="locked"'
    seg_id = regex_id.search(header).group(0)
    if str_rate == '100' and string_100 in header:
        return seg_id, False
    elif str_rate == '100' and string_101 in header:
        return seg_id, False
    elif str_rate == '101' and string_101 in header:
        return seg_id, False
    elif str_locked == 'locked' and string_locked in header:
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


def mqxlz_dir_fname(fn):
    path_extract = dirname_from_fname(fn) + '_extract'
    fn_actual = zipfile.ZipFile(fn).extract(
        'document.mqxliff', path=path_extract)
    return path_extract, fn_actual


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


def print_and_append(str_method, to_print, to_write, file_to_write_in):
    try_printing(to_print)
    if str_method == '0':
        file_to_write_in.append(to_write)
    else:
        pass


def print_and_append_metadata(
    f_result_w, fpath_terms, str_function, str_method, str_rate, str_locked
):
    print('-' * 70)
    date_time_version = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S v') + setup.dict_console['version']
    print_and_append(
        str_method, 'Time and version: ' + date_time_version,
        [date_time_version], f_result_w)
    list_name = fname_from_str_path(fpath_terms)
    if str_function == '0':
        f_terms = open(fpath_terms, encoding='utf-8')
        header = f_terms.readline().rstrip('\n')
        f_terms.close()
        print_and_append(str_method, 'Terms: ' + list_name, [list_name], f_result_w)
    else:
        print_and_append(str_method, 'Function: ' + list_name, [list_name], f_result_w)
    settings = str_from_settings(str_rate, str_locked)
    print_and_append(str_method, 'Options: ' + settings, [settings], f_result_w)
    if str_function == '0':
        print_and_append(
            str_method, 'Header: [' + header + '] + Segment Number',
            header.split(',') + ['ID', 'Target'] , f_result_w)
    print('-' * 70)


def remove_tags(segment):
    regex_tag = re.compile('<[^/].*?>.*?</.*?>', re.S)
    segment_clean = regex_tag.sub('', segment)
    return segment_clean


def replace_back_slash(str_path):
    return str_path.replace('\\', '/')


def str_from_settings(str_rate, str_locked):
    if str_rate == 'all':
        setting_rate = 'Check all match rates'
    elif str_rate == '101':
        setting_rate = r'Exclude 101% matches'
    elif str_rate == '100':
        setting_rate = r'Exclude 100% / 101%'
    if str_locked == 'all':
        setting_locked = 'Include locked segments'
    else:
        setting_locked = 'Exclude locked segments'
    settings = setting_rate + ', ' + setting_locked
    return settings


def try_printing(to_print):
    try:
        print(to_print)
    except UnicodeError:
        special_char = re.compile(r'[^\w\s -~]| ')
        try:
            print(special_char.sub(' ', to_print))
        except:
            print('**Some special characters could not be printed.**')
    except:
        print('**Some special characters could not be printed.**')
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


def unzip_if_mqxlz(fn_bl, list_mqxlz_dir):
    if fn_bl[-5:] == 'mqxlz':
        list_mqxlz_dir.append(mqxlz_dir_fname(fn_bl)[0])
        return mqxlz_dir_fname(fn_bl)[1]
    else:
        return fn_bl


def check_forbidden_terms(
        frame, tuple_str_bl, str_terms, str_result,
        str_function, str_method, str_rate, str_locked):
    start = time.time()
    fn_bl_list = ls_from_tuple_str(tuple_str_bl)
    fpath_terms = replace_back_slash(str_terms)
    fpath_result = replace_back_slash(str_result)
    f_result_w = []
    list_mqxlz_dir = []
    list_found_rows = []
    regex_pattern = re.compile(
        '(?<=<target xml:space="preserve">).*?(?=</target>)', re.S)

    print_and_append_metadata(
        f_result_w, fpath_terms, str_function, str_method, str_rate, str_locked
    )

    for fn_bl in fn_bl_list:
        f_result_w.append([''])
        print_and_append(str_method, fn_bl, [fn_bl], f_result_w)
        fn_bl_actual = replace_back_slash(unzip_if_mqxlz(fn_bl, list_mqxlz_dir))
        f_bl = open(fn_bl_actual, encoding='utf-8')
        f_bl_line_range_list = []
        not_historical = True
        for f_bl_line in f_bl:
            if '<mq:historical-unit ' in f_bl_line:
                not_historical = False
            elif '</mq:historical-unit>' in f_bl_line:
                not_historical = True
            elif f_bl_line.startswith('<trans-unit id="') and not_historical:
                seg_id, is_range = limit_header_range(f_bl_line, str_rate, str_locked)
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
        if str_function == '0':
            for row in f_terms_read:
                if not row or row[0] is None:
                    continue
                else:
                    pass
                for seg_id, line in f_bl_line_range_list:
                    match = re.search(row[0], line)
                    if match:
                        print_and_append(
                            str_method, str(row) + '\t' + seg_id,
                            row + [seg_id, line], f_result_w)
                        try_printing(line)
                        list_found_rows.append(row)
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
                        print_and_append(str_method, ls, ls, f_result_w)
                        list_found_rows.append(ls)
        print('\n')
        f_bl.close()

    f_terms.close()

    if list_found_rows and str_function == '0':
        f_result_w.append([''])
        print_and_append(str_method, 'Summary', ['Summary'], f_result_w)
        list_reduced = list({str(i) for i in list_found_rows})
        for i in list_reduced:
            print_and_append(str_method, i, ls_from_list_str(i), f_result_w)
        print_and_append(str_method, '', [''], f_result_w)
    elif str_function == '0':
        print('No forbidden term was found!')

    # Delete the directories before exporting the results, which sometimes
    # causes an error to terminate the program
    if list_mqxlz_dir:
        for i in list_mqxlz_dir:
            os.remove(i + r'/document.mqxliff')
        for i in list_mqxlz_dir:
            try_rmdir(i)

    if list_found_rows and str_method == '0':
        f_result = open(fpath_result, 'a', encoding='utf-8-sig')
        f_result_wc = csv.writer(f_result, lineterminator='\n')
        f_result_wc.writerows(f_result_w)
        f_result.close()
        print(fname_from_str_path(fpath_result), 'was successfully created.')
    elif list_found_rows and str_method == '1':
        print('The search was successfully finished.')
    if list_found_rows and str_function == '0':
        print(str(len(list_found_rows)), 'matches.')

    elapsed = time.time() - start
    print(
        str(elapsed)[:10], 'seconds.\n\n',
        '\rClick [x] on the tk window or press [Enter] on this screen to exit.'
    )
    try:
        input('\n')
    except:
        pass

    frame.quit()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
