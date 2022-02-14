import pickle
def read_from_pickle(path):
	#print('opening '+path)
	with open(path, 'rb') as file:
		try:
			while True:
				object_file=pickle.load(file)
		except EOFError:
			pass
		file.close()
	return object_file
