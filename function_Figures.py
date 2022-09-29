import pickle
import re
from glob import glob
# from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from read_spine_properties import get_n_spinese
from open_pickle import read_from_pickle
from read_spine_properties import calculate_Rneck
from scalbar_sapir import AnchoredHScaleBar
from pdf2image import convert_from_path
import matplotlib.image as mpimg
fontsize=14
L_widgh=5
text_size=fontsize
legend_size=10
label_size=8
font = {'size' : text_size}

plt.rc('font', size=20)          # controls default text sizes
plt.rc('axes', titlesize=16)     # fontsize of the axes title
plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=legend_size)    # legend fontsize
plt.rc('figure', titlesize=22)  # fontsize of the figure title
#plt.rcParams.update({ "text.usetex": True,"font.family": "Helvetica"})
place=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f"]
# folder_='cells_outputs_data_short/'+cell_name
# folder_='cells_outputs_data_3_initial_cells/'+cell_name
addlw=0
i=0
def show_dirr(png_file):
    if png_file.split('.')[-1]=='pdf':  # if only have pdf (no png) => create png and read it later
        images = convert_from_path(png_file)
        if len(images) == 1:
            images[0].save(png_file.replace(".pdf", ".png"))
        else:  # save per page
            print("Error. too many images")
            return
        # for page_no, image in enumerate(images):
        #     image.save(png_file.replace(".pdf", "_p{0}.png".format(page_no)))
        png_file = png_file.replace(".pdf", ".png")
    # read png
    img = mpimg.imread(png_file)
    imgplot = plt.imshow(img)

def show_directory(ax, title="",png_file=""):
    global i
    if png_file.split('.')[-1]=='pdf':  # if only have pdf (no png) => create png and read it later
        if len(glob(png_file.replace(".pdf", ".png")))>0:
            png_file = png_file.replace(".pdf", ".png")
        else:
            images = convert_from_path(png_file)
            if len(images) == 1:
                images[0].save(png_file.replace(".pdf", ".png"))
            else:  # save per page
                print("Error. too many images")
                return
                # for page_no, image in enumerate(images):
                #     image.save(png_file.replace(".pdf", "_p{0}.png".format(page_no)))
            png_file = png_file.replace(".pdf", ".png")
    # read png
    img = mpimg.imread(png_file)
    if ax is None:
        plt.title(title)
        imgplot = plt.imshow(img)
    else:
        ax.set_title(title)
        ax.axis('off')
        ax.imshow(img)
    i+=1
def find_nearest(array, values):
    indices = np.abs(np.subtract.outer(array, values)).argmin(0)
    return indices
def plot_error(ax,dirr):
    dict3=read_from_pickle(dirr)
    # RA0=dict3['RA']
    # RAs,RMs,CMs,errors=[],[],[],[]
    # errors=dict3['error']['decay&max']
    # error_all=dict3['error']
    errors=[value['error'] for value in dict3]
    RA0=[value['RA'] for value in dict3]
    RMs=[value['RM'] for value in dict3]
    CMs=[value['CM'] for value in dict3]
    RA0=np.take_along_axis(np.array(RA0), np.argsort(RA0,axis=0), axis=0)
    RMs=np.take_along_axis(np.array(RMs), np.argsort(RA0,axis=0), axis=0)
    CMs=np.take_along_axis(np.array(CMs), np.argsort(RA0,axis=0), axis=0)
    errors=np.take_along_axis(np.array(errors), np.argsort(RA0,axis=0), axis=0)

    minimums_arg=np.argsort(errors)
    ax.plot(RA0,errors,'.',lw=8+addlw)
    RA0120= find_nearest(RA0,120)
    RA0150= find_nearest(RA0,150)
    RA_min= minimums_arg[0]
    RA0_best_fit=find_nearest(errors[RA_min:],0.1)+RA_min
    for mini,name in zip([RA0120,RA0150,RA_min,RA0_best_fit],['RA=120', 'RA=150','Ra_min','RA0_best_fit']):
        ax.scatter(RA0[mini], errors[mini], '*',label=name+' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RA0[mini], 2)) + ' CM=' + str(
                     round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)),lw=8+addlw)
    ax.legend(loc='upper left')


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
    RA=0
    if '2017_04_03_B' in file_dirr:
        return 'RA=70'
    for passive_params in ['RA_min_error','RA_best_fit','RA=70','RA=100','RA=120','RA=150','RA=200','RA=300']:
        try_find=glob(file_dirr+'fit RA=*_'+passive_params+'.p')
        if len(try_find)>0:
            RA=float(re.findall(r"[-+]?(?:\d*\.\d+|\d+)", try_find[0].split('/')[-1])[0])
            if RA>50:
                return passive_params
    raise 'Error no passive parameters founded'
