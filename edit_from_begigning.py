import pickle
from glob import glob
from plot_morphology_Yoni import plot_morph
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from create_folder import create_folder_dirr
# cell_name = '2017_05_08_A_4-5'
from scalbar_sapir import AnchoredHScaleBar
import math

L_widgh=5
text_size=15
label_size=8
def clear_short_pulse(ax, dir):
    # d = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_05_08_A_4-5/clear_short_pulse.p'
    data = pickle.load(open(dir, 'rb'))
    T = data[1]-data[1][0] # in sec
    T = T.rescale('ms')
    for v in data[0]:
        ax.plot(T, v, color='grey',alpha=0.2,lw=0.1)
    ax.plot(T, data[0].mean(axis=0), color='k')
    return ax

def clear_syn_mean(ax, dir):
    # d = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_05_08_A_4-5/clear_short_pulse.p'
    data = pickle.load(open(dir, 'rb'))
    T = data[1]-data[1][0] # in sec
    T = T.rescale('ms')
    for v in data[0]:
        ax.plot(T, v, color='grey',alpha=0.2,lw=0.1)
    ax.plot(T, data[0].mean(axis=0), color='k')
    return ax
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
    ax.plot(T,V['experiment']-E_PAS,color = 'black',alpha=0.2,label='experiment',lw=9)
    ax.plot(T,V['Model']-E_PAS,c='red',label='Model',alpha=0.5,lw=4)
    ax.plot(T,V['V_AMPA']-E_PAS,c='#18852a',linestyle ="--",alpha=1)
    ax.plot(T,V['V_NMDA']-E_PAS,c='#03b5fc',linestyle ="--",alpha=1)
    place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c='#18852a')
    ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c='#03b5fc')
    plt.legend(loc="upper left",prop={'size': label_size})
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
    ax.plot(experiment['T'], experiment['V']-E_PAS, color = 'black',alpha=0.2,label='experiment',lw=9)
    ax.plot(fit_decay['T'], fit_decay['V']-E_PAS, color = 'b',alpha=0.3,label='fit decay',lw=4)
    ax.plot(fit_max['T'], fit_max['V']-E_PAS,color = 'yellow',alpha=0.8,label='fit maxV',lw=4)
    ax.plot(model['T'][:len(model['V'])], model['V']-E_PAS, color = 'red', linestyle ="-",alpha=0.5,label='Model',lw=4)
    plt.rcParams.update({'font.size': text_size})
    ax.text(500,-2,"RM="+str(round(parameters['RM']))+"\nRA="+str(round(parameters['RA']))+"\nCM="+str(round(parameters['CM'],1)),size='large')
    ax.legend(loc='lower right',prop={'size': label_size})
    add_scale_bar(ax,'fit_short_pulse')

    return ax

def plot_pickle(ax,dirr,scale_bar_type,remove_begin=True,wigth_factor=1):
    # plt.rc('font', size=text_size)
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

        ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw()*wigth_factor,alpha=line.get_alpha(),label=label)
        if len(x)==1:
            ax.scatter(x,y,color=line.get_color(),s=line.get_markersize(),alpha=line.get_alpha(),label=label)
    add_scale_bar(ax,scale_bar_type)
    return ax

def add_scale_bar(ax,type):
    # args = dict(transform=ax.transData)
    if type=='clear_short_pulse':
        x_lim=550/1000
    elif type=="fit_short_pulse":
        x_lim = 550
    elif type=='clear_syn':
        x_lim=0.3
    elif type=='fit_syn':
        x_lim=300

    right=ax.get_xlim()[1]
    ax.set_xlim(left=max(0, right-x_lim),right = right)
    y_units = ax.get_ylim()[1] - ax.get_ylim()[0]
    x_units = ax.get_xlim()[1] - ax.get_xlim()[0]
    is_ms_diff = x_units > 10  # True when we show in sec
    x_txt = 100  # ms
    add_x, add_y = 100,  1  # ms, mv - scalebar size
    add_y=round(y_units/5)
    j=0
    while add_y==0:
        j+=1
        add_y=round(y_units/5,j)
    if "short_pulse" in type:
        x_txt = 50  # show 50ms for short pulse

    x_to_ms=lambda x: x
    if not is_ms_diff:  # in sec
        add_x /= 1000
        x_to_ms=lambda x: x / 1000
    if "fit" in type:
        ax.add_artist(AnchoredHScaleBar(size_x=x_txt, size_y=add_y, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                        sep=5, loc="upper right", linekw=dict(color="k", linewidth=2),))
    ax.set_axis_off()

