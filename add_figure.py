import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def add_figure(title,x_label,y_label):
	plt.close()
	figure=plt.figure()
	plt.title(title,fontsize=15)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	return figure
