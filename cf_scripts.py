'''
cd dropbox/codes/check_forbidden
py -B cf_scripts.py

This file contains helper functions, which are
basically without any side effects to UIs and Variables
'''
import setup
import cf_html
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

default_dict_options = {
    'bool_function': False, 'bool_export': False,
    'bool_open': True, 'bool_save': False
}

tuple_html_entities = (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', '\''))


def append_metadata():
    list_metadata = []

    meta_date_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    meta_program = 'Check Forbidden'
    meta_version = 'v' + setup.dict_console['version']
    list_metadata.append(meta_date_time)
    list_metadata.append(''.join([
        '<a href="https://github.com/ShunSakurai/check_forbidden" target="_blank">',
        meta_program, '</a>', ' ', meta_version
    ]))

    return list_metadata


def apply_update(download_path):
    print('Starting the installer...')
    print('You may have to close the current process to continue.')
    print('After installation, please manually delete the installer in Downloads folder.')
    if sys.platform.startswith('win'):
        download_path_bslash = replace_fslash_w_bslash(download_path)
        os.startfile(download_path_bslash)
    else:
        subprocess.run(['open', download_path])


def cleanup_if_mqxlz(fn_bl):
    if fn_bl.endswith('mqxlz'):
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


def check_updates(*event, download_function=download_installer):
    print('-' * 70)
    url_releases = 'https://github.com/ShunSakurai/check_forbidden/releases'
    try:
        str_release_page = str(ur.urlopen(url_releases).read())
    except:
        print('Check Forbidden could not connect to', url_releases)
        return
    pattern_version = re.compile(r'(?:<span class="css-truncate-target"[^>]*?>v)([0-9.]+)(?=</span>)')
    pattern_installer = re.compile(r'/ShunSakurai/check_forbidden/releases/download/v([0-9.]+)/(check_forbidden_installer_\1.0.exe)')
    str_newest_version = pattern_version.search(str_release_page).group(1)
    url_installer = pattern_installer.search(str_release_page)
    if new_version_is_available(setup.dict_console['version'], str_newest_version):
        download_path = download_function(str_newest_version, url_installer)
        apply_update(download_path)
    else:
        print('You are using the newest version:', setup.dict_console['version'])


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


def get_max_length(two_dimensions_list):
    max_length = 0
    for row in two_dimensions_list:
        if isinstance(row, list) and len(row) > max_length:
            max_length = len(row)
    return max_length


def fname_from_str_path(str_path):
    f_name = str_path.rsplit('/', 1)[-1]
    return f_name


def load_header_range(header):
    regex_id = re.compile(r'<trans-unit id="(\d+)"')
    regex_percent = re.compile(r'mq:percent="(\d+)"')
    string_locked = 'mq:locked="locked"'
    seg_id = int(regex_id.search(header).group(1))
    percent = 0
    match_percent = regex_percent.search(header)
    locked = string_locked in header
    if match_percent:
        percent = int(match_percent.group(1))
    return seg_id, percent, locked


def load_translation(fn_bl_tuple):
    fn_bl = fn_bl_tuple[1]
    f_bl = open(fn_bl, encoding='utf-8')
    f_bl_line_list = []

    if fn_bl.endswith('.txt'):
        index = 1
        for i in f_bl.readlines():
            f_bl_line_list.append((index, '', i, '-', 'No', '-'))
            index += 1

    source_pattern = re.compile(
        '<source xml:space="preserve".*?>(.*?)</source>', re.S)
    target_pattern = re.compile(
        '<target xml:space="preserve">(.*?)</target>', re.S)

    not_historical = True
    for f_bl_line in f_bl:
        if '<mq:historical-unit ' in f_bl_line:
            not_historical = False
        elif '</mq:historical-unit>' in f_bl_line:
            not_historical = True
        elif f_bl_line.startswith('<trans-unit id="') and not_historical:
            seg_id, percent, locked = load_header_range(f_bl_line)
        elif f_bl_line.startswith('<source xml:space="preserve"') and not_historical:
            while '</source>' not in f_bl_line:
                f_bl_line += '\n' + next(f_bl)
            source_line_with_tag = source_pattern.search(f_bl_line).group(1)
            source_line_text_only = replace_tags(source_line_with_tag)
        elif f_bl_line.startswith('<target xml:space="preserve">') and not_historical:
            while '</target>' not in f_bl_line:
                f_bl_line += '\n' + next(f_bl)
            target_line_with_tag = target_pattern.search(f_bl_line).group(1)
            target_line_text_only = replace_tags(target_line_with_tag)
            same = source_line_text_only == target_line_text_only
            if target_line_text_only:
                f_bl_line_list.append(
                    (seg_id, source_line_text_only, target_line_text_only, percent, locked, same)
                )
        else:
            continue
    f_bl.close()
    return f_bl_line_list


