#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from itertools import product
from heapq import nlargest
import logging


MAX_LEN = 5


def parse_ngramstr(text):
    ngram, count = text.rsplit(maxsplit=1)
    return ngram, int(count)


def parse_line(line):
    query, *ngramcounts = line.strip().split('\t')
    return query, tuple(map(parse_ngramstr, ngramcounts))


def expand_query(query):
    # TODO: write your query expansion, e.g.,
    #  "in/at afternoon" -> ["in afternoon", "at afternoon"]
    #  "listen ?to music" -> ["listen music", "listen to music"]
    q_split = query.split()
    q_split_copy = q_split.copy()
    result = []
    expand = 0
    # Handle '/'
    for i in range(len(q_split)):
        if '/' in q_split[i]:
            expand = 1
            candidate = q_split[i].split('/')
            for j in candidate:
                res = query.replace(q_split[i], j)
                result.append(res)

    # Handle '?'
    for i in range(len(q_split)):
        if '?' in q_split[i]:
            expand = 1
            q_split_copy.remove(q_split[i])
            new = " ".join(q_split_copy)
            result.append(new)

            # remove '?'
            word = q_split[i].split('?')[1]
            result.append(query.replace(q_split[i], word))

    if expand == 0:
        return [query]
    else:
        return result


def extend_query(query):
    # TODO: write your query extension, 
    # e.g., can tolerate missing/unnecessary determiners
    extend = 0
    q_split = query.split()
    q_split_copy = q_split.copy()
    result = []

    # Handle '*': generate MAX_LEN query with 0 ~ MAX_LEN '_'
    for i in range(len(q_split)):
        if '*' in q_split[i]:
            extend = 1
            q_split_copy.remove(q_split[i])
            new = " ".join(q_split_copy)
            result.append(new)
            for j in range(1, MAX_LEN):
                replace = ['_' for _ in range(1, j+1)]
                replace = " ".join(replace)
                result.append(query.replace(q_split[i], replace))

    if extend == 0:
        return [query]
    else:
        return result


def load_data(lines):
    logging.info('Loading...', end='')
    # read linggle data
    linggle_table = {query: ngramcounts for query, ngramcounts in map(parse_line, lines)}
    logging.info('ready.')
    return linggle_table


def linggle(linggle_table):
    q = input('linggle> ')

    # exit execution keyword: exit()
    if q == 'exit()':
        return

    # extend and expand query
    queries = [
        simple_query
        for query in extend_query(q)
        for simple_query in expand_query(query)
    ]

    # test
    # for i in queries:
    #     print(i)

    # gather results
    ngramcounts = {item for query in queries if query in linggle_table for item in linggle_table[query]}
    # output 10 most common ngrams
    ngramcounts = nlargest(10, ngramcounts, key=itemgetter(1))

    if len(ngramcounts) > 0:
        print(*(f"{count:>7,}: {ngram}" for ngram, count in ngramcounts), sep='\n')
    else:
        print(' '*8, 'no result.')
    print()

    return True


if __name__ == '__main__':
    import fileinput
    # If the readline module was loaded, then input() will use it to provide elaborate line editing and history features.
    # https://docs.python.org/3/library/functions.html#input
    import readline

    linggle_table = load_data(fileinput.input())
    while linggle(linggle_table):
        pass

    # nc.sample 用來測試 mapper reducer 是否正確
    # reducer 產出的東西要和 linggle sample 相似