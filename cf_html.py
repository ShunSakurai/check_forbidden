def mk_table_filter_header(dict_options):
    if dict_options['bool_function']:
        return ''
    ls_filter_header = []
    for (width, col) in zip(
        [9, 4, 20, 20, 4, 4, 4, 10],
        ['File', 'Seg', 'Source', 'Target', r'%', 'Locked', 'Same', 'Forbidden']
    ):
        ls_filter_header.append(
            ''.join([
                ' ' * 10, '<th style="width:', str(width),
                r'%;">', col, '</th>'
            ])
        )
    return '\n'.join(ls_filter_header)


def mk_table_filter_body(num_columns):
    ls_filter_body = []
    for (id, klass, ph) in zip(
        ['include', 'exclude', 'includeRegex', 'excludeRegex', 'numberRange'],
        ['filter', 'filter moreTools', 'filter moreTools', 'filter moreTools', 'filter moreTools'],
        ['', '!', '.*', '!.*', '1-2']
    ):
        ls_filter_body.append(
            ''.join([' ' * 8, '<tr id="', id, '" class="', klass, '">'])
        )
        ls_filter_body.append(
            ''.join([
                ' ' * 10, '<td><input oninput="filterSegments(this, ', id,
                ')" placeholder="', ph, '" /></td>'
            ])
        )
        ls_filter_body += [
            ''.join([
                ' ' * 10, '<td><input oninput="filterSegments(this, ', id,
                ')" /></td>'
            ])
        ] * (num_columns - 1)
        ls_filter_body.append(' ' * 8 + '</tr>')
    return '\n'.join(ls_filter_body)


def mk_terms_result_header(dict_options, csv_header):
    ls_result_header = []
    for (width, col) in zip(
        [9, 4, 20, 20, 4, 4, 4],
        ['File', 'Seg', 'Source', 'Target', r'%', 'Locked', 'Same']
    ):
        ls_result_header.append(
            ''.join([
                ' ' * 10, '<th onclick="sortTable(this)" style="width:',
                str(width), r'%;">', col, '</th>'
            ])
        )
    for header_item in csv_header:
        ls_result_header.append(
            ''.join([
                ' ' * 10 + '<th onclick="sortTable(this)">',
                str(header_item), '</th>'
            ])
        )
    return '\n'.join(ls_result_header)


def mk_table_result(f_result_w, dict_options):
    ls_str_tables = []
    first_line = True
    closing_tags = ''.join([' ' * 6, '</tbody>\n', ' ' * 4, '</table>'])
    counter_id = 0

    iter_result = iter(f_result_w)
    for line in iter_result:
        if isinstance(line, str) and not first_line:
            ls_str_tables.append(closing_tags)

        if isinstance(line, str):
            ls_str_tables.append(''.join([
                ' ' * 4, '<table>\n',
                ' ' * 6, f'<caption onclick="collapseTbody(this)">▼ {line}</caption>\n',
                ' ' * 6, '<tbody>\n', ' ' * 8, f'<tr id="{str(counter_id)}">'
            ])
            )
            if not dict_options['bool_function']:
                ls_str_tables.append(mk_terms_result_header(dict_options, next(iter_result)))
            ls_str_tables.append(' ' * 8 + '</tr>')
            first_line = False
            counter_id += 1
        else:
            ls_str_tables.append(' ' * 8 + f'<tr id="{str(counter_id)}">')
            ls_str_tables.append(
                ' ' * 10 + '<td>' +
                ''.join(['</td>\n', ' ' * 10, '<td>']).join([str(i) for i in line]) +
                '</td>'
            )
            ls_str_tables.append(' ' * 8 + '</tr>')
            counter_id += 1
    ls_str_tables.append(closing_tags)
    return '\n'.join(ls_str_tables)