def ls_from_list_str(list_str):
    r'''
    >>> ls_from_list_str("['Index', 'Source', 'Target (NG)', 'Target (OK)']")
    ['Index', 'Source', 'Target (NG)', 'Target (OK)']

    >>> ls_from_list_str('Mere string')
    ['Mere string']
    '''
    list_from_str = [i.strip('\'') for i in list_str.strip('[]').split(', ')]
    return list_from_str


def ls_from_str_tuple(str_tuple):
    r'''
    >>> ls_from_str_tuple(r' {C:\Users\path\file name with space.mqliff} C:/Users/path/file_name,_with_comma.mqxlz')
    ['C:\\Users\\path\\file name with space.mqliff', 'C:/Users/path/file_name,_with_comma.mqxlz']
    >>> ls_from_str_tuple(r"('C:\Users\path\file name with space.mqliff', 'C:/Users/path/file_name,_with_comma.mqxlz')")
    ['C:\\Users\\path\\file name with space.mqliff', 'C:/Users/path/file_name,_with_comma.mqxlz']
    '''
    if not str_tuple:
        return ['']
    list_from_str = []
    str_tuple = str_tuple.strip('(, )')

    while str_tuple:
        first_character = str_tuple[0]
        if first_character in '{\'"':
            if first_character == '{':
                # path is input directly in the field
                pattern_end = re.compile(r'(?<=[^\\])}')
            else:
                # files are selected from the button
                pattern_end = re.compile(r'(?<=[^\\])' + first_character)
            match = pattern_end.search(str_tuple)
            if not match:
                list_from_str.append(str_tuple)
                break
            end = match.end(0)
            list_from_str.append(str_tuple[1: end - 1])
            str_tuple = str_tuple[end:]
            str_tuple = str_tuple.strip(', ')

        else:
            # only one file is selected and the path doesn't include space
            list_from_str.append(str_tuple)
            break

    return list_from_str


def new_version_is_available(str_installed, str_online):
    list_installed = setup.zero_pad(str_installed).split('.')
    list_online = setup.zero_pad(str_online).split('.')
    for (i, o) in zip(list_installed, list_online):
        if int(i) == int(o):
            pass
        else:
            return int(i) < int(o)
    return False


def open_file(str_file_path):
    print('Opening the file...')
    if sys.platform.startswith('win'):
        str_file_path_bslash = replace_fslash_w_bslash(str_file_path)
        os.startfile(str_file_path_bslash)
    else:
        subprocess.run(['open', str_file_path])


def open_folder(tuple_path):
    if tuple_path and 'Command Prompt only.' not in tuple_path:
        str_path_1 = ls_from_str_tuple(tuple_path)[0]
        str_path_dir = dir_from_str_path(str_path_1)
        if sys.platform.startswith('win'):
            str_path_dir_bslash = replace_fslash_w_bslash(str_path_dir)
            os.startfile(str_path_dir_bslash)
        else:
            subprocess.run(['open', str_path_dir])


def open_readme(*event):
    webbrowser.open_new_tab(
        'https://github.com/ShunSakurai/check_forbidden/blob/master/README.md')


def print_and_append_terms_data(fpath_terms, dict_options):
    fname_header_terms = []
    fname_terms = fname_from_str_path(fpath_terms)

    print('-' * 70)
    if not dict_options['bool_function']:
        f_terms = open(fpath_terms, encoding='utf-8')
        header = f_terms.readline().rstrip('\n')
        f_terms.close()
        try_printing('Terms: ' + fpath_terms)
        try_printing('Header: [' + header + '] + Segment Number')
        fname_header_terms.append(fname_terms)
        fname_header_terms.append(header.split(','))
    else:
        try_printing('Function: ' + fpath_terms)
        fname_header_terms.append(fname_terms)
    print('-' * 70)

    return fname_header_terms


def print_or_append(to_print, to_write, file_to_write_in, dict_options):
    file_to_write_in.append(to_write)
    if dict_options['bool_export']:
        try_printing(to_print)


