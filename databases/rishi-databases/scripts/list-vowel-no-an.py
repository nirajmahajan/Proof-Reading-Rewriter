import csv
import pickle

# Written by Rishi Agarwal, Department of Computer Science, IIT Bombay.

l = []
with open('words-beginning-vowel-no-an.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        l.append(row[0].lower())
csvFile.close()

with open('../article.pickle', 'wb') as handle:
	pickle.dump(set(l), handle)
