def mk_table_filter_header(dict_options):
    ls_filter_header = []
    if not dict_options['bool_function']:
        for (width, col) in zip(
            [10, 5, 20, 20, 5, 5, 10],
            ['File', 'Seg', 'Source', 'Target', r'%', 'Lock', 'Forbidden']
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
        ['include', 'exclude', 'includeRegex', 'excludeRegex'],
        ['filter', 'filter moreTools', 'filter moreTools', 'filter moreTools'],
        ['', '!', '.*', '!.*']
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
        ] * 6
        ls_filter_body.append(' ' * 8 + '</tr>')
    return '\n'.join(ls_filter_body)


def mk_table_result_header(dict_options):
    ls_result_header = []
    if not dict_options['bool_function']:
        for (width, col) in zip(
            [10, 5, 20, 20, 5, 5],
            ['File', 'Seg', 'Source', 'Target', r'%', 'Lock']
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
    closing_tags = ''.join([
        ' ' * 10, '</td></tr>\n', ' ' * 6, '</tbody>\n', ' ' * 4, '</table>'
    ])

    iter_result = iter(f_result_w)
    for line in iter_result:
        if isinstance(line, str) and not first_line:
            ls_str_tables.append(closing_tags)
        if isinstance(line, str):
            ls_str_tables.append(''.join([
                ' ' * 4, '<table border="1">\n',
                ' ' * 6, '<caption>{}</caption>\n',
                ' ' * 6, '<tbody>\n', ' ' * 8, '<tr>'
            ]).format(line)
            )
            ls_str_tables.append(mk_table_result_header(dict_options))
            if not dict_options['bool_function']:
                ls_str_tables.append(' ' * 10 + '<th>')
                ls_str_tables.append(
                    ''.join(['</th>\n', ' ' * 10, '<th>'])
                    .join(str(i) for i in next(iter_result))
                )
                ls_str_tables.append(' ' * 10 + '</th>')
            ls_str_tables.append(' ' * 8 + '</tr>')
            first_line = False
        else:
            ls_str_tables.append(''.join([' ' * 8, '<tr>\n', ' ' * 10, '<td>']))
            ls_str_tables.append(
                ''.join(['</td>\n', ' ' * 10, '<td>'])
                .join([str(i) for i in line])
            )
            ls_str_tables.append(' ' * 10 + '</td></tr>')
    ls_str_tables.append(closing_tags)
    return '\n'.join(ls_str_tables)
