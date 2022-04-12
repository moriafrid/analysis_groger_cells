import pickle
pickle.HIGHEST_PROTOCOL
from extra_function import create_folder_dirr
import matplotlib.pyplot as plt
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
def graph_plot_again(dirr):
    fig1=pickle.load(open(dirr, 'rb'))
    fig=plt.figure()
    ax=fig1.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    for line in ax.lines:
        line.set_linewidth(0.5)
        # scel=AnchoredScaleBar()
        bar_x=AnchoredSizeBar(ax.transData,200/0.1,'200 ms','lower left',frameon=False,label_top=True,size_vertical=0.05)
        if len(line.get_xdata()>1):
            plt.plot(line.get_xdata(),line.get_ydata())
        else:
            plt.plot(line.get_xdata(),line.get_ydata(),'*')
        # a=ax._get_axis_list()
        plt.xlabel(ax.get_xlabel(),fontsize = 20)
        plt.ylabel(ax.get_ylabel(),fontsize = 20)
        plt.title(ax.get_title(),fontsize = 30)
        plt.axis('off')
    pass
def graph_edition(dirr,plot_again=False):
    fig1=pickle.load(open(dirr, 'rb'))
    cell_name=dirr[dirr.rfind('2017'):].split('/')[0]
    plt.axis('off')
    if plot_again:
        fig=plt.figure()
    ax=fig1.gca()
    ax.set_xlabel('0.1 ms',fontsize=20)
    ax.set_ylabel('mV',fontsize=20)

    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    scel=AnchoredScaleBar(ax.transData,200/0.1,1,'200 ms','1mV','lower left')
    bar_x=AnchoredSizeBar(ax.transData,200/0.1,'200 ms','center left',frameon=False,label_top=True,size_vertical=0.05)
    # bar_x=AnchoredSizeBar(ax.get_xaxis_transform(),200/0.1,'200 ms','lower left',frameon=False,label_top=True,size_vertical=0.05)
    # bar_x=AnchoredSizeBar(ax.get_yaxis_transform(),200/0.1,'200 ms','lower left',frameon=False,label_top=True,size_vertical=0.05)

    bar_x.set_width(0.01)
    bar_x.set_height(0.0001)
    bar_x.set_snap(False)
    ax.add_artist(scel)

    ax.set_title('Long Pulse',fontsize = 30)
    # ax.set_yticklabels('mV')

    # scalebar_x = ScaleBar(0.08, units="m",dimension="si-length", length_fraction=0.25)
    # scalebar_y = ScaleBar(0.08, units="m",rotation="vertical",scale_loc="bottom")
    # ax.add_artist(scalebar_y)
    # ax.add_artist(scalebar_x)


    # example_line_x=np.mean([line.get_xdata() for line in ax.lines],axis=0)
    # example_line_y=np.mean([line.get_ydata() for line in ax.lines],axis=0)
    example_line_x=ax.lines[0].get_xdata()
    example_line_y=ax.lines[0].get_ydata()
        # ax.bar(example_line_x[0:100],0.5,bottom=example_line_y[0],)
        # ax.annotate('mv',example_line_x[0:100])
        # ax.annotate('ms',example_line_y[0:100])
        # ax.lines[0].set_color('red')
        # plt.set_color('r')
    for line in ax.lines:
        line.set_linewidth(0.5)
        if plot_again:
            if len(line.get_xdata()>1):
                plt.plot(line.get_xdata(),line.get_ydata())
            else:
                plt.plot(line.get_xdata(),line.get_ydata(),'*')
            # a=ax._get_axis_list()
            plt.xlabel(ax.get_xlabel(),fontsize = 20)
            plt.ylabel(ax.get_ylabel(),fontsize = 20)
            plt.title(ax.get_title(),fontsize = 30)
            plt.axis('off')
    plt.show()
    # plt.close()
    create_folder_dirr('cells_initial_information/'+cell_name+'/final_data/png')
    create_folder_dirr('cells_initial_information/'+cell_name+'/final_data/pdf')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/png/'+dirr.split('/')[-1][:-2]+'.png')
    plt.savefig('cells_initial_information/'+cell_name+'/final_data/pdf/'+dirr.split('/')[-1][:-2]+'.pdf')
    with open('cells_initial_information/'+cell_name+'/final_data/png/'+dirr.split('/')[-1][:-2]+'.p', 'wb') as file:
        pickle.dump(fig1, file)
    return fig

if __name__=="__main__":
    graph_edition('cells_outputs_data_short/2017_05_08_A_4-5/data/electrophysio_records/short_pulse/clear_short_pulse_fig.p')
    graph_edition('cells_outputs_data_short/2017_05_08_A_4-5/data/electrophysio_records/syn/clear_syn_fig.p')
