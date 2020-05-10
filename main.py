#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

def convert_array_presentation(str):
    key, value = str.split(': ')
    v_split = value.replace(' ', '').split(',')
    v_split_r = [a for a in v_split if a != '']
    result = '%s: [%s]' % (key, ', '.join(v_split_r))
    return result

def convert_line(str):
    if 'category' in str or 'tags' in str:
        return convert_array_presentation(str)
    return str

def convert(path):
    path_split = path.split('/')
    file_name = path_split.pop(-1)

    with open(path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        result = '\n'.join(map(convert_line, l_strip))

    with open(file_name, mode = 'w') as f:
        f.write(result)

if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args):
        if type(args[1]) is str:
            convert(args[1])
        else:
            print('Argument is not string')
    else:
        print('Arguments are too short')

# TODO: ディレクトリをよみこんで処理する
# TODO: 出力先をコマンドライン引数に渡せるようにする