def escape_html_entities(string, *unescape):
    for (entity, symbol) in tuple_html_entities:
        if not unescape:
            string = string.replace(symbol, entity)
        else:
            string = string.replace(entity, symbol)
    return string


def replace_tags(segment):
    regex_tag = re.compile(r'<([^/\s]+).*?>(.*?)</\1>', re.S)
    regex_tag_comment = re.compile(r'<mrk mtype=.*?>', re.S)
    regex_displaytext = re.compile(r'displaytext=&quot;(.*?)&quot;')
    regex_val = re.compile(r'val=&quot;(.*?)&quot;', re.DOTALL)
    if regex_tag_comment.search(segment):
        segment = regex_tag_comment.sub('', segment)

    match_tag = True
    while match_tag:
        match_tag = re.search(regex_tag, segment)
        if match_tag:
            if match_tag[1] == 'ph' and match_tag[2] in ['&lt;br /&gt;']:
                text_after = '\n'
            else:
                match_displaytext = re.search(regex_displaytext, match_tag[2])
                match_val = re.search(regex_val, match_tag[2])
                if match_displaytext and not match_displaytext[1].startswith('&amp;lt;'):
                    text_after = match_displaytext[1]
                elif match_val and not match_val[1].startswith('&amp;lt;'):
                    if match_val[1] in ['&ampnbsp;', 'nbsp']:
                        text_after = ' '
                    elif match_val[1] in ['\n', 'br', 'br/', 'br /']:
                        text_after = '\n'
                    else:
                        text_after = match_val[1]
                else:
                    text_after = ''
            segment = ''.join([
                segment[:match_tag.start()], text_after, segment[match_tag.end():]
            ])
    return escape_html_entities(segment, True)


def replace_bslash_w_fslash(str_path):
    return str_path.replace('\\', '/')


def replace_fslash_w_bslash(str_path):
    return str_path.replace('/', '\\')


def tf_to_yn(value):
    if isinstance(value, str):
        return value
    if value:
        return ('Yes')
    else:
        return ('No')


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


def try_rmdir(dir_path):
    try:
        os.dir_path(dir_path)
    except:
        try:
            time.sleep(0.01)
            os.rmdir(dir_path)
        except:
            print('Please go to the bilingual file location and delete the _extract folder manually.')


def unique_ordered_list(sequence):
    unique_list = []
    for i in sequence:
        if i not in unique_list:
            unique_list.append(i)
    return unique_list


def unzip_if_mqxlz(fn_bl):
    if fn_bl.endswith('mqxlz'):
        path_extract = dirname_from_fname(fn_bl) + '_extract'
        fn_actual = zipfile.ZipFile(fn_bl).extract(
            'document.mqxliff', path=path_extract)
        return fn_actual
    else:
        return fn_bl


def write_result(f_result_w, fpath_result, dict_options):
    list_metadata = append_metadata()
    if not dict_options['bool_function']:
        fpath_template = 'files/cf_template_terms.html'
        num_columns = 8
    else:
        fpath_template = 'files/cf_template_functions.html'
        num_columns = get_max_length(f_result_w)

    f_template = open(fpath_template, encoding='utf-8')
    fr_template = f_template.read()

    f_result = open(fpath_result, 'w', encoding='utf-8')
    f_result.write(fr_template.replace(
        '@list_metadata', '</li>\n<li>'.join(list_metadata)
    ).replace(
        '@filter_header', cf_html.mk_table_filter_header(dict_options)
    ).replace(
        '@filter_body', cf_html.mk_table_filter_body(num_columns)
    ).replace(
        '@result_tables', cf_html.mk_table_result(f_result_w, dict_options)
    ))
    f_result.close()
    return fname_from_str_path(fpath_result)


def wrap_up_result_if_found(
        list_matched_rows, list_matches_summary, fpath_result, dict_options):
    if not dict_options['bool_function']:
        print('Summary')
        list_reduced = unique_ordered_list(
            [str(i) for i in list_matches_summary]
        )
        for i in list_reduced:
            try_printing(i)
        print('')
        print(str(len(list_matched_rows)), 'matches.')


def check_against_function(
        fname_bl, f_bl_line_list, fpath_terms, dict_options):
    sublist_matched_rows = []

    mdir, mfile = fpath_terms.rsplit('/', 1)
    mname = mfile.rsplit('.', 1)[0]
    sys.path.append(mdir)
    external_script = importlib.import_module(mname)
    for (seg_id, source, target, percent, locked, same) in f_bl_line_list:
        result = external_script.function(seg_id, source, target, percent, locked, same)
        if result:
            for ls in result:
                print_or_append(ls, ls, sublist_matched_rows, dict_options)

    return sublist_matched_rows


