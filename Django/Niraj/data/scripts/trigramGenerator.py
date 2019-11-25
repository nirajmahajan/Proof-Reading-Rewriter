# creates a file with all possible trigrams from an input file (processed)
# input path is given by argparse
# outputs each trigram seperated by a $ symbol
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)

args = vars(parser.parse_args())

if(not os.path.exists(args['path'])):
	print("Invalid Path")
	os._exit(1)

if(not os.path.isfile(args['path'])):
	print("Path does not have a file")
	os._exit(2)

outf = open('trigout.txt', 'w')
with open(args['path'], 'r') as infile:
	elem = infile.readline()
	word_list = elem.split()
	for i in range(0, len(word_list)-2):
		w1 = word_list[i];
		w2 = word_list[i+1];
		w3 = word_list[i+2];
		outf.write(w1 + '$' + w2 + '$' + w3 + '\n')

outf.close()
