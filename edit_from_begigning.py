import pickle
from glob import glob
from plot_morphology_Yoni import plot_morph
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
def clear_short_pulse(ax, dir):
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

def clear_syn_mean(ax, dir):
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
def plot_syn_model(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('data_')+4:])[0])
    T=dict_syn['time']
    V=dict_syn['voltage']
    ax.plot(T,V['experiment']-E_PAS,color = 'black',alpha=0.2,label='experiment',lw=7)
    ax.plot(T,V['Model']-E_PAS,c='red',lw=3,label='Model',alpha=0.5)
    ax.plot(T,V['V_AMPA']-E_PAS,c='#18852a',linestyle ="--",alpha=1)
    ax.plot(T,V['V_NMDA']-E_PAS,c='#03b5fc',linestyle ="--",alpha=1)
    place_text=0.5
    ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c='#18852a',size='medium')
    ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c='#03b5fc',size='medium')
    plt.legend(loc="upper left",prop={'size': 7})
    add_scale_bar(ax,'fit_syn')

def plot_short_pulse_model(ax,dirr):
    global  E_PAS
    dict_result=read_from_pickle(dirr)
    experiment=dict_result['experiment']
    model=dict_result['model']
    fit_decay=dict_result['fit_decay']
    fit_max=dict_result['fit_Rin']
    parameters=dict_result['parameter']
    E_PAS=parameters['E_PAS']
    ax.plot(experiment['T'], experiment['V']-E_PAS, color = 'black',alpha=0.2,label='experiment',lw=7)
    ax.plot(fit_decay['T'], fit_decay['V']-E_PAS, color = 'b',alpha=0.3,label='fit decay',lw=4)
    ax.plot(fit_max['T'], fit_max['V']-E_PAS,color = 'yellow',alpha=0.8,label='fit maxV',lw=4)
    ax.plot(model['T'][:len(model['V'])], model['V']-E_PAS, color = 'red', linestyle ="-",alpha=0.5,label='Model',lw=3)
    ax.text(500,-2,"RM="+str(round(parameters['RM']))+"\nRA="+str(round(parameters['RA']))+"\nCM="+str(round(parameters['CM'])),size='large')
    ax.legend(loc='lower right',prop={'size': 7})
    add_scale_bar(ax,'fit_short_pulse')
    return ax

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
            # if "fit" in dirr

        ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw(),alpha=line.get_alpha(),label=label)
        if len(x)==1:
            ax.scatter(x,y,color=line.get_color(),s=line.get_markersize(),alpha=line.get_alpha(),label=label)
    add_scale_bar(ax,scale_bar_type)
    return ax

def add_scale_bar(ax,type):
    if type=='clear_short_pulse':
        base_y=-4
        base_x=100/1000
        ax.plot([base_x,base_x], [base_y, base_y+1], color='k')
        ax.plot([base_x,base_x+100/1000],[base_y, base_y], color='k')
        ax.text(base_x-50/1000, base_y+0.1, '1 mV', rotation=90)
        ax.text(base_x+10/1000, base_y-0.5, '100 ms')
        x_lim=550/1000
        y_lim=7
        if cell_name=='2017_03_04_A_6-7':
            x_lim=700/1000

        if cell_name=='2017_02_20_B':
            y_lim=10
    elif type=="fit_short_pulse":
        base_y=-4
        base_x=100
        ax.plot([base_x,base_x], [base_y, base_y+1], color='k')
        ax.plot([base_x,base_x+100],[base_y, base_y], color='k')
        ax.text(base_x-40, base_y+0.1, '1 mV', rotation=90)
        ax.text(base_x, base_y-0.4, '100 ms')
        x_lim=550
        y_lim=7
        if cell_name=='2017_03_04_A_6-7':
            x_lim=700
        if cell_name=='2017_02_20_B':
            y_lim=10
    elif type=='clear_syn':
        base_y=1.5
        base_x=180/1000
        ax.plot([base_x,base_x], [base_y, base_y+0.5], color='k')
        ax.plot([base_x,base_x+50/1000],[base_y, base_y], color='k')
        ax.text(base_x-20/1000, base_y, '0.5 mV', rotation=90)
        ax.text(base_x+10/1000, base_y-0.2, '50 ms')
        x_lim=0.3
        y_lim=3.1
        if cell_name=='2017_03_04_A_6-7':
            y_lim=6.5

    elif type=='fit_syn':
        base_y=1.0
        base_x=200
        ax.plot([base_x,base_x], [base_y, base_y+0.6], color='k')
        ax.plot([base_x,base_x+50],[base_y, base_y], color='k')
        ax.text(base_x-20, base_y+0.1, '0.5 mV', rotation=90)
        ax.text(base_x+5, base_y-0.2, '50 ms')
        x_lim=300
        if cell_name=='2017_03_04_A_6-7':
            y_lim=6.5
    elif type=='neuron':
        ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower left",rotation="horizontal"))
    if cell_name=='2016_04_16_A':
        y_lim+=2
    left=ax.get_xlim()[0]
    right=ax.get_xlim()[1]
    bottom=ax.get_ylim()[0]
    ax.set_xlim(left=right-x_lim,right = right)
    ax.set_ylim(bottom=bottom, top =bottom+y_lim)
    plt.rcParams.update({'font.size': 12})
    ax.set_axis_off()

# cell_name = '2017_05_08_A_4-5'
cell_name = read_from_pickle('cells_name2.p')[9]
fig = plt.figure(figsize=(20, 20))
fig.suptitle(cell_name, fontsize=20)# fig.set_figheight(6)
# fig.set_figwidth(6)
shapes = (2, 4)
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
# plt.subplots_adjust(hspace=0.3, wspace=0.3)
base_dir='final_data/'+cell_name+'/'
decided_passive_params=find_RA(base_dir)
plot_morph(ax1, cell_name, without_axons=True)
plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_results.p')[0])
plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')
plot_syn_model(ax5,glob(base_dir+'AMPA&NMDA_soma_data_*'+decided_passive_params+'.p',)[0])

plt.savefig(base_dir+'figure1.pdf')
plt.savefig(base_dir+'figure1.svg')
plt.show()