def plot_short_pulse_model(ax,dirr,antil_point=-1,show_legend=True,text_place=[0.6,0.9]):
    global  E_PAS,parameters
    dict_result=read_from_pickle(dirr)
    experiment=dict_result['experiment']
    model=dict_result['model']
    fit_decay=dict_result['fit_decay']
    fit_max=dict_result['fit_Rin']
    parameters=dict_result['parameter']
    E_PAS=parameters['E_PAS']
    ax.plot(experiment['T'][:antil_point], experiment['V'][:antil_point]-E_PAS, color = 'black',alpha=0.2,label='experiment',lw=10+addlw*2)
    ax.plot(fit_decay['T'][:antil_point], fit_decay['V'][:antil_point]-E_PAS, color = 'b',alpha=0.3,label='fit decay',lw=6+addlw)
    ax.plot(fit_max['T'][:antil_point], fit_max['V'][:antil_point]-E_PAS,color = 'yellow',alpha=0.8,label='fit maxV',lw=6+addlw)
    ax.plot(model['T'][:len(model['V'])][:antil_point], model['V'][:antil_point]-E_PAS, color = 'red', linestyle ="-",alpha=1,label='Model',lw=3+addlw)
    plt.rcParams.update({'font.size': text_size})
    RM_text="R_m="+str(round(parameters['RM']))+"\u03A9cm^2"
    RA_text="R_a="+str(round(parameters['RA']))+"\u03A9cm"+"\n"
    CM_text="C_m="+str(round(parameters['CM'],1))+"\u03BCf/cm^2"+"\n"
    ax.text(text_place[0],text_place[1],RA_text+CM_text+RM_text,transform=ax.transAxes,size='medium')
    #ax.text(500,-5,"RM="+str(round(parameters['RM']))+" "+'\u03A9cm^2'+"\nRA="+str(round(parameters['RA']))+" \u03A9cm\nCM="+str(roun (parameters['CM'],1))+" \u03BCf/cm^2",size='large')
    if show_legend:
        ax.legend(loc='upper left',prop={'size': legend_size})
    add_scale_bar(ax,'fit_short_pulse',dirr)
    return ax

def plot_syn_model(ax,dirr,start_point=600,show_legend=False):
    dict_syn=read_from_pickle(dirr)
    E_PAS=dict_syn['parameters']['E_PAS']
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('pickles_')+7:])[0])
    T=dict_syn['time']
    V=dict_syn['voltage']
    end_point=int(len(T)*5/6)
    ax.plot(T[start_point:end_point],V['experiment'][start_point:end_point]-E_PAS,color = 'black',alpha=0.2,label='experiment',lw=10+addlw*2)
    ax.plot(T[start_point:end_point],V['Model'][start_point:end_point]-E_PAS,c='red',label='Model',alpha=1,lw=4+addlw)
    ax.plot(T[start_point:end_point],V['V_AMPA'][start_point:end_point]-E_PAS,c='#18852a',linestyle ="--",alpha=1,lw=3+addlw)
    ax.plot(T[start_point:end_point],V['V_NMDA'][start_point:end_point]-E_PAS,c='#03b5fc',linestyle ="--",alpha=1,lw=3+addlw)
    plt.rcParams.update({'font.size': text_size})
    place_text=0.5
    xplace=T[0]
    yplace=V['Model'][0]-E_PAS-0.3
    ax.text(-0.1,-0.02,'g_max AMPA='+str(round(dict_result['mean_final_pop'][0]*1000,2))+' [nS]',c='#18852a',transform=ax.transAxes)#dict_result['parameters'][0]
    ax.text(-0.1,-0.07,'g_max NMDA='+str(round(dict_result['mean_final_pop'][1]*1000,2))+' [nS]',c='#03b5fc',transform=ax.transAxes)#dict_result['parameters'][1]
    if show_legend:
        ax.legend(loc="upper left",prop={'size': legend_size})
    add_scale_bar(ax,'fit_syn')

