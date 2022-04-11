import pickle
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

def graph_edition(dirr):
    fig1=pickle.load(open(dirr, 'rb'))
    fig=plt.figure()
    for ax in fig.get_axes():  #show only specific spines
        if not ax.get_subplotspec().is_first_col():
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
    ax=fig1.gca()
    for line in ax.lines:
        plt.plot(line.get_xdata(),line.get_ydata())
        # a=ax._get_axis_list()
        plt.xlabel(ax.get_xlabel(),)
        plt.ylabel(ax.get_ylabel(),)
        plt.title(ax.get_title(),)
    return fig
