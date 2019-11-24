# Loads a pickle with elements as bigrams seperated by $ along with their frequencies
# Adds this into the sql database
import os
import argparse
import sqlite3
import pickle

# parser = argparse.ArgumentParser()
# parser.add_argument('--path', required=True)

# args = vars(parser.parse_args())

# if(not os.path.exists(args['path'])):
# 	print("Invalid Path")
# 	os._exit(1)

# if(not os.path.isfile(args['path'])):
# 	print("Path does not have a file")
# 	os._exit(2)

with open('big.pickle', 'rb') as handle:
    BIG = pickle.load(handle)
print('Loaded the dictionary', flush = True)

conn = sqlite3.connect('../dumps/Trigram-Bigram-Dictionary.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS Bigrams''')

c.execute('''CREATE TABLE Bigrams
             (id INTEGER PRIMARY KEY,first text, second text, freq INTEGER)''')
          
print('Created the table', flush=True)
count = 0
sql_str = "INSERT into Bigrams(first, second, freq) VALUES (?, ?, ?)"
data = []
# outf = open('outBigWithFreq.txt', 'w')
# outf.write('first,second,freq\n')
# with open(args['path'], 'r') as infile:
for elem, freq in sorted(BIG.items(), key = lambda x: x[1], reverse=True):
	count = count + 1;
	if(count % 100000 == 0):
		print(count, end = ", ", flush=True)
		c.executemany(sql_str, data)
		conn.commit()
		data = []
	word_list = elem.split('$')
	w1 = word_list[0]
	w2 = word_list[1]
	# c.execute('''SELECT id, freq FROM Bigrams WHERE first = ? AND second = ?''', (w1, w2))
	# data1 = c.fetchall()

	# if(len(data1) == 0):
	# 	c.execute('''INSERT into Bigrams(first, second, freq) values(?,?,?)''', (w1, w2, 1))
	# else:
	# 	c.execute('''UPDATE Bigrams SET freq = ? WHERE id = ?''', (data1[0][1]+1, data1[0][0]))
	data.append((w1, w2, freq,))

print('\nData generated', flush = True)

# outf.close()
c.executemany(sql_str, data)
conn.commit()
c.close()
conn.close()			