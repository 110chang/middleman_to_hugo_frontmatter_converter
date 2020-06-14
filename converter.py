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

    def convert_line(self, line):
        if line == 'READMORE': return READ_MORE
        if line == FRONTMATTER_SEP: self.sep_count += 1
        if self.sep_count > 1: return line

        if 'category' in line:
            return self.convert_array_presentation(line)

        if 'tags' in line:
            return self.convert_array_presentation(line)

        return line

    def insert_alias(self, file_name):
        new_name = re.sub(r"^\d{4}[-]\d{2}[-]\d{2}[-]", '', file_name)
        # print(new_name)

    def convert(self, lines):
        self.sep_count = 0
        line_arr = map(self.convert_line, lines)
        return '\n'.join(line_arr)
