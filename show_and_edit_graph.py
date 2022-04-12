import pickle
pickle.HIGHEST_PROTOCOL
from extra_function import create_folder_dirr
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from glob import glob

# from matplotlib_scalebar.scalebar import ScaleBar
from scalebars import AnchoredScaleBar
global AnchoredScaleBar
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
# for ax in fig1.get_axes():  #show only specific spines
#     if not ax.get_subplotspec().is_first_col():
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
import matplotlib
import numpy as np
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
class Graph_edit:
    def __init__(self,dirr):
        self.fig1=pickle.load(open(dirr, 'rb'))
        self.cell_name=dirr[dirr.rfind('2017'):].split('/')[0]
        self.ax=self.fig1.gca()
    def remove_axis(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
    def change_axis_name(self,title='',xlabel='',ylabel=''):
        if title!='':
            self.ax.set_title(title,fontsize = 30)
        if xlabel!='':
            self.ax.set_xlabel(xlabel,fontsize=20)
        if ylabel!='':
            self.ax.set_ylabel(ylabel,fontsize=20)
    def show(self):
        plt.show()
def graph_plot_again(dirr):
    fig1=pickle.load(open(dirr, 'rb'))
    cell_name=dirr[dirr.rfind('2017'):].split('/')[0]
    fig_name=dirr.split('/')[-1][:-2]
    ax=fig1.gca()
    fig=plt.figure()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    mean_x=np.mean([line.get_xdata().rescale('ms') for line in ax.lines],axis=0)
    mean_x-=mean_x[0]
    mean_y=np.mean([line.get_ydata() for line in ax.lines],axis=0)
    peaks,param=find_peaks(mean_y,prominence=1)
    index2cat=peaks[0]-200
    index2end=index2cat+2000
    for line in ax.lines:
        if len(line.get_xdata()>1):
            x=line.get_xdata().rescale('ms')
            x-=x[0]
            plt.plot(x[index2cat:index2end],line.get_ydata()[index2cat:index2end],alpha=0.02,color=line.get_color())
        else:
            plt.plot(line.get_xdata(),line.get_ydata(),'*')
    plt.xlabel(ax.get_xlabel(),fontsize = 20)
    plt.ylabel(ax.get_ylabel(),fontsize = 20)
    plt.title(ax.get_title(),fontsize = 30)
    plt.plot(mean_x[index2cat:index2end],mean_y[index2cat:index2end],color='black',lw=2)
    return fig,cell_name,fig_name



def graph_edition(dirr,plot_again=False):
    fig1=pickle.load(open(dirr, 'rb'))
    cell_name=dirr[dirr.rfind('2017'):].split('/')[0]
    cell_name=dirr.split('/')[1]
    fig_name=dirr.split('/')[-1][:-2]
    ax=fig1.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    create_folder_dirr('cells_initial_information/'+cell_name+'/final_data/png')
    create_folder_dirr('cells_initial_information/'+cell_name+'/final_data/pdf')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')

    return fig1,cell_name,fig_name

if __name__=="__main__":
    # short_pulse=Graph_edit('cells_outputs_data_short/2017_05_08_A_4-5/data/electrophysio_records/short_pulse/clear_short_pulse_fig.p')

    # cell_name='2017_05_08_A_4-5'
    # fig_fit_hsort_pulse,cell_name,fig_name=

    fig_IV,cell_name,fig_name=graph_edition(glob('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/*/I_V_curve_fit.p')[0])
    ax3=fig_IV.gca()
    ax3.set_xlabel(ax3.get_xlabel(),loc='right')
    ax3.set_ylabel(ax3.get_ylabel(),loc='top')
    for line in ax3.lines:
        line.set_linewidth(3)
        line.set_markersize(15)
    plt.legend(loc='lower right')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    pickle.dump(fig_IV, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))

    plt.show()

    fig_long_pulse,cell_name,fig_name=graph_edition('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse/clear_short_pulse_fig.p')
    # plt.axis('off')
    ax=fig_long_pulse.gca()
    ax.set_title('Long Pulse',fontsize = 30)
    ax.set_xlabel('0.1 ms',fontsize=20)
    ax.set_ylabel('mV',fontsize=20)
    pickle.dump(fig_long_pulse, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))
    scel=AnchoredScaleBar(ax.transData,200/0.1,1,'200 ms','1mV','lower left')
    ax.add_artist(scel)
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    # plt.show()

    fig_syn,cell_name,fig_name=graph_plot_again('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn_fig.p')
    # plt.axis('off')
    ax2=fig_syn.gca()
    # plt.plot(ax2.lines[0].get_xdata(),ax2.lines[0].get_ydata(),'r')
    ax2.set_title('synapse',fontsize = 30)
    ax2.set_xlabel('ms',fontsize=20)
    ax2.set_ylabel('mV',fontsize=20)
    pickle.dump(fig_long_pulse, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))
    scel=AnchoredScaleBar(ax.transData,2000,2,'200 ms','1 mV','center right')
    ax2.add_artist(scel)
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    plt.show()


    a=1
