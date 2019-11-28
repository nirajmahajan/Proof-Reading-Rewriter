# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.

# Generates frequency data from the raw word list.txt located in data
# credits : https://norvig.com/spell-correct.html
import re
import os
import pickle
import argparse
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)
parser.add_argument('--out', required=True)

args = vars(parser.parse_args())

if(not os.path.exists(args['path'])):
	print("Invalid Path")
	os._exit(1)

if(not os.path.isfile(args['path'])):
	print("Path does not have a file")
	os._exit(2)

WORDS = {}
# WORDSET = {'a'}

counter = 0
with open(args['path'],'r') as f:
    for line in f:
        if line.strip() in WORDS:
        	WORDS[line.strip()] += 1
        else: 
        	WORDS[line.strip()] = 1	
        	# WORDSET.add(line.strip())

with open(args['out'], 'wb') as handle:
	pickle.dump(WORDS, handle)

# with open('../dumps/db.pickle', 'wb') as handle:
# 	pickle.dump(WORDSET, handle)
