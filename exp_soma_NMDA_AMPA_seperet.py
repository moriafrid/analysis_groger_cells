import os

from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
from glob import glob
from tqdm import tqdm
import pickle
import matplotlib
from open_pickle import read_from_pickle
from extraClasses import neuron_start_time
from add_figure import add_figure

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
import sys
if len(sys.argv) != 4:
    specipic_cell='*'
    before_after='_after_shrink'
    specipic_moo='_correct_seg'
    print("sys.argv isn't run")
else:
    print("the sys.argv len is correct",flush=True)
    specipic_cell = sys.argv[1]
    if type(specipic_cell)!=str:
        specipic_cell='*'
    before_after=sys.argv[2]
    specipic_moo= sys.argv[3]
    if type(specipic_moo)!=str:
        specipic_moo='*'

    print('run with sys.argv', sys.argv)

folder_= ''
folder_data1=folder_+'cells_outputs_data_short/'+specipic_cell+'/MOO_results_same_strange'+before_after+specipic_moo+'/*/F_shrinkage=*/const_param/'
folder_data2=folder_+'cells_outputs_data_short/'+specipic_cell+'/MOO_results_relative_strange'+before_after+specipic_moo+'/*/F_shrinkage=*/const_param/'
save_name='/AMPA&NMDA_soma_seperete'
color=['#03d7fc','#fcba03']
def simulate_syn(sec,seg,num=None,color='black'):
    global time_all
    if num is None:
        V_spine,spines,syn_objs=[],[],[]
        for sec_t,seg_t,i in zip(sec,seg,range(get_n_spinese(cell_name))):
            spine, syn_obj = loader.create_synapse(eval('model.'+sec_t), seg_t,reletive_strengths[i], number=i,netstim=netstim)
            spines.append(spine)
            syn_objs.append(syn_obj)
    else:
        spines, syn_objs = loader.create_synapse(eval('model.'+sec),seg,reletive_strengths[num], number=num,netstim=netstim)
    time = h.Vector()
    time.record(h._ref_t)
    V_soma = h.Vector()
    V_soma.record(model.soma[0](0.5)._ref_v)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()
    cut_from_start_time=int(neuron_start_time/0.1)
    V_soma_All = np.array(V_soma)[cut_from_start_time:]
    time_all = np.array(time)[cut_from_start_time:]
    time_all-=time_all[0]
    # take syn_obj to be 0 to see the NMDA
    if num is None:
        for j in range(get_n_spinese(cell_name)):
            syn_objs[j][1][1].weight[0]=0
    else:
        syn_objs[1][1].weight[0]=0

    h.steps_per_ms = 1.0/h.dt
    h.run()
    V_soma_AMPA = np.array(V_soma)[cut_from_start_time:]
    V_NMDA = V_soma_All-V_soma_AMPA

    # plt.plot(time_all, V_soma_All, color='g', lw=5,label='all',alpha=0.4)
    if not num is None:
        plt.plot(time_all, V_soma_AMPA, color=color, lw=2,linestyle='-', label='AMPA '+str(round(loader.get_param('weight_AMPA')*1000*reletive_strengths[num]/sum(reletive_strengths),3))+'nS '+str(round(reletive_strengths[num]*100))+"%",alpha=0.6)
        plt.plot(time_all, V_NMDA+V_soma_All[0],lw=2, color=color, linestyle='--', label='NMDA '+str(round(loader.get_param('weight_NMDA')*1000*reletive_strengths[num]/sum(reletive_strengths),3))+'nS '+str(round(reletive_strengths[num]*100))+"%",alpha=0.6)
    else:
        plt.plot(time_all, V_soma_AMPA, color=color, lw=2,linestyle='-', label='AMPA '+str(round(loader.get_param('weight_AMPA')*1000,3))+'nS',alpha=0.6)
        plt.plot(time_all, V_NMDA+V_soma_All[0],lw=2, color=color, linestyle='--', label='NMDA '+str(round(loader.get_param('weight_NMDA')*1000,3))+'nS',alpha=0.6)
    return {'V_soma_AMPA':V_soma_AMPA,'V_soma_NMDA':V_NMDA+V_soma_All[0]}

for curr_i, model_place in tqdm(enumerate(glob(folder_data2+'*')+glob(folder_data1+'*'))):
    print(model_place)
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if get_n_spinese(cell_name)<2:continue
    if type=='test': continue
    if "same" in model_place: continue
    try:loader = OPEN_RES(res_pos=model_place+'/', curr_i=curr_i)
    except Exception as e:
        print(e)
        print(model_place + '/hall_of_fame.p is not exsist' )
        continue
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
        relative='relative'
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
        relative='same'
    model=None
    model=loader.get_model()
    RDSM_objective_file = folder_+'cells_initial_information/'+cell_name+"/mean_syn.p"
    V_data,T_data=read_from_pickle(RDSM_objective_file)
    T_with_units=T_data-T_data[0]
    T_with_units=T_with_units*1000
    T_base = np.array(T_with_units)
    V_base = np.array(V_data)
    # T_with_units=T_data.rescale('ms')
    # spike_timeing=T_base[np.argmax(np.array(V_base))-65]
    spike_timeing=T_base[read_from_pickle('syn_onset.p')[cell_name]]
    total_duration=T_base[-1] + neuron_start_time
    # V_base=V_base+E_PAS

    h=loader.sim.neuron.h
    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = spike_timeing + neuron_start_time
    netstim.noise = 0
    h.tstop = total_duration

    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    fig=add_figure(cell_name+' AMPA and NMDA '+relative+" strength"+'\n'+model_place.split('/')[-1]+" "+passive_propert_title,'time[ms]','Voltage[mV]')
    plt.text(0,V_base[0]+2,reletive_strengths)
    secs,segs=get_sec_and_seg(cell_name)
    dict_result={}
    for num in range(get_n_spinese(cell_name)):
        dict_result['voltage_'+str(num)]=simulate_syn(secs[num],segs[num],num=num,color=color[num])
    dict_result['voltage_all']=simulate_syn(secs,segs,color='black')
    plt.plot(T_base, np.array(V_base)+loader.get_param('e_pas'), color='black',label='EP record',alpha=0.2,lw=5)
    dict_result['voltage_all']['experiment']=np.array(V_base)+loader.get_param('e_pas')
    plt.legend()
    print("Save ", model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))
    dict_result['parameters']={'reletive_strengths':reletive_strengths,'PSD':psd_sizes,'RA':loader.get_param('Ra'),'RM':1.0/loader.get_param('g_pas'),'CM':loader.get_param('cm'),'E_PAS':loader.get_param('e_pas')}
    pickle.dump([{'time':time_all},dict_result], open(model_place+save_name+'_pickles.p', 'wb'))
    # plt.show()
    plt.close()
    loader.destroy()
    # model.destroy()
os.system('python reorgenize_results.py')
