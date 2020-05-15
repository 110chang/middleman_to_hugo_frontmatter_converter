#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import sys

FRONTMATTER_SEP = '---'
OUTPUT_DIR = 'dist'
READ_MORE = '<!--more-->'

class Converter:
    sep_count = 0

    def convert_array_presentation(self, line):
        if re.search(r"[:]\s*$", line):
            return line

        key, value = line.split(': ')
        v_split = value.replace(' ', '').split(',')
        v_split_r = [a for a in v_split if a != '']
        result = '%s: [%s]' % (key, ', '.join(v_split_r))

        return result

    def convert_line(self, line):
        if re.search(r"^READMORE$", line): return READ_MORE

        if line == FRONTMATTER_SEP:
            self.sep_count += 1

        if self.sep_count > 1: return line

        if 'category' in line or 'tags' in line:
            return self.convert_array_presentation(line)

        return line

    def convert(self, path):
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        path_split = path.split('/')
        file_name = path_split.pop(-1)

        with open(path) as f:
            self.sep_count = 0
            l_strip = [s.rstrip() for s in f.readlines()]
            result = '\n'.join(map(self.convert_line, l_strip))

        with open(os.path.join(OUTPUT_DIR, file_name), mode = 'w') as f:
            f.write(result)

    def handle_path(self, path):
        if os.path.isfile(path):
            self.convert(path)
            return

        if not os.path.isdir(path):
            return

        entries = os.listdir(path)

        for entry in entries:
            if not re.search(r"[.]md$", entry) is None:
                self.convert(path + entry)

    def clear_dist(self):
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
            converter.clear_dist()
            converter.handle_path(args[1])
        else:
            print('Argument is not string')
    else:
        print('Arguments are too short')

if __name__ == '__main__':
    main()

# TODO: 出力先をコマンドライン引数に渡せるようにする
