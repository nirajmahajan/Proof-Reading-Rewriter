import csv
import pickle

l = {}
with open('participles.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		lis = row[0].strip().split()
		l[lis[0]] = lis[2]
csvFile.close()

with open('participles.pickle', 'wb') as handle:
	pickle.dump(l, handle)
