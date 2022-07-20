import pickle
from glob import glob
from matplotlib_scalebar.scalebar import ScaleBar
from plot_morphology_Yoni import plot_morph
import matplotlib.pyplot as plt
def short_pulse(ax, dir):
    # d = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_05_08_A_4-5/clear_short_pulse.p'
    data = pickle.load(open(dir, 'rb'))
    T = data[1]-data[1][0] # in sec
    T = T.rescale('ms')
    for v in data[0]:
        ax.plot(T, v, color='grey',alpha=0.2,lw=0.1)
    ax.plot(T, data[0].mean(axis=0), color='k')
    # add scale bar
    ax.plot([0,0], [-2, -4], color='k')
    ax.plot([0, 200],[-4, -4], color='k')
    ax.text(-50, -3.5, '2 mV', rotation=90)
    ax.text(50, -4.7, '200 ms')
    ax.set_axis_off()
    return ax

def syn_mean(ax, dir):
    # d = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_05_08_A_4-5/clear_short_pulse.p'
    data = pickle.load(open(dir, 'rb'))
    T = data[1]-data[1][0] # in sec
    T = T.rescale('ms')
    for v in data[0]:
        ax.plot(T, v, color='grey',alpha=0.2,lw=0.1)
    ax.plot(T, data[0].mean(axis=0), color='k')
    # add scale bar
    ax.plot([200,200], [1, 1.5], color='k')
    ax.plot([200,250],[1, 1], color='k')
    ax.text(180, 1.15, '0.5 mV', rotation=90)
    ax.text(210, 0.8, '50 ms')
    ax.set_axis_off()
    return ax
from open_pickle import read_from_pickle
def find_RA(file_dirr):
    for passive_params in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        try_find=glob(file_dirr+'fit RA=*_'+passive_params+'.p')
        if len(try_find)>0:
            return passive_params

def plot_pickle(ax,dirr,scale_bar_type,remove_begin=True):
    fig1=read_from_pickle(dirr)
    ax_temp=fig1.gca()
    plt.close()
    for i,line in enumerate(ax_temp.lines):
        x=line.get_data()[0]
        y=line.get_data()[1]
        if len(x>1) and remove_begin:
            x=x-x[0]
            # y=y-y[0]
        if scale_bar_type=='fit_short_pulse':
            label=str(i)
        else:
            label=line.get_label()
        ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw(),alpha=line.get_alpha(),label=label)
        if len(x)==1:
            ax.scatter(x,y,color=line.get_color(),s=line.get_markersize(),alpha=line.get_alpha(),label=label)
    ax.legend()
    add_scale_bar(ax,scale_bar_type)
    ax.set_axis_off()

    return ax

def add_scale_bar(ax,type):
    if type=='clear_short_pulse':
        base_y=-4
        base_x=0
        ax.plot([base_x,base_x], [base_y, base_y+2], color='k')
        ax.plot([base_x,base_x+100/1000],[base_y, base_y], color='k')
        ax.text(base_x-30/1000, base_y+0.1, '2 mV', rotation=90)
        ax.text(base_x+10/1000, base_y-0.3, '100 ms')
    elif type=="fit_short_pulse":
        base_y=-80
        base_x=0
        ax.plot([base_x,base_x], [base_y, base_y+2], color='k')
        ax.plot([base_x,base_x+100],[base_y, base_y], color='k')
        ax.text(base_x-30, base_y, '2 mV', rotation=90)
        ax.text(base_x+10, base_y-0.3, '100 ms')
    elif type=='clear_syn':
        base_y=1.5
        base_x=0.18
        ax.plot([base_x,base_x], [base_y, base_y+0.5], color='k')
        ax.plot([base_x,base_x+50/1000],[base_y, base_y], color='k')
        ax.text(base_x-20/1000, base_y, '0.5 mV', rotation=90)
        ax.text(base_x+10/1000, base_y-0.2, '50 ms')
    elif type=='fit_syn':
        base_y=-76.2-0.5
        ax.plot([200,200], [base_y, base_y+0.5], color='k')
        ax.plot([200,250],[base_y, base_y], color='k')
        ax.text(180, base_y, '0.5 mV', rotation=90)
        ax.text(210, base_y-0.1, '50 ms')
    elif type=='neuron':
        ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower left",rotation="horizontal"))
        ax.set_axis_off()


cell_name = '2017_05_08_A_4-5'
fig = plt.figure(figsize=(20, 20))
# fig.set_figheight(6)
# fig.set_figwidth(6)
shapes = (2, 4)
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
# plt.subplots_adjust(hspace=0.3, wspace=0.3)

temp='final_data/2017_05_08_A_4-5/neuron_morphology_fig.p'
base_dir='final_data/'+cell_name+'/'
decided_passive_params=find_RA(base_dir)
plot_morph(ax1, cell_name, without_axons=True)
plot_pickle(ax3,glob(base_dir+'fit *'+decided_passive_params+'.p')[0],'fit_short_pulse',remove_begin=False)
# plot_pickle(ax1,base_dir+'neuron_morphology_fig.p','neuron',remove_begin=False)
plot_pickle(ax5,glob(base_dir+'AMPA&NMDA_soma_*'+decided_passive_params+'.p')[0],'fit_syn')
plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')

# passive_fit(ax3,glob(base_dir+'fit RA=*_'+decided_passive_params+'.p')[0])
# syn_mean(ax4, 'cells_initial_information/'+cell_name+'/clear_syn_split.p')
# plot_morph(ax1, cell_name, without_axons=True)
# short_pulse(ax2, 'cells_initial_information/'+cell_name+'/clear_short_pulse.p')
# fig1=pickle.load(open(temp, 'rb'))
# for l in  list(fig1.axes[0].get_lines()):
#
#     ax1.plot(l)
plt.show()
