# Written by Niraj Mahajan, Department of Computer Science, IIT Bombay.

import os
import pickle

OLD = {}

inf = open('out.sql', 'r')

count = 0
for line in inf:
	count = count +1
	if(count % 100000 == 0):
		print(count, end = ' ', flush = True)
	row = line.split('$')
	w1 = row[0]
	w2 = row[1]
	w3 = row[2]
	w4 = int(row[3])
	key1 = w1+'$'+w2+'$'+w3
	OLD[key1] = OLD.get(key1, 0) + w4

print('new data added', flush = True)

with open('trig.pickle', 'wb') as handle:
    pickle.dump(OLD, handle, protocol=pickle.HIGHEST_PROTOCOL)

