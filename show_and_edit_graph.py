import pickle
import re
from read_passive_parameters_csv import get_passive_from_Ra
pickle.HIGHEST_PROTOCOL
from extra_function import create_folder_dirr
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from glob import glob

# from matplotlib_scalebar.scalebar import ScaleBar
from scalebars import AnchoredScaleBar
from scalbar_sapir import AnchoredHScaleBar
from open_pickle import read_from_pickle
# global AnchoredScaleBar
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
# for ax in fig1.get_axes():  #show only specific spines
#     if not ax.get_subplotspec().is_first_col():
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
import matplotlib
import numpy as np
from matplotlib_scalebar.scalebar import ScaleBar

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def get_Moo_label(dirr):
    data=read_from_pickle(dirr+'final_pop.p')['mean_final_pop']
    g_AMPA=str(round(data['mean_final_pop'][data['parameters'].index('weight_AMPA')]*3,3))+'nS'
    tau1=str(round(data['mean_final_pop'][data['parameters'].index('exp2syn_tau1')],3))+'ms'
    tau2=str(round(data['mean_final_pop'][data['parameters'].index('exp2syn_tau2')],3))+'ms'

    g_NMDA=str(round(data['mean_final_pop'][data['parameters'].index('weight_NMDA')]*3,3))
    NMDA_tau1=str(round(data['mean_final_pop'][data['parameters'].index('NMDA_tau_r_NMDA')],3))
    NMDA_tau2=str(round(data['mean_final_pop'][data['parameters'].index('NMDA_tau_d_NMDA')],3))
    return 'g_AMPA='+g_AMPA+'\n'+'tau1='+tau1+' tau2='+tau2+'\n'+'gmax_NMDA='+g_NMDA+'\n'+'tau1='+NMDA_tau1+' tau2='+NMDA_tau2
class Graph_edit:
    def __init__(self,dirr,ax_tot=None,remove_axis=True,change_title_size=True,change_lw=False,remove_title='True',fig=None):
        self.fig1=pickle.load(open(dirr, 'rb'))
        plt.gcf()
        self.cell_name=dirr[dirr.rfind('201'):].split('/')[0]
        if ax_tot is None:
            self.ax=self.fig1.gca()
        else:
            self.ax=self.fig1.gca()
            move_axes(self.ax,self.fig)
        # plt.close(self.fig1)
        self.dirr=dirr

        #the function runing:
        if 'IV' in self.dirr:
            self.change_axis_place()
        elif remove_axis:
            self.remove_axis()
            # self.add_scalebar()
        if change_title_size:
            self.change_axis_name()
        if change_lw:
            self.change_lw()
        self.figure_shape()
        self.savefig()
        if remove_title:
            self.change_axis_name(title='remove')

    def plot_again(self):
        pass
    def get_figure(self):
        return self.fig1.get_figure()
    def remove_axis(self):
        # self.ax.set_axis_off()
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        # self.ax.spines['bottom'].set_visible(False)
        # self.ax.spines['left'].set_visible(False)
        # self.ax.set_axis_off()

    def change_axis_place(self):
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_position('zero')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def change_axis_name(self,title='',xlabel='',ylabel=''):
        if title!='':
            if title=='remove':
                self.ax.set_title('')
            else:
                self.ax.set_title(title,fontsize = 10)
        if xlabel!='':
            self.ax.set_xlabel(xlabel,fontsize=5)
        if ylabel!='':
            self.ax.set_ylabel(ylabel,fontsize=5)
    def show(self):
        plt.show()
    def add_scalebar(self,units="um",length=100,location="lower left",orientation="horizontal"):
        #orientation can be vertical or horizontal
        if units=="um":
            self.ax.add_artist(ScaleBar(1, units, fixed_value=length, location=location,rotation=orientation))
        else:
            # scel=AnchoredScaleBar(self.ax.transData,200/0.1,1,'200ms','1mV','lower left')
            scel2=AnchoredHScaleBar(ax=self.ax,size_x=200*0.1, size_y=1, linekw=dict(color="crimson"), x_to_ms=lambda x: x/0.1)
            # scel=AnchoredHScaleBar(ax=ax,size_x=1.2, linekw=dict(color="crimson"))
            # self.ax.add_artist(scel)
            self.ax.add_artist(scel2)
    def change_lw(self,multipule_lw=2):
        for line in self.ax.lines:
            line.set_linewidth(line.get_lw()*multipule_lw)
            # line.set_markersize(line.get_s()*multipule_lw)
    def change_color(self,color,lines):
        for line in self.ax.lines:
            if not line in lines: continue
            line.set_color(color)
    def savefig(self,file_type=''):
        dirr_save=self.dirr[:self.dirr.rfind('/')]+'/edit/'+self.dirr.split('/')[-1][:-2]
        create_folder_dirr(dirr_save[:dirr_save.rfind('/')])
        if not file_type=='':file_type='.'+file_type
        plt.savefig(dirr_save)
        pickle.dump(self.fig1, open(dirr_save+'.p', 'wb'))
        plt.close(self.fig1)
        return dirr_save+'.png'
    def add_text(self,text='',x=0.25,y=0.25,color='black',fontsize=20):
        if text=='short_pulse':
            title=self.ax.get_title()
            RM,RA,CM=re.findall(r"[-+]?(?:\d*\.\d+|\d+)",title[title.find('RM='):])
            # Ra=int(re.findall(r"[-+]?(?:\d*\.\d+|\d+)",self.dirr))[0]
            # RA,CM,RM=get_passive_from_Ra(cell_name,Ra)
            text='RA='+RA+'\n'+'CM='+CM+'\n'+'RM='+RM+'\n'
        elif 'final_pop' in text:
            text=get_Moo_label(text)
            # text='g_AMPA='+CM+'nS\n'+'tau1='+RA+' tau2='+'\n'+'gmax_NMDA='+CM+'\n'+'RM='+RM+'\n'
        plt.text(x,y,text,fontsize=fontsize, color=color)
    def figure_shape(self,hight=10,widght=10):
        self.fig1.set_figheight(hight)
        self.fig1.set_figwidth(widght)
    def first_edition(self):
        self.remove_axis()
        self.change_axis_name()
        # self.change_lw()
        # self.add_scalebar()
        self.add_text()
        self.savefig()
        # self.show()