def plot_syn_model2(ax,dirr,start_point=0,show_legend=True,bbox_to_anchor=(1, 0.35)):
    dict_syn=read_from_pickle(dirr)
    E_PAS=dict_syn[-1]['parameters']['E_PAS']
    dict_result=read_from_pickle(glob(dirr[:dirr.rfind('/')]+'/final_pop'+dirr[dirr.rfind('pickles_')+7:])[0])
    T=dict_syn[0]['time']
    V=dict_syn[1]
    reletive_strengths=dict_syn[-1]['parameters']['reletive_strengths']
    AMPA_weight=round(dict_result['mean_final_pop'][0]*1000,2)
    NMDA_weight=round(dict_result['mean_final_pop'][1]*1000,2)
    for k,color,label in zip(['voltage_all','voltage_0','voltage_1'],['black','#03d7fc','#fc8003'],['model','syn_0','syn1']):
        if k== 'voltage_all':
            label_AMPA='AMPA '+str(AMPA_weight)+' nS'
            label_NMDA='NMDA '+str(NMDA_weight)+' nS'
        else:
            num=int(re.findall(r'\d+', k)[0])
            label_AMPA='AMPA '+str(round(AMPA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+' nS'
            label_NMDA='NMDA '+str(round(NMDA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+' nS'
#            label_AMPA='AMPA '+str(round(AMPA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+' nS '+str(round(reletive_strengths[num]*100))+"%"
#            label_NMDA='NMDA '+str(round(NMDA_weight*reletive_strengths[num]/sum(reletive_strengths),3))+' nS '+str(round(reletive_strengths[num]*100))+"%"

        ax.plot(T[start_point:],V[k]['V_soma_AMPA'][start_point:]-E_PAS,'-',c=color,lw=3+addlw,label=label_AMPA,alpha=0.8)
        ax.plot(T[start_point:],V[k]['V_soma_NMDA'][start_point:]-E_PAS,'--',c=color,lw=3+addlw,label=label_NMDA,alpha=0.8)
        # ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c=color)
        # ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c=color)


    ax.plot(T[start_point:],V['voltage_all']['experiment'][start_point:]-E_PAS,color = 'black',alpha=0.2,label='experiment',lw=12+addlw)
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    # ax.text(200,place_text,dict_result['parameters'][0]+'='+str(round(dict_result['mean_final_pop'][0]*1000,2))+'[nS]',c='#18852a')
    # ax.text(200,place_text-0.2,dict_result['parameters'][1]+'='+str(round(dict_result['mean_final_pop'][1]*1000,2))+'[nS]',c='#03b5fc')
    if show_legend:
        ax.legend(loc="lower center", bbox_to_anchor=bbox_to_anchor,prop={'size': legend_size-2})
    add_scale_bar(ax,'fit_syn')


def get_resistance_par(dirr,parameter):
    found_path=glob(dirr[:dirr.rfind('/')]+'/Rins_pickles*.p')
    if found_path!=1:
        raise "there is more then one option"
    else:
        found_path=found_path[0]
    return read_from_pickle(found_path)['parameters'][parameter]

def get_MOO_result_parameters(cell_name,return_parameter,
                              passive_parameter=None,syn_num=None,relative=None,before_shrink='after',shrinkage_resize=['1.0','1.0'],
                              full_trace=True,from_picture=None,double_spine_area=False):
    if cell_name in ['2017_07_06_C_3-4','2017_02_20_B']: full_trace=False
    df=pd.read_csv('cells_initial_information/'+cell_name+'/results_MOO_Rin_result.csv',index_col=0)
    curr=df
    colombs=[]
    if relative is None:
        relative=get_n_spinese(cell_name)>1
    for v in ['passive_parameter','syn_num','before_shrink','full_trace','relative','from_picture']:
        if not eval(v) is None:
            colombs.append((df[v] == eval(v)).to_numpy().astype(int))
    correct_col = np.mean(colombs, axis=0).astype(int).astype(bool)
    curr_df = df[correct_col]
    return curr_df[return_parameter].to_numpy()

def get_passive_val_name(dirr):
    for p in ['RA_min_error','RA_best_fit','RA=70','RA=100','RA=120','RA=150','RA=200','RA=300']:
        if p in dirr:
            return p
    raise "no passive_val_name in this dirr"


def plot_neck_voltage(ax,dirr,start_point=900,bbox_to_anchor=(0.8, 0.5)):
    dict_syn=read_from_pickle(dirr)
    passive_parameter=get_passive_val_name(dirr)
    cell_name=dirr.split('/')[2]
    RA=dict_syn['parameters']['RA']
    Rin_base=get_MOO_result_parameters(cell_name,'neck_base_Rin',passive_parameter=passive_parameter)
    if len(Rin_base)>get_n_spinese(cell_name): raise "there is too many argue from Rin"
    # Rin_base=get_resistance_par(dirr)
    E_PAS=dict_syn['parameters']['E_PAS']
    T=dict_syn['time']
    V=dict_syn
    size_y_scal_bar=[]
    num=0
    #['#0390fc','#fc6703']
    for k,color,label in zip(['voltage_0','voltage_1'],['#03d7fc','#fc8003'],['syn_0','syn1']):
        Rneck=calculate_Rneck(cell_name,RA,num) #chnage to be in Mega
        antil_point=len(V[k]['V_base_neck'])-1300#int(len(V[k]['V_base_neck'])*2/3)
        T_temp=T[start_point:antil_point]
        ax.plot(T_temp,V[k]['V_base_neck'][start_point:antil_point]-E_PAS,c='black',lw=3+addlw,alpha=0.5,zorder=2)
        ax.plot(T_temp,V[k]['V_head'][start_point:antil_point]-E_PAS,'-',c=color,lw=4+addlw,alpha=0.8,label='Rneck='+str(round(Rneck,2))+' MOhm\n Rin_base='+str(round(Rin_base[num],2)),zorder=1)
        ax.plot(T_temp,V[k]['V_base_neck'][start_point:antil_point]-E_PAS,linestyle='dashdot',alpha=0.8,dashes=[2, 3],c=color,lw=2+addlw,zorder=3)

        size_y_scal_bar.append(int(max(V[k]['V_head'])-E_PAS))
        num+=1
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    ax.legend(loc="lower center", bbox_to_anchor=bbox_to_anchor,prop={'size': legend_size})
    x_to_ms=lambda x: x

    ax.add_artist(AnchoredHScaleBar(size_x=6, size_y=round((max(size_y_scal_bar)-0)/4), frameon=False, ax=ax, x_to_ms=x_to_ms,
                                sep=5, loc="upper right", linekw=dict(color="k", linewidth=2+addlw/2),))
    # start=75
    # ax.set_xlim(left=start,right=start+100)
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
    for k,color,label in zip(['voltage_0','voltage_1'],['#03d7fc','#fc8003'],['syn_0','syn1']):
        ax.plot(T,V[k]-E_PAS,'-',c=color,lw=2+addlw,alpha=0.6)
        size_y_scal_bar.append(int(max(V[k])-E_PAS))
    # place_text=0.5
    plt.rcParams.update({'font.size': text_size})
    ax.legend(loc="upper left",prop={'size': legend_size})
    x_to_ms=lambda x: x

    ax.add_artist(AnchoredHScaleBar(size_x=25, size_y=max(size_y_scal_bar)-2, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                sep=5, loc="upper right", linekw=dict(color="k", linewidth=2+int(np.ceil(addlw/2))),))
    start=75
    ax.set_xlim(left=start,right=start+100)
    ax.set_axis_off()

def plot_pickle(ax,dirr,scale_bar_type=None,remove_begin=True,wigth_factor=1,antil_point=-1):
    plt.rc('font', size=text_size)
    fig1=read_from_pickle(dirr)
    ax_temp=fig1.gca()
    plt.close()
    mean_cal=[]
    for i,line in enumerate(ax_temp.lines):
        x=line.get_data()[0]
        y=line.get_data()[1]
        if len(x)>1 and remove_begin:
            x=x-x[0]
            # y=y-y[0]
        if scale_bar_type=='fit_short_pulse':
            label=str(i)
        else:
            label=line.get_label()
            # if "fit" in dirr

        if len(x)==1:
            ax.scatter(x,y,color=line.get_color(),marker=line.get_marker(),lw=line.get_markersize()-3+addlw,alpha=line.get_alpha(),label=label)
        elif len(x)>1:
            if not scale_bar_type is None:
                if "clear" in scale_bar_type:
                    try:
                        alpha=line.get_alpha()*5/6
                    except:
                        alpha=1
                    ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw()*wigth_factor+int(np.ceil(addlw/2)),alpha=alpha,label=label)
                    mean_cal.append(y)
                else:
                    ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw()*wigth_factor+int(np.ceil(addlw/2)),alpha=line.get_alpha(),label=label)
            else:
                ax.plot(x,y,line.get_linestyle(),color=line.get_color(),lw=line.get_lw()*wigth_factor+int(np.ceil(addlw/2)),alpha=line.get_alpha(),label=label)


    if not scale_bar_type is None:
        if 'syn' in scale_bar_type:
            end_point=1.7
        else:
            end_point=0
        add_scale_bar(ax,scale_bar_type,dirr,end_point=end_point)
        ax.plot(x,np.mean(mean_cal,axis=0),color='black',lw=line.get_lw()*wigth_factor+addlw)
    else:
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1),prop={'size': legend_size-1})
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


    return ax
