#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
from converter import Converter

OUTPUT_DIR = 'dist'

def handle_file(path):
    converter = Converter()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    path_split = path.split('/')
    file_name = path_split.pop(-1)

    with open(path) as f:
        l_strip = [s.rstrip() for s in f.readlines()]
        result = converter.convert(l_strip)

    with open(os.path.join(OUTPUT_DIR, file_name), mode = 'w') as f:
        f.write(result)

def handle_path(path):
    if os.path.isfile(path):
        handle_file(path)
        return

    if not os.path.isdir(path):
        return

    entries = os.listdir(path)

    for entry in entries:
        if not re.search(r"[.]md$", entry) is None:
            handle_file(path + entry)

def clear_dist():
    shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

    with open(os.path.join(OUTPUT_DIR, '.gitkeep'), 'w') as f:
        pass

def main():
    converter = Converter()
    args = sys.argv

    if 2 <= len(args):
        if type(args[1]) is str:
            print('Start processing...')
            clear_dist()
            handle_path(args[1])
        else:
            print('Argument is not string')
    else:
        print('Arguments are too short')

if __name__ == '__main__':
    main()

# TODO: 出力先をコマンドライン引数に渡せるようにする
