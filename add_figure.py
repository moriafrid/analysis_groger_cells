import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def add_figure(title,x_label,y_label,titlesize=20,bottom_visiability=True,xylabelsize=18,xytitlesize=18):
	plt.close()
	figure=plt.figure(figsize=(5, 5))
	figure.subplots_adjust(left=0.2,right=0.9,top=0.9,bottom=0.15)
	plt.rc('axes', titlesize=xytitlesize)     # fontsize of the axes title
	plt.rc('axes', labelsize=xylabelsize)    # fontsize of the x and y labels
	# plt.rc('axes', titlesize=24)     # fontsize of the axes title
	# plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
	plt.title(title,fontsize=titlesize)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	import seaborn as sns
	sns.despine(top=True, right=True, left=False, bottom=False)

	return figure


def adgust_subplot(ax,title,x_label,y_label,latter='',titlesize=20,bottom_visiability=True,xylabelsize=20,xytitlesize=20,e_label=True,xlatter=-0.2,ylatter=1.05):
	ax.text(xlatter, ylatter, latter, transform=ax.transAxes, size=22,weight="bold")
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
	if e_label==True:
		ax.ticklabel_format(style='sci',scilimits=(0,0),axis='y')

	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	# ax.spines['bottom'].set_visible(bottom_visiability)
	if not bottom_visiability:
		ax.get_xaxis().set_ticks([])
	ax.set_title(title,fontsize=titlesize)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