def add_scale_bar(ax,type='',dirr='',end_point=0):
    start_place=0
    # args = dict(transform=ax.transData)
    if type=='clear_short_pulse':
        x_lim=550/1000
        if '6-7' in dirr:
            x_lim=600/1000
    elif type=="fit_short_pulse":
        x_lim = 550
        if '6-7' in dirr:
            x_lim=600
    elif type=='clear_syn':
        x_lim=0.2
        end_point=1.7
    elif type=='fit_syn':
        x_lim=200
    else:
        x_lim=ax.get_xlim()[1]-ax.get_xlim()[0]
    right=ax.get_xlim()[1]
    ax.set_xlim(left=max(0, right-x_lim),right = right)
    y_units = ax.get_ylim()[1] - ax.get_ylim()[0]
    x_units = ax.get_xlim()[1] - ax.get_xlim()[0]
    is_ms_diff = x_units > 10  # True when we show in sec
    x_txt = 50  # ms
    add_x, add_y = 100,  1  # ms, mv - scalebar size
    add_y=round(y_units/5)
    if type=='fit_syn':
        add_y=round(y_units/5,1)
    j=0
    while add_y==0:
        j+=1
        add_y=round(y_units/5,j)
    if "short_pulse" in type:
        x_txt = 100  # show 50ms for short pulse

    x_to_ms=lambda x: x
    if not is_ms_diff:  # in sec
        add_x /= 1000
        x_to_ms=lambda x: x / 1000
    if "fit_short_pulse" == type:
        print("fit_short_pulse is find")
        if'04_03_B' in dirr:
            loc="lower left" 
        else:
            loc="lower right"      
        ax.add_artist(AnchoredHScaleBar(size_x=x_txt, size_y=add_y, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                        sep=5, loc=loc,linekw=dict(color="k", linewidth=2+int(np.ceil(addlw/2))),))
    elif "fit_syn" == type:
        ax.add_artist(AnchoredHScaleBar(size_x=x_txt, size_y=add_y, frameon=False, ax=ax, x_to_ms=x_to_ms,
                                        sep=5, loc="upper right",linekw=dict(color="k", linewidth=2+int(np.ceil(addlw/2))),))
    ax.set_axis_off()

if __name__=='__main__':
    print(get_MOO_result_parameters('2017_07_06_C_3-4','W_NMDA'))
