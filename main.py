#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys

output_dir = 'dist'

def convert_array_presentation(line):
    if re.search(r"[:]\s*$", line): return line
    key, value = line.split(': ')
    v_split = value.replace(' ', '').split(',')
    v_split_r = [a for a in v_split if a != '']
    result = '%s: [%s]' % (key, ', '.join(v_split_r))
    return result

def convert_line(line):
    if 'category' in line or 'tags' in line:
        return convert_array_presentation(line)
    return line

def convert(path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path_split = path.split('/')
    file_name = path_split.pop(-1)

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        result = '\n'.join(map(convert_line, l_strip))

    with open(os.path.join(output_dir, file_name), mode = 'w') as f:
        f.write(result)

def handle_path(path):
    if os.path.isfile(path):
        convert(path)
        return

    if not os.path.isdir(path):
        return

    entries = os.listdir(path)

    for entry in entries:
        if not re.search(r"[.]md$", entry) is None:
            convert(path + entry)

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        if type(args[1]) is str:
            print('Start processing...')
            handle_path(args[1])
        else:
            print('Argument is not string')
    else:
        print('Arguments are too short')

# TODO: 出力先をコマンドライン引数に渡せるようにする
# TODO: frontmatter外の処理をしない
