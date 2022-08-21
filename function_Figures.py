import pickle
import re
from glob import glob
# from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from read_spine_properties import calculate_Rneck
from scalbar_sapir import AnchoredHScaleBar

fontsize=16
L_widgh=5
text_size=15
label_size=8

plt.rc('font', size=20)          # controls default text sizes
plt.rc('axes', titlesize=16)     # fontsize of the axes title
plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
plt.rc('ytick', labelsize=10)    # fontsize of the tick labels
plt.rc('legend', fontsize=16)    # legend fontsize
plt.rc('figure', titlesize=22)  # fontsize of the figure title
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
    E_PAS=dict_syn['parameters']['E_PAS']
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('pickles_')+7:])[0])
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
    ax.legend(loc="upper left",prop={'size': label_size})
    add_scale_bar(ax,'fit_syn')

def plot_syn_model2(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    E_PAS=dict_syn[-1]['parameters']['E_PAS']
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('pickles_')+7:])[0])
    T=dict_syn[0]['time']
    V=dict_syn[1]
    reletive_strengths=dict_syn[-1]['parameters']['reletive_strengths']
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
def plot_neck_voltage(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    cell_name=dirr.split('/')[1]
    RA=dict_syn['parameters']['RA']
    E_PAS=dict_syn['parameters']['E_PAS']
    T=dict_syn['time']
    V=dict_syn
    size_y_scal_bar=[]
    num=0
    #['#0390fc','#fc6703']
    for k,color,label in zip(['voltage_0','voltage_1'],['#03d7fc','#fcba03'],['syn_0','syn1']):
        Rneck=calculate_Rneck(cell_name,RA,num) #chnage to be in Mega
        antil_point=int(len(V[k]['V_base_neck'])*2/3)
        T=T[:antil_point]
        ax.plot(T,V[k]['V_base_neck'][:antil_point]-E_PAS,c='black',lw=2,alpha=0.5)
        ax.plot(T,V[k]['V_head'][:antil_point]-E_PAS,'-',c=color,lw=2,alpha=0.6,label=str(round(Rneck,2))+'MOhm')
        ax.plot(T,V[k]['V_base_neck'][:antil_point]-E_PAS,linestyle='dashdot',alpha=0.5,dashes=[3, 2],c=color,lw=2)

        size_y_scal_bar.append(int(max(V[k]['V_head'])-E_PAS))
        num+=1
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    ax.legend(loc="upper left",prop={'size': label_size})
    x_to_ms=lambda x: x

    ax.add_artist(AnchoredHScaleBar(size_x=25, size_y=max(size_y_scal_bar)-2, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                sep=5, loc="upper right", linekw=dict(color="k", linewidth=2),))
    start=75
    ax.set_xlim(left=start,right=start+100)
    ax.set_axis_off()
def plot_syn_voltage(ax,dirr):
    dict_syn=read_from_pickle(dirr)
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('pickles_')+7:])[0])
    T=dict_syn['time']
    V=dict_syn
    E_PAS=dict_syn['parameters']['E_PAS']
    reletive_strengths=dict_syn['parameters']['reletive_strengths']
    AMPA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    NMDA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    size_y_scal_bar=[]
    for k,color,label in zip(['voltage_0','voltage_1'],['#03d7fc','#fcba03'],['syn_0','syn1']):
        ax.plot(T,V[k]-E_PAS,'-',c=color,lw=2,alpha=0.6)
        size_y_scal_bar.append(int(max(V[k])-E_PAS))
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    ax.legend(loc="upper left",prop={'size': label_size})
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
