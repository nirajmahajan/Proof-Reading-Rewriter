# Code written by Niraj Mahajan, Department of Computer Science, IIT Bombay
# Extracts all urls from all files in a given directory
# For downloading files with urls (from Gutenburg), refer here
# https://webapps.stackexchange.com/questions/12311/how-to-download-all-english-books-from-gutenberg
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)
parser.add_argument('--out', required=True)

args = vars(parser.parse_args())

if(not os.path.exists(args['path'])):
	print("Invalid Path")
	os._exit(1)

temp = open(args['out'], 'w')
temp.close()

if(not os.path.isdir(args['path'])):
	print("Path is not a directory")
	os._exit(2)


for root, dirs, files in os.walk(args['path'], topdown=False):
	for name in files:
		iter_file = open(os.path.join(root, name), 'r')
		text = iter_file.read()
		a = re.findall(r'http://.*?zip', text)
		b = re.findall(r'https://.*?zip', text)
		iter_file.close()
		
		with open(args['out'], 'a') as out_file:
			for site in a + b:
				out_file.write(site)
				out_file.write("\n")
				out_file.flush()

