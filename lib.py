#!/usr/bin/env python
# import numpy as np
import functools
import numbers
from typing import List, Set, Dict, Tuple, Optional
from collections import defaultdict
# from copy import deepcopy

"""
Commonly used functions from 2020:

from fileinput import input
from itertools import combinations, permutations, product, islice
from functools import reduce
from collections import Counter, defaultdict, deque
from re import match, subn, findall
from copy import deepcopy
from numpy import array, count_nonzero
from math import sqrt, pow, radians, sin, cos, tan
"""

"""
BFS
2d scanning (4-way/tblr & 8-way):
- 4-way: DR=[-1,0,1,0], DC=[0,-1,0,1]  for i in range(4)
- 9-way: for dr, dc in itertools.product([-1,0,1],[-1,0,1]):
"""


# ANSI Colors for POSIX terminals
class ANSIColor:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   GRAY = '\033[90m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def grouped(lines, is_separator=None):
    """Separate list of lines into groups of consecutive non-empty lines.

    is_separator
        A function to determine if a line separates other groups of lines (defaults to True for empty lines). Has to be
        based only on the contents of the line. The line itself will be dropped and not included in any groups that are
        output.
    """
    if is_separator is None:
        is_separator = lambda ln: ln == ''

    group = []
    for line in lines:
        if line == '':
            if len(group) > 0:
                yield group
            group = []
        else:
            group.append(line)
    # Handle final group in case there's no ending separator
    # Alternative is to add separator at the end: lines.append('')
    # but this requires modifying or copying the input
    if len(group) > 0:
        yield group


def grouped_rule(lines, line_id):
    """Group multiple consecutive lines that fit the given rule.

    line_id
        A value extracted from a line with which to group a line with neighbours if their values also match.
    """
    group = []
    for line in lines:
        group.append(line)
        if len(set([line_id(line) for line in group])) > 1:
            group = group[:-1]
            yield group
            group = [line]
    yield group


def print_dict(dic):
    for key in sorted(dic.keys()):
        print(key, dic[key])
    print()


def prod(iterable):
    # operator.mul
    return functools.reduce(lambda a,b,: a*b, iterable, 1)


def set_char(stringy, pos, charry):
    list1 = list(stringy)
    list1[pos] = charry
    return ''.join(list1)


def wrap(value, limit):
    return value % limit


class Map2D:
    """
    A 2D map based on a list of strings.
    """

    def __init__(self):
        pass

    def load_from_file(self, filename):
        input_file = open(filename,'r')
        mappy = [line.rstrip('\n') for line in input_file.readlines()]
        # lines = [line.rstrip('\n') for line in input_file.readlines()]
        # # numpy arrays won't work if line lengths aren't exactly the same
        # arr = np.array([list(line) for line in lines])
        self.load_from_data(mappy)

    def load_from_data(self, list_of_strings):
        self.map_data = list_of_strings
        self.validate()

    def validate(self):
        assert self.rows > 0
        first_row_len = self.cols
        for row in self.map_data:
            assert len(row) == first_row_len

    @property
    def rows(self):
        # height, y-axis
        return len(self.map_data)

    @property
    def cols(self):
        # width, x-axis
        return len(self.row(0))

    @property
    def shape(self):
        return (self.rows, self.cols)

    def row(self, idx):
        return self[idx]
    
    def col(self, idx):
        """Get a whole column as a string"""
        colly = ''
        for row in self.map_data:
            colly += row[idx]
        return colly

    def in_bounds(self, row, col):
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return True
        return False

    def get(self, row, col):
        return self.map_data[row][col]

    def set(self, row, col, value):
        whole_row = self.map_data[row]
        self.map_data[row] = set_char(whole_row, col, value)

    def move_slope(self, row_jmp, col_jmp, wrap=False, row_start=0, col_start=0):
        """
        Generator to move across map at a constant rate until out of bounds.

        m.move_slope(5,6,wrap=True)
        m.move_slope(5,6,wrap=(True, False))
        """
        if isinstance(wrap, bool):
            wrap = (wrap, wrap)

        row = row_start
        col = col_start
        while self.in_bounds(row, col):
            # Allow calculation based on current position and value
            yield self.get(row, col), row, col
            # Move
            row += row_jmp
            col += col_jmp
            # Wrap if specified
            row = row % self.rows if wrap[0] else row
            col = col % self.cols if wrap[1] else col

    def __getitem__(self, key):
        """
        No wrapping capabilities. Use get() for that.
        """
        if isinstance(key, numbers.Integral):
            key = (key, slice(None, None, None))

        assert isinstance(key, tuple)
        assert len(key) == 2
        # assert all(isinstance(i, numbers.Integral) for i in key)
        row, col = key
        return self.map_data[row][col]

    def to_str(self):
        stry = ''
        for row in self.map_data:
            stry += row + '\n'
        return stry
    
    def to_str_col(self, locs_per_color: List[Set[Tuple[int,int]]], colors: List[str],
                   replace_chars: Optional[Dict[str, str]]=None):
        """Print map with some locations having specific colors."""
        if replace_chars is None:
            replace_chars = {}

        highlights_per_row = defaultdict(list)
        for idx, locs in enumerate(locs_per_color):
            color = colors[idx]
            print(locs)
            for row, col in locs:
                highlights_per_row[row].append((col, color))
        print(highlights_per_row)

        stry = ''
        for idx, row in enumerate(self.map_data):
            # if idx not in highlights_per_row:
            #     stry += row + '\n'
            #     continue
            locs = highlights_per_row[idx]

            new_row = list([replace_chars[r] if r in replace_chars else r for r in row])
            # Add in reverse order (from end) so starting index doesn't change
            for col, color in sorted(locs, key=lambda cc: cc[0], reverse=True):
                curr_value = row[col]
                if curr_value in replace_chars:
                    curr_value = replace_chars[curr_value]
                # Insert in reverse order as well (since each insert() pushes
                # values to the end)
                new_row[col] = ANSIColor.END
                new_row.insert(col, curr_value)
                new_row.insert(col, color)
            stry += ''.join(new_row) + '\n'
        return stry

    def to_str_partial(self, first=3, last=3):
        """Show string with only first and last few rows"""
        stry = ''
        for idx in range(first):
            stry += self[idx] + '\n'
        stry += '\n    ...\n\n'
        for idx in range(last, 0, -1):
            stry += self[-idx] + '\n'
        return stry

    def __str__(self):
        stry = 'Size: {}x{}\n'.format(self.rows, self.cols)    
        if self.rows <= 20:
            stry += self.to_str()
        else:
            stry += self.to_str_partial()
        return stry


if __name__ == '__main__':
    # mapp = Map2D()
    # mapp.load_from_file('input.txt')
    # print(mapp)
    # print(mapp.get(0, 0))
    # print(mapp.get(322, 30))
    # print(mapp.get(323, 31, wrap=True))
    # print(mapp.get(322, 31, wrap=(False, True)))
    # print(mapp.to_str())
    # print(mapp.col(1))
    pos = Pos2D(1, 2)
    print(pos.r, pos.c)
    print(pos.x, pos.y)
    print(pos.w, pos.h)
    exit()