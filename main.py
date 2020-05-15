#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from converter import Converter

FRONTMATTER_SEP = '---'
OUTPUT_DIR = 'dist'
READ_MORE = '<!--more-->'

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
