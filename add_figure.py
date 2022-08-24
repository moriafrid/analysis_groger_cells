import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def add_figure(title,x_label,y_label):
	plt.close()
	figure=plt.figure()
	plt.rc('font', size=20)          # controls default text sizes
	plt.rc('axes', titlesize=16)     # fontsize of the axes title
	plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=10)    # fontsize of the tick labels
	plt.rc('legend', fontsize=16)    # legend fontsize
	plt.rc('figure', titlesize=22)  # fontsize of the figure title
	plt.title(title,fontsize=15)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	return figure


def adgust_subplot(ax,title,x_label,y_label):
	plt.rc('font', size=20)          # controls default text sizes
	plt.rc('axes', titlesize=24)     # fontsize of the axes title
	plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=18)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=18)    # fontsize of the tick labels
	#plt.rc('legend', fontsize=30)    # legend fontsize
	plt.rc('figure', titlesize=40)  # fontsize of the figure title
	ax.set_title(title,fontsize=30)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