def add_scale_bar_test(ax,type):
    x_lim = 0
    if type=='clear_short_pulse':
        x_lim=550/1000
    elif type=="fit_short_pulse":
        x_lim = 550
    elif type=='clear_syn':
        x_lim=0.3
    elif type=='fit_syn':
        x_lim=300

    # left=ax.get_xlim()[0]
    right=ax.get_xlim()[1]
    # bottom=ax.get_ylim()[0]
    ax.set_xlim(left=max(0, right-x_lim),right = right)
    # ax.set_ylim(bottom=bottom, top =bottom+y_lim)

    args = dict(transform=ax.transData)
    # plt.rcParams.update({'font.size': text_size})
    y_units = ax.get_ylim()[1] - ax.get_ylim()[0]
    x_units = ax.get_xlim()[1] - ax.get_xlim()[0]
    is_sub_mv_diff = y_units < 3  # todo magic number - True when we show 0.1mV
    print(type,'mv:',y_units)
    is_ms_diff = x_units > 10  # True when we show in sec
    # print(type, " is ms? ", is_ms_diff, " is 0.1mV ", is_sub_mv_diff)
    base_x, base_y = ax.get_xlim()[0], -4.0
    sft_txt_x, sft_txt_y = 50, 1  # ms mV
    x_txt = 100  # ms
    add_x, add_y = 100,  1  # ms, mv - scalebar size
    add_y=math.ceil(y_units/4)
    # if add_y==0:
    #     add_y=round(y_units/4,1)
    x_to_ms=lambda x: x
    if is_sub_mv_diff:
        sft_txt_x = 20  # ms
        x_txt = 50  # show 50ms for short pulse
        add_x = 50
        base_y /= 10
        add_y /= 10
        sft_txt_y /= 10
        # scale_mV_lw /= 10
    if not is_ms_diff:  # in sec
        add_x /= 1000
        sft_txt_x /= 1000
        x_to_ms=lambda x: x / 1000
    # ax.plot([base_x, base_x], [base_y, base_y + add_y], color='k', lw=L_widgh, **args)  # ms
    # ax.plot([base_x, base_x + add_x], [base_y, base_y], color='k', lw=L_widgh * scale_mV_lw, **args)  # mV
    # ax.text(base_x - sft_txt_x, base_y - sft_txt_y, f'{add_y} mV', rotation=90, **args)  # mV
    # ax.text(base_x - sft_txt_x, base_y - sft_txt_y, f'{x_txt} ms', **args)  # ms
    ax.add_artist(AnchoredHScaleBar(size_x=x_txt, size_y=add_y, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                    sep=5, loc="upper right", linekw=dict(color="k", linewidth=2),))

    if type=='clear_short_pulse':
        base_y=-4
        base_x=100/1000
        # ax.plot([base_x,base_x], [base_y, base_y+1], color='k',lw=L_widgh)
        # ax.plot([base_x,base_x+100/1000],[base_y, base_y], color='k',lw=L_widgh)
        # ax.text(base_x-50/1000, base_y+0.1, '1 mV', rotation=90)
        # ax.text(base_x+10/1000, base_y-0.5, '100 ms')
        x_lim=550/1000
        y_lim=7
        if cell_name=='2017_03_04_A_6-7':
            x_lim=700/1000

        if cell_name=='2017_02_20_B':
            y_lim=10
    elif type=="fit_short_pulse":
        base_y=-4#E_PAS#-4
        base_x=100
        # ax.plot([base_x,base_x], [base_y, base_y+1], color='k',lw=L_widgh)
        # ax.plot([base_x,base_x+100],[base_y, base_y], color='k',lw=L_widgh)
        # ax.text(base_x-40, base_y+0.1, '1 mV', rotation=90)
        # ax.text(base_x, base_y-0.4, '100 ms')
        x_lim=550
        y_lim=7
        if cell_name=='2017_03_04_A_6-7':
            x_lim=700
        if cell_name=='2017_02_20_B':
            y_lim=10
        # plt.rcParams.update({'font.size': text_size})

    elif type=='clear_syn':
        base_y=1.5
        base_x=180/1000
        # ax.plot([base_x,base_x], [base_y, base_y+0.5], color='k',lw=L_widgh)
        # ax.plot([base_x,base_x+50/1000],[base_y, base_y], color='k',lw=L_widgh)
        # ax.text(base_x-20/1000, base_y, '0.5 mV', rotation=90)
        # ax.text(base_x+10/1000, base_y-0.2, '50 ms')
        x_lim=0.3
        y_lim=3.1
        if cell_name=='2017_03_04_A_6-7':
            y_lim=6.5

    elif type=='fit_syn':
        base_y=1.0
        base_x=200
        # ax.plot([base_x,base_x], [base_y, base_y+0.6], color='k',lw=L_widgh)
        # ax.plot([base_x,base_x+50],[base_y, base_y], color='k',lw=L_widgh)
        # ax.text(base_x-20, base_y+0.1, '0.5 mV', rotation=90)
        # ax.text(base_x+5, base_y-0.2, '50 ms')
        x_lim=300
        y_lim=3.1
        if cell_name=='2017_03_04_A_6-7':
            y_lim=6.5
    elif type=='neuron':
        # ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower left",rotation="horizontal"))
        base_y=1.0
        base_x=200
        # ax.plot([base_x,base_x], [base_y, base_y+0.6], color='k',lw=L_widgh)
        # ax.plot([base_x,base_x+50],[base_y, base_y], color='k',lw=L_widgh)
        # ax.text(base_x-20, base_y+0.1, '0.5 mV', rotation=90)
        # ax.text(base_x+5, base_y-0.2, '50 ms')

    if cell_name=='2016_04_16_A':
        y_lim+=2

    # ax.set_ylim([-4, 4])
    ax.set_axis_off()


