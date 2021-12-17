#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter
import sys
from collections import defaultdict

def pre_processing(lists, line):
    line = line.strip().split('#')
    key = line[0]
    value = line[1]
    value1, value2 = value.split('\t')
    # dictionary[key] = "{} {}".format(value1, value2)
    value = "{} {}".format(value1, value2)
    lists.append((key, value))

def inverted_index_reduce(lists):
    output = "{}\t{}"
    # for key, groups in groupby(dicts, key=itemgetter(0)):
    #     group = list(groups)
    #     key = list(key)
    #     sys.stdout.write(output.format(key, group))
    # v = {}

    # for key, value in dicts.items():
    #     v.setdefault(key, set()).add(value)
    data_dict = {}
    for x in lists:
        data_dict.setdefault(x[0],[]).append(x[1])
    
    for key, value in data_dict.items():
        value = "\t".join(value)
        sys.stdout.write(output.format(key, value)+'\n')

    # for key, value in data_dict.items():
    #     value = ' '.join(value)
    #     sys.stdout.write(output.format(key, value)+'\n')




if __name__ == '__main__':
    # import fileinput
    # iterable = map(str.split, fileinput.input())
    # for word, line_numbers in inverted_index_reduce(iterable):
    #     print(word, *line_numbers, sep='\t')
    lists= []
    for line in sys.stdin:
        pre_processing(lists, line)
    inverted_index_reduce(lists)