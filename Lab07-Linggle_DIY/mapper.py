from itertools import combinations

def inverted_index_map(lines):
    value = lines.strip()
    line = lines.strip().split('\t')
    ngram = line[0]
    ngram_split = ngram.split()
    # count = int(line[1])
    possible = []
    output = "{}#{}"
    
    for L in range(1, len(ngram_split)+1):
        for subset in combinations(ngram_split, L):
            subset = list(subset)
            possible.append(subset)
    
    for item in possible:
        res = ngram_split.copy()
        j = 0
        for i in range(len(ngram_split)):
            if j < len(item):
                if res[i] == item[j]:
                    j += 1
                else:
                    res[i] = '_'
            else:
                res[i] = '_'
        res = ' '.join(res)
        sys.stdout.write(output.format(res, value)+'\n')

if __name__ == '__main__':
    import fileinput
    import sys
    # for word, line_no in inverted_index_map(fileinput.input()):
    #     print(word, line_no)
    for line in sys.stdin:
        inverted_index_map(line)
    #         print(word, line_no)