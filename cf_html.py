def mk_table_filter_header(dict_options):
    ls_filter_header = []
    if not dict_options['bool_function']:
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


def mk_table_filter_body():
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
        ] * 7
        ls_filter_body.append(' ' * 8 + '</tr>')
    return '\n'.join(ls_filter_body)


def mk_table_result_header(dict_options):
    ls_result_header = []
    if not dict_options['bool_function']:
        for (width, col) in zip(
            [9, 4, 20, 20, 4, 4, 4],
            ['File', 'Seg', 'Source', 'Target', r'%', 'Locked', 'Same']
        ):
            ls_result_header.append(
                ''.join([
                    ' ' * 10, '<th style="width:', str(width),
                    r'%;">', col, '</th>'
                ])
            )
    return '\n'.join(ls_result_header)


def mk_table_result(f_result_w, dict_options):
    ls_str_tables = []
    first_line = True
    closing_tags = ''.join([' ' * 6, '</tbody>\n', ' ' * 4, '</table>'])

    iter_result = iter(f_result_w)
    for line in iter_result:
        if isinstance(line, str) and not first_line:
            ls_str_tables.append(closing_tags)
        if isinstance(line, str):
            ls_str_tables.append(''.join([
                ' ' * 4, '<table border="1">\n',
                ' ' * 6, '<caption onclick="collapseTbody(this)">▼ {}</caption>\n',
                ' ' * 6, '<tbody>\n', ' ' * 8, '<tr>'
            ]).format(line)
            )
            ls_str_tables.append(mk_table_result_header(dict_options))
            if not dict_options['bool_function']:
                ls_str_tables.append(
                    ' ' * 10 + '<th>' +
                    ''.join(['</th>\n', ' ' * 10, '<th>'])
                    .join(str(i) for i in next(iter_result)) +
                    '</th>'
                )
            ls_str_tables.append(' ' * 8 + '</tr>')
            first_line = False
        else:
            ls_str_tables.append(' ' * 8 + '<tr>')
            ls_str_tables.append(
                ' ' * 10 + '<td>' +
                ''.join(['</td>\n', ' ' * 10, '<td>'])
                .join([str(i) for i in line]) +
                '</td>'
            )
            ls_str_tables.append(' ' * 8 + '</tr>')
    ls_str_tables.append(closing_tags)
    return '\n'.join(ls_str_tables)
