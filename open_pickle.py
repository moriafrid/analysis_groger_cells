import pickle
import matplotlib.pyplot as plt
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

def show_picture(dirr):
	fig1=pickle.load(open(dirr, 'rb'))
	cell_name=dirr[dirr.rfind('2017'):].split('/')[0]
	fig_name=dirr.split('/')[-1][:-2]
	ax=fig1.gca()
	for line in ax.lines:
		print(len(line.get_xdata()))
		if len(line.get_xdata()>10):
			plt.plot(line.get_xdata(),line.get_ydata(),color=line.get_color(),label=line.get_label())
		else:
			print('*')
			plt.scatter(line.get_xdata(),line.get_ydata(),color=line.get_color(),label=line.get_label())
	plt.legend()
	plt.xlabel(ax.get_xlabel(),fontsize = 20)
	plt.ylabel(ax.get_ylabel(),fontsize = 20)
	plt.title(ax.get_title(),fontsize = 30)
	plt.show()
