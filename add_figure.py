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
	import seaborn as sns
	sns.despine(top=True, right=True, left=False, bottom=False)

	return figure


def adgust_subplot(ax,title,x_label,y_label,latter='',titlesize=30,bottom_visiability=True,xylabelsize=20,xytitlesize=20):
	ax.text(-0.2, 1.05, latter, transform=ax.transAxes, size=22,weight="bold")
	# ax.text(-0.1, 0.9, string.ascii_uppercase[i], transform=ax.transAxes, size=25)
	# plt.rc('font', size=20)
	plt.rc('axes', titlesize=xytitlesize)     # fontsize of the axes title
	plt.rc('axes', labelsize=xylabelsize)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=20) #controls default text sizes
	# plt.rc('axes', titlesize=24)     # fontsize of the axes title
	# plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=20)    # fontsize of the tick labels

	#plt.rc('legend', fontsize=30)    # legend fontsize
	# plt.rc('figure', titlesize=40)  # fontsize of the figure title

	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	# ax.spines['bottom'].set_visible(bottom_visiability)
	if not bottom_visiability:
		ax.get_xaxis().set_ticks([])
	ax.set_title(title,fontsize=titlesize)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