def check_against_terms(
        fname_bl, f_bl_line_list, f_terms_reader, dict_options):
    sublist_matched_rows = []
    sublist_matches_summary = []

    for row in f_terms_reader:
        if not row or not row[0]:
            continue
        try:
            pattern = re.compile(row[0])
        except:
            print('Error occurred with regex pattern:', row[0])
            print(sys.exc_info()[1], '\n', sys.exc_info()[0])
            continue
        for (seg_id, source, target, percent, locked, same) in f_bl_line_list:
            match = pattern.search(target)
            if match:
                s, e = match.start(), match.end()
                print_or_append(
                    '\n\r'.join([
                        str(row),
                        ''.join([
                            str(seg_id), '\t', target[s - 5:s], '...',
                            target[s:e], '...', target[e:e + 5]]),
                        source, target, ''
                    ]),
                    [
                        fname_bl, seg_id,
                        re.sub(r'\n+', '<br />', escape_html_entities(source)),
                        re.sub(r'\n+', '<br />', ''.join([
                            escape_html_entities(target[:s]), '<mark>',
                            escape_html_entities(target[s:e]), '</mark>',
                            escape_html_entities(target[e:])])),
                        percent, tf_to_yn(locked), tf_to_yn(same)
                    ] + [escape_html_entities(cell) for cell in row],
                    sublist_matched_rows, dict_options
                )
                sublist_matches_summary.append(row)
            else:
                continue
    return sublist_matched_rows, sublist_matches_summary


def check_for_each_term_list(
        list_fn_bl_tuple, fpath_terms, fpath_result, dict_options):
    fname_header_terms = print_and_append_terms_data(fpath_terms, dict_options)
    list_matched_rows = []
    list_matches_summary = []
    for fn_bl_tuple in list_fn_bl_tuple:
        try_printing(fn_bl_tuple[0] + '\n')
        fname_bl = fname_from_str_path(fn_bl_tuple[0])
        f_bl_line_list = load_translation(fn_bl_tuple)

        f_terms = open(fpath_terms, encoding='utf-8')
        f_terms_reader = csv.reader(f_terms)
        if dict_options['bool_function']:
            list_matched_rows += check_against_function(
                fname_bl, f_bl_line_list, fpath_terms, dict_options)
        else:
            sublist_matched_rows, sublist_matches_summary = check_against_terms(
                fname_bl, f_bl_line_list, f_terms_reader, dict_options)
            list_matched_rows += sublist_matched_rows
            list_matches_summary += sublist_matches_summary
    f_terms.close()

    if list_matched_rows:
        wrap_up_result_if_found(
            list_matched_rows, list_matches_summary, fpath_result, dict_options
        )
        return fname_header_terms + list_matched_rows
    else:
        print('No forbidden term was found!')
        return []


def check_forbidden_terms(
        str_tuple_bl, str_tuple_terms, str_result, dict_options):
    dict_options = dict_options or default_dict_options
    start = time.time()
    list_fpath_bl = ls_from_str_tuple(str_tuple_bl)
    list_fpath_terms = ls_from_str_tuple(str_tuple_terms)
    fpath_result = replace_bslash_w_fslash(str_result)

    for fn_terms in list_fpath_terms:
        if fn_terms.rsplit('.', 1)[-1] not in ['csv', 'txt', 'py']:
            print('File name is invalid:', fn_terms)
            return

    for fn_bl in list_fpath_bl:
        if fn_bl.rsplit('.', 1)[-1] not in ['mqxlz', 'mqxliff', 'txt']:
            print('File name is invalid:', fn_bl)
            return

    list_fn_bl_tuple = []
    for fn_bl in list_fpath_bl:
        fn_actual = replace_bslash_w_fslash(unzip_if_mqxlz(fn_bl))
        list_fn_bl_tuple.append((fn_bl, fn_actual))

    f_result_w = []
    for fpath_terms in list_fpath_terms:
        f_result_w += check_for_each_term_list(
            list_fn_bl_tuple, fpath_terms, fpath_result, dict_options
        )

    elapsed = time.time() - start
    print(str(elapsed)[:10], 'seconds.\n')
    return f_result_w, fpath_result, list_fpath_bl


if __name__ == "__main__":
    import doctest
    doctest.testmod()
