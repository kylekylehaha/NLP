from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools
import itertools as it

model = kenlm.Model('bnc.prune.arpa')

def words(text): return re.findall(r'\w+|[,.?]', text.lower())

WORDS = Counter(words(open('Data/big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can

###### Task1 ######
def spelling_check(sentence):
    sentence_split = sentence.split()
    candidate = []
    ## TODO ##

    # Find the token not in Big.txt
    not_token = []
    for word in sentence_split:
        if word not in WORDS:
            not_token.append(word)
    
    # Generate candidates of token not in Big.txt
    not_token_can = {}
    for token in not_token:
        not_token_can[token] = suggest(token)


    # Generate all combinationa
    combinations = it.product(*(not_token_can[token] for token in not_token_can))
    combinations = list(combinations)

    best_score = -100000000000
    best_can = sentence
    for sublist in combinations:
        can_str = sentence

        # Replace all word in one of combination
        for i in range (len(sublist)):
            can_str = can_str.replace(not_token[i], sublist[i])

        # Append candiate string into candidate    
        candidate.append(can_str)

        # Choose best candidate by kenlm
        can_str_score = model.score(can_str, bos=True, eos=True)/len(can_str)
        if can_str_score > best_score:
            best_score = can_str_score
            best_can = can_str
    

    return best_can, candidate

print("Task 1 Spelling Check")
task1_input = 'he sold everythin escept the housee'
print("Text:",task1_input,"\n")
print("Candidates:")
task1_result, task1_candidate = spelling_check(task1_input)
for i in task1_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task1_candidate))
print()
print("Result:", task1_result,"\n\n\n")

    
###### Task2 ######
atcs = {"", "the", "a", "an"}
preps = {"", "about", "at", "by", "for", "from", "in", "of", "on", "to", "with"}

def prep_check(sentence):
    sentence_list = sentence.split()
    candidate = []

    # Find article and preposition 
    replace = {}
    for word in sentence_list:
        if word  in atcs:
            replace[word] = atcs
        if word in preps:
            replace[word] = preps

    # Generate all combinationa
    combinations = it.product(*(replace[token] for token in replace))
    combinations = list(combinations)

    can_str_score = -1000000000
    best_score = -100000000
    best_can = sentence
    can_str = sentence
    keylist = list(replace.keys())
    for sublist in combinations:
        can_str = sentence
        for i in range (len(sublist)):
            can_str = can_str.replace(keylist[i], sublist[i])
        candidate.append(can_str)
        can_str_score = model.score(can_str, bos=True, eos=True)/len(can_str.split())
        if can_str_score > best_score:
            best_can = can_str
            best_score = can_str_score
    
    # Remove any duplicates from list
    # candidate = list(dict.fromkeys(candidate))
    return best_can, candidate

print("Task 2 Preposition and Article Check")
task2_input = 'look on an picture in the right'
print("Text:",task2_input,"\n")
task2_result, task2_candidate = prep_check(task2_input)
print("Candidates:")
for i in task2_candidate[:30]:
    print(i)
print("Number of Candidate:", len(task2_candidate))
print()
print("Result:", task2_result,"\n\n\n")

def process_sent(sent):
    ## TODO ##
    candidate1,_ = spelling_check(sent)
    candidate2,_ = prep_check(candidate1)
    return candidate2
    
    
print("Task 3 Combination")
task3_input = 'we descuss a possible meamin by that'
print("Text:",task3_input,"\n")
comb_result = process_sent(task3_input)
print("Result:", comb_result)