# cell_name = read_from_pickle('cells_name2.p')
if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p'):
        before_after='_before_shrink'
        base_dir='final_data'+before_after+'/'+cell_name+'/'
        save_dir='final_data'+before_after+'/Figure1/'
        create_folder_dirr(save_dir)
        print(cell_name)
        fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
        fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
        # fig.set_figwidth(6)
        shapes = (2, 4)
        ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
        ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2) # , sharex=ax2
        ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
        ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1, sharey=ax4) # , sharex=ax4
        # plt.subplots_adjust(hspace=0.3, wspace=0.3)
        fontsize=16
        plt.rc('font', size=20)          # controls default text sizes
        plt.rc('axes', titlesize=16)     # fontsize of the axes title
        plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=10)    # fontsize of the tick labels
        plt.rc('legend', fontsize=16)    # legend fontsize
        plt.rc('figure', titlesize=22)  # fontsize of the figure title

        decided_passive_params=find_RA(base_dir)
        plot_morph(ax1, cell_name, before_after,without_axons=True)
        plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_results.p')[0])
        # plot_pickle(ax3,glob(base_dir+'fit RA=*'+decided_passive_params+'.p')[0],'fit_short_pulse',wigth_factor=2,remove_begin=False)
        # plt.rcParams.update({'font.size': text_size})

        plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
        plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')
        plot_syn_model(ax5,glob(base_dir+'AMPA&NMDA_soma_data_*'+decided_passive_params+'.p')[0])

        plt.savefig(save_dir+cell_name+'.svg',dpi=500)
        plt.savefig(save_dir+cell_name+'.pdf',dpi=500)
        # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar
        plt.show()

