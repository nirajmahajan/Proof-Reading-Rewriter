# Loads a text with dictionary words
# Adds this into the sql database
import os
import argparse
import sqlite3

conn = sqlite3.connect('../dumps/Trigram-Bigram-Dictionary.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Words''')

c.execute('''CREATE TABLE Words
             (id INTEGER PRIMARY KEY,word text)''')
          
print('Created Table', flush=True)

sql_str = "INSERT into Words (word) values(?)"
inf = open('../textfiles/db.txt', 'r')
count = 1
data = []
for line in inf:
	count = count + 1;
	if(count % 100000 == 0):
		print(count, end = ", ", flush=True)
		c.executemany(sql_str, data)
		conn.commit()
		data = []
	data.append([line.strip()])
	
print('\nData generated', flush = True)
# outf.close()
c.executemany(sql_str, data)
conn.commit()
c.close()
conn.close()			