import pickle
import re
from glob import glob
from extra_function import load_swc
from dendogram import Dendogram, add_sec2
from plot_morphology_Yoni import plot_morph
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from create_folder import create_folder_dirr
# cell_name = '2017_05_08_A_4-5'
from read_spine_properties import get_n_spinese
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
    return 'there is no decided passive parameters founded'
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

def plot_syn_model2(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('data_')+4:])[0])
    T=dict_syn[0]['time']
    V=dict_syn[1]
    reletive_strengths=dict_syn[2]['strengths']['relative']
    AMPA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    NMDA_weight=round(dict_result['mean_final_pop'][1]*1000,2)
    for k,color,label in zip(['voltage_all','voltage_0','voltage_1'],['black','#03d7fc','#fcba03'],['model','syn_0','syn1']):
        if k== 'voltage_all':
            label_AMPA='AMPA '+str(AMPA_weight)+'nS'
            label_NMDA='NMDA '+str(NMDA_weight)+'nS'
        else:
            num=int(re.findall(r'\d+', k)[0])

            label_AMPA='AMPA '+str(round(AMPA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+'nS '+str(round(reletive_strengths[num]*100))+"%"
            label_NMDA='NMDA '+str(round(NMDA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+'nS '+str(round(reletive_strengths[num]*100))+"%"

        ax.plot(T,V[k]['V_soma_AMPA']-E_PAS,'-',c=color,lw=2,label=label_AMPA,alpha=0.6)
        ax.plot(T,V[k]['V_soma_NMDA']-E_PAS,'--',c=color,lw=2,label=label_NMDA,alpha=0.6)
        # ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c=color)
        # ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c=color)


    ax.plot(T,V['voltage_all']['experiment']-E_PAS,color = 'black',alpha=0.2,label='experiment',lw=9)
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    # ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c='#18852a')
    # ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c='#03b5fc')
    ax.legend(loc="upper left",prop={'size': label_size})
    add_scale_bar(ax,'fit_syn')
def plot_syn_voltage(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('data_')+4:])[0])
    T=dict_syn['time']
    V=dict_syn
    reletive_strengths=dict_syn['parameters']['reletive_strengths']
    AMPA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    NMDA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    size_y_scal_bar=[]
    for k,color,label in zip(['voltage_0','voltage_1'],['#03d7fc','#fcba03'],['syn_0','syn1']):
        ax.plot(T,V[k]-E_PAS,'-',c=color,lw=2,alpha=0.6)
        size_y_scal_bar.append(int(max(V[k])-E_PAS))
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    plt.legend(loc="upper left",prop={'size': label_size})
    x_to_ms=lambda x: x

    ax.add_artist(AnchoredHScaleBar(size_x=25, size_y=max(size_y_scal_bar)-2, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                sep=5, loc="upper right", linekw=dict(color="k", linewidth=2),))
    start=75
    ax.set_xlim(left=start,right=start+100)
    ax.set_axis_off()
def plot_short_pulse_model(ax,dirr):
    global  E_PAS,parameters
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
    ax.text(500,-5,"RM="+str(round(parameters['RM']))+"\nRA="+str(round(parameters['RA']))+"\nCM="+str(round(parameters['CM'],1)),size='large')
    ax.legend(loc='upper left',prop={'size': label_size})
    add_scale_bar(ax,'fit_short_pulse')
    return ax
def plot_pickle(ax,dirr,scale_bar_type=None,remove_begin=True,wigth_factor=1):
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
    if not scale_bar_type is None:
        add_scale_bar(ax,scale_bar_type)
    return ax
def add_scale_bar(ax,type=''):
    start_place=0
    # args = dict(transform=ax.transData)
    if type=='clear_short_pulse':
        x_lim=550/1000
    elif type=="fit_short_pulse":
        x_lim = 550
    elif type=='clear_syn':
        start_place=50/1000
        x_lim=0.3

    elif type=='fit_syn':
        start_place=50
        x_lim=300

    else:
        x_lim=ax.get_xlim()[1]-ax.get_xlim()[0]

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

if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p')[9:]:
        if '4-3' in cell_name: continue
        before_after='_after_shrink'
        # if cell_name in ['2017_07_06_C_3-4','2016_05_12_A','2016_04_16_A','2017_07_06_C_4-3','2017_05_08_A_5-4']:continue
        # if cell_name!='2017_04_03_B':continue
        base_dir='final_data/'+cell_name+'/'
        save_dir='final_data/Figure1/'
        create_folder_dirr(save_dir)
        print(cell_name)
        fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
        fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
        # fig.set_figwidth(6)
        shapes = (2, 4)
        ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
        ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

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
        if cell_name in ['2017_03_04_A_6-7','2017_05_08_A_5-4']: decided_passive_params='RA_best_fit'
        plot_morph(ax1, cell_name, before_after,without_axons=True)

        if get_n_spinese(cell_name)>1:
            ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2)
            ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
            plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
            plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_results.p')[0])
            plot_syn_model2(ax4,glob(base_dir+'AMPA&NMDA_soma_seperete_data*_relative_'+decided_passive_params+'.p')[0])
            # morph_path=glob("cells_initial_information/"+cell_name+'/*'+before_after+'.swc')[0]
            # dendogram=None
            # dendogram = Dendogram('dend_only', morph_path, add_sec2,load_func=load_swc,E_PAS=E_PAS,passive_val={"RM":parameters['RM'],"RA":parameters['RA'],"CM":parameters['CM']})
            # dendogram.cumpute_distances(dendogram.cell.soma)
            # max_y=dendogram.plot(base_dir,ax=ax4,title='',ylabel="distance from soma (um)")
            # plot_pickle(ax5,glob(base_dir+'Voltage Spine&Soma_full_relative_'+decided_passive_params+'.p')[0])
            plot_syn_voltage(ax5,glob(base_dir+'Voltage Spine&Soma_data*_relative_'+decided_passive_params+'.p')[0])

        else:

            ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2) # , sharex=ax2
            ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1, sharey=ax4) # , sharex=ax4
            plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
            plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_results.p')[0])
            plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')
            plot_syn_model(ax5,glob(base_dir+'AMPA&NMDA_soma_data_*'+decided_passive_params+'.p')[0])

        plt.savefig(save_dir+cell_name+'.svg',dpi=500)
        plt.savefig(save_dir+cell_name+'.pdf',dpi=500)
        # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar
        plt.show()

