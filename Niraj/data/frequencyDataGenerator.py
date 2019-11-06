# Generates frequency data from the raw word list.txt located in data
# credits : https://norvig.com/spell-correct.html
import re
import pickle
from collections import Counter

WORDS = {}

with open('raw_word_list.txt','r') as f:
    for line in f:
        if line.strip() in WORDS:
        	WORDS[line.strip()] += 1
        else: 
        	WORDS[line.strip()] = 1

with open('freq.pickle', 'wb') as handle:
	pickle.dump(WORDS, handle)