def move_axes(ax, fig, subplot_spec=111):
    """Move an Axes object from a figure to a new pyplot managed Figure in
    the specified subplot."""

    # get a reference to the old figure context so we can release it
    old_fig = ax.figure

    # remove the Axes from it's original Figure context
    ax.remove()

    # set the pointer from the Axes to the new figure
    ax.figure = fig

    # add the Axes to the registry of axes for the figure
    fig.axes.append(ax)
    # twice, I don't know why...
    fig.add_axes(ax)

    # then to actually show the Axes in the new figure we have to make
    # a subplot with the positions etc for the Axes to go, so make a
    # subplot which will have a dummy Axes
    dummy_ax = fig.add_subplot(subplot_spec)

    # then copy the relevant data from the dummy to the ax
    ax.set_position(dummy_ax.get_position())

    # then remove the dummy
    dummy_ax.remove()

    # close the figure the original axis was bound to
    plt.close(old_fig)

# def show_picture(dirr):
#     fig1=pickle.load(open(dirr, 'rb'))
#     cell_name=dirr[dirr.rfind('201'):].split('/')[0]
#     fig_name=dirr.split('/')[-1][:-2]
#     ax=fig1.gca()
#     for line in ax.lines:
#         plt.plot(line.get_xdata(),line.get_ydata(),'*')
#     plt.xlabel(ax.get_xlabel(),fontsize = 20)
#     plt.ylabel(ax.get_ylabel(),fontsize = 20)
#     plt.title(ax.get_title(),fontsize = 30)
#     plt.show()
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
    # short_pulse=Graph_edit('cells_outputs_data_short/2017_05_08_A_4-5(0)(0)/data/electrophysio_records/short_pulse/clear_short_pulse_fig.p')

    cell_name='2017_05_08_A_4-5(0)(0)'
    fig_fit_short_pulse,cell_name,fig_name=graph_edition('cells_outputs_data_short/'+cell_name+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*1.0&F_shrinkage=1.0/const_param/RA/fit RA=73.p')
    ax0=fig_fit_short_pulse.gca()
    for line in ax0.lines:
        line.set_linewidth(3)
    plt.legend(loc='lower right')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    pickle.dump(fig_fit_short_pulse, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))
    # plt.show()
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

    # plt.show()

    fig_long_pulse,cell_name,fig_name=graph_edition('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse/clear_short_pulse_fig.p')
    # plt.axis('off')
    ax=fig_long_pulse.gca()
    ax.set_title('Long Pulse',fontsize = 30)
    ax.set_xlabel('0.1 ms',fontsize=20)
    ax.set_ylabel('mV',fontsize=20)
    pickle.dump(fig_long_pulse, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))
    scel=AnchoredScaleBar(ax.transData,200/0.1,1,'200 ms','1mV','lower left')
    scel2=AnchoredHScaleBar(ax=ax,size_x=200, size_y=1, linekw=dict(color="crimson"), x_to_ms=lambda x: x/0.1)
    # scel=AnchoredHScaleBar(ax=ax,size_x=1.2, linekw=dict(color="crimson"))
    ax.add_artist(scel)
    ax.add_artist(scel2)
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    plt.show()
    plt.close('all')

    fig_syn,cell_name,fig_name=graph_plot_again('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn_fig.p')
    # plt.axis('off')
    ax2=fig_syn.gca()
    # plt.plot(ax2.lines[0].get_xdata(),ax2.lines[0].get_ydata(),'r')
    ax2.set_title('synapse',fontsize = 30)
    ax2.set_xlabel('ms',fontsize=20)
    ax2.set_ylabel('mV',fontsize=20)
    # pickle.dump(fig_long_pulse, open('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png', 'wb'))
    scel=AnchoredScaleBar(ax2.transData,20,2,'200 ms','1 mV','center right')
    scel2=AnchoredHScaleBar(ax=ax2,size_x=2/0.1, size_y=1, linekw=dict(color="black"), txtkw=dict(fontsize=5), loc='center left')
    ax2.add_artist(scel)
    ax2.add_artist(scel2)
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+fig_name+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+fig_name+'.pdf')
    plt.show()


    a=1
