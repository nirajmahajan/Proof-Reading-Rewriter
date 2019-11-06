import pickle

with open('freq.pickle', 'rb') as handle:
	FREQ_TABLE = pickle.load(handle)

with open('db.pickle', 'rb') as handle:
	DB = pickle.load(handle)

