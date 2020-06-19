#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

FRONTMATTER_SEP = '---'
READ_MORE = '<!--more-->'

class Converter:
    def __init__(self):
        self.sep_count = 0
        self.category = ''

    def convert_array_presentation(self, line):
        if re.search(r"[:]\s*$", line):
            return line

        key, value = line.split(': ')
        v_split = value.replace(' ', '').split(',')
        v_split_r = [a for a in v_split if a != '']

        if (key == 'category'):
            key = 'categories'
            self.category = v_split_r.pop()

        result = '%s: [%s]' % (key, ', '.join(v_split_r))

        return result

    def convert_date_format(self, line):
        # print(line)
        matched = re.match(r"^date[:]\s(\d{4}[-]\d{2}[-]\d{2})\s(\d{2}[:]\d{2}[:]\d{2})", line)
        if matched:
            # print(matched.group(1) + 'T' + matched.group(2) + '+09:00')
            return 'date: ' + matched.group(1) + 'T' + matched.group(2) + '+09:00'
        matched2 = re.match(r"^date[:]\s(\d{4}[-]\d{2}[-]\d{2})\s(\d{2}[:]\d{2}) UTC", line)
        if matched2:
            # print(matched2.group(1) + 'T' + matched2.group(2) + ':00+09:00')
            return 'date: ' + matched2.group(1) + 'T' + matched2.group(2) + ':00+09:00'

    def convert_ficker_link(self, line):
        return re.sub(r'http:\/\/(farm\d\.static\.?flickr\.com\/[0-9a-zA-Z-_./]+)', r'https://\1', line)

    def convert_amazon_link(self, line):
        return re.sub(r'http:\/\/(rcm-jp\.amazon\.co\.jp\/[0-9a-zA-Z-=_./&?;]+)', r'https://\1', line)

    def convert_amazon_link2(self, line):
        return re.sub(r'http:\/\/(www\.assoc-amazon\.jp\/[0-9a-zA-Z-=_./&?;]+)', r'https://\1', line)

    def convert_line(self, line):
        line = self.convert_ficker_link(line)
        line = self.convert_amazon_link(line)
        line = self.convert_amazon_link2(line)

        if line == 'READMORE': return READ_MORE
        if line == FRONTMATTER_SEP: self.sep_count += 1
        if self.sep_count > 1: return line

        if 'category' in line:
            return self.convert_array_presentation(line)

        if 'tags' in line:
            return self.convert_array_presentation(line)

        if 'date' in line:
            return self.convert_date_format(line)

        return line

    def insert_alias(self, line_arr, file_name):
        new_name = re.sub(r"^\d{4}[-]\d{2}[-]\d{2}[-]", '', file_name)
        new_name = re.sub(r"[.]md$", '', new_name)
        new_name = re.sub(r"[.]html$", '', new_name)
        sep_indexes = [i for i, x in enumerate(line_arr) if x == '---']
        second_sep_index = sep_indexes[1]
        if (self.category):
            line_arr.insert(second_sep_index, '  - /%s/%s' % (self.category.lower(), new_name))
        else:
            line_arr.insert(second_sep_index, '  - /%s' % new_name)
        line_arr.insert(second_sep_index, 'aliases:')

        return line_arr

    def convert(self, lines, file_name):
        self.sep_count = 0
        line_arr = map(self.convert_line, lines)
        line_arr = self.insert_alias(line_arr, file_name)
        return '\n'.join(line_arr)
