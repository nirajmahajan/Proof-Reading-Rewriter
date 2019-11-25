import sqlite3
import os
import pickle

dic = {}
# Establish connection to the sql database
try:
	conn = sqlite3.connect('../dumps/Trigram-Bigram-Dictionary.db')
	c = conn.cursor()
except Exception as e:
	raise e
	os._exit(1)

print('Fetching data', flush=True)
c.execute('''SELECT first, second, freq FROM Bigrams''')
rows = c.fetchall()
print('DATA fetched', flush=True)

count = 1
for row in rows:
	count = count +1
	if(count % 100000 == 0):
		print(count, flush = True)
	w1 = row[0]
	w2 = row[1]
	w3 = int(row[2])
	key1 = w1+'$'+w2
	dic[key1] = dic.get(key1, 0) + w3

print('old data added', flush = True)
c.close()
conn.commit()
conn.close()

with open('big.pickle', 'wb') as handle:
    pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

