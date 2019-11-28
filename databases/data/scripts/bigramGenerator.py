# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.

# creates a file with all possible bigrams from an input file (proccessed)
# input path is given by argparse
# outputs each bigram seperated by a $ symbol
import os
import argparse
# import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)

args = vars(parser.parse_args())

if(not os.path.exists(args['path'])):
	print("Invalid Path")
	os._exit(1)

if(not os.path.isfile(args['path'])):
	print("Path does not have a file")
	os._exit(2)

count = 0
outf = open('bigout.txt', 'w')
with open(args['path'], 'r') as infile:
	elem = infile.readline()
	word_list = elem.split()
	for i in range(0, len(word_list)-1):
		w1 = word_list[i];
		w2 = word_list[i+1];
		outf.write(w1 + '$' + w2 + '\n')

outf.close()
