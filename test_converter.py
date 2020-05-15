#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from converter import Converter

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()

    def test_convert_array_presentation(self):
        expected = 'key: [value, value2]'
        actual = self.converter.convert_array_presentation('key: value, value2,')
        self.assertEqual(expected, actual)

    def test_convert_array_presentation_to_empty_value(self):
        expected = 'key: '
        actual = self.converter.convert_array_presentation('key: ')
        self.assertEqual(expected, actual)

    def test_convert_line_to_readmore(self):
        expected = '<!--more-->'
        actual = self.converter.convert_line('READMORE')
        self.assertEqual(expected, actual)

    def test_convert_line_to_categories(self):
        expected = 'category: [value]'
        actual = self.converter.convert_line('category: value,')
        self.assertEqual(expected, actual)

    def test_convert_line_to_tags(self):
        expected = 'tags: [value, value2]'
        actual = self.converter.convert_line('tags: value, value2')
        self.assertEqual(expected, actual)

    def test_convert_line_count_frontmatter(self):
        expected = 'tags: [should, be, converted]'
        self.converter.convert_line('---')
        actual = self.converter.convert_line('tags: should, be, converted,')
        self.assertEqual(expected, actual)

        expected = 'tags: should, not, be, converted,'
        self.converter.convert_line('---')
        actual = self.converter.convert_line('tags: should, not, be, converted,')
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
