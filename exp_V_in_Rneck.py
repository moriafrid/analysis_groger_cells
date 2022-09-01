import os

from find_MOO_file import MOO_file
from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from glob import glob
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
from tqdm import tqdm
import pickle
import matplotlib
from open_pickle import read_from_pickle
from extraClasses import neuron_start_time
import sys
from find_MOO_file import MOO_file
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
print(sys.argv)
if len(sys.argv) != 4:
    specipic_cell='*'
    before_after='_before_shrink'
    specipic_moo='_correct_seg'
    run_reorgenize=False
    print("sys.argv isn't run")
else:
    print("the sys.argv len is correct",flush=True)
    specipic_cell = sys.argv[1]
    if specipic_cell=='None':
        specipic_cell='*'
    before_after=sys.argv[2]
    specipic_moo= sys.argv[3]
    if specipic_moo=='None':
        specipic_moo='*'
        run_reorgenize=False
    else:
        run_reorgenize=True

folder_= ''
# folder_data1=folder_+'cells_outputs_data_short/'+specipic_cell+'/MOO_results_same_strange'+before_after+specipic_moo+'/*/F_shrinkage=*/const_param/'
# folder_data2=folder_+'cells_outputs_data_short/'+specipic_cell+'/MOO_results_relative_strange'+before_after+specipic_moo+'/*/F_shrinkage=*/const_param/'
save_name='/Voltage in neck'
folders=[]
for moo_file in MOO_file(before_after=before_after):
    folders+=glob(folder_+'cells_outputs_data_short/'+specipic_cell+'/'+moo_file+'/F_shrinkage=*/const_param/*/')

for curr_i, model_place in tqdm(enumerate(folders)):
    if 'syn_xyz' in model_place:
        sec_from_picture=False
    else:
        sec_from_picture=True
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    # if get_n_spinese(cell_name)==2:continue
    if type=='test': continue
    try:loader = OPEN_RES(res_pos=model_place+'/', curr_i=curr_i)
    except:
        print(model_place + '/hall_of_fame.p is not exsist' )
        continue
    psd_sizes=get_parameter(cell_name,'PSD')
    if 'relative' in model_place:
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
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
    model=None
    model=loader.get_model()

    h=loader.sim.neuron.h
    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = spike_timeing + neuron_start_time
    netstim.noise = 0
    h.tstop = total_duration

    secs,segs=get_sec_and_seg(cell_name,from_picture=sec_from_picture)
    num=0
    V_spine=[]
    V_base_neck=[]
    spines=[]
    syn_objs=[]
    imps_base=[]
    imps_spine_head=[]
    imp_soma=h.Impedance(sec=model.soma[0])
    imp_soma.loc(0.5)
    distance=[]
    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(loader.get_sec(sec), seg,reletive_strengths[num], number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        V_spine.append(h.Vector())
        V_spine[num].record(spine[1](1)._ref_v) #thh spine head
        V_base_neck.append(h.Vector())
        V_base_neck[num].record(loader.get_sec(sec)(seg)._ref_v) #the neck base

        imps_base.append(h.Impedance(sec=loader.get_sec(sec)))
        imps_base[num].loc(seg) #spine base = on dend segment

        imps_spine_head.append(h.Impedance(sec=spine[1]))
        imps_spine_head[num].loc(1) #spine_head

        distance.append(h.distance(model.soma[0](0.5),loader.get_sec(sec)(seg)))
        num+=1

    time = h.Vector()
    time.record(h._ref_t)
    V_soma = h.Vector()
    V_soma.record(model.soma[0](0.5)._ref_v)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt

    h.run()
    Rin_soma=imp_soma.input(0)
    Rin_base,Rtrans_base=[],[]
    for imp in imps_base:
        imp.compute(0)
        Rin_base.append(imp.input(0))
        Rtrans_base.append(imp.transfer(model.soma[0](0.5)))

    Rin_head,Rtrans_head=[],[]
    for imp in imps_spine_head:
        imp.compute(0)
        Rin_head.append(imp.input(0))
        Rtrans_head.append(imp.transfer(model.soma[0](0.5)))
    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    cut_from_start_time=int(neuron_start_time/0.1)

    V_soma=np.array(V_soma)[cut_from_start_time:]
    time=np.array(time)[cut_from_start_time:]-time[cut_from_start_time]
    names=["A","B"]

    fig = plt.figure(figsize=(10,10))

    if get_n_spinese(cell_name) == 2:
       axs = fig.subplot_mosaic("""AB""")
    else:
       axs = fig.subplot_mosaic("""A""")

    fig.suptitle('Voltage in Spine base\n '+" ".join([model_place.split('/')[1],model_place.split('/')[-1] ,'\n',model_place.split('/')[4],model_place.split('/')[2]])+'\n'+passive_propert_title)
    dicty={}
    dicty['time']=time
    parameters_dict={'reletive_strengths':reletive_strengths,'PSD':psd_sizes,'RA':loader.get_param('Ra'),'RM':1.0/loader.get_param('g_pas'),'CM':loader.get_param('cm'),'E_PAS':loader.get_param('e_pas')}
    dicty['parameters']=parameters_dict
    for j in range(len(V_spine)):
        V_spine[j]=np.array(V_spine[j])[cut_from_start_time:]
        V_base_neck[j]=np.array(V_base_neck[j])[cut_from_start_time:]
        axs[names[j]].set_title('spine'+str(j)+" "+secs[j]+" "+str(segs[j]))
        # axs[names[j]].plot(time, V_soma,'green',label='V_soma higth:'+str(round(np.amax(V_soma)-np.amin(V_soma),2))+'mV')
        axs[names[j]].plot(time, V_spine[j],'orange',label='V_spine'+str(j)+ ' higth:'+str(round(np.amax(V_spine[j])-np.amin(V_spine[j]),2))+'mV')
        axs[names[j]].plot(time, V_base_neck[j],'green',label='V_base_neck'+str(j)+ ' higth:'+str(round(np.amax(V_base_neck[j])-np.amin(V_base_neck[j]),2))+'mV')
        axs[names[j]].set_xlabel('time [ms]')
        axs[names[j]].set_ylabel('voltage [mv]')
        axs[names[j]].legend()
        axs[names[j]].plot(np.array(T_base), np.array(V_base)+loader.get_param('e_pas'), color='black',label='EP record',alpha=0.2,lw=5)
        dicty['voltage_'+str(j)]={'V_head':V_spine[j],'V_base_neck':V_base_neck[j]}

    pickle.dump(dicty, open(model_place+save_name+'_pickles.p', 'wb'))
    parameters_dict['distance']=distance
    parameters_dict['W_AMPA']=loader.get_param('weight_AMPA')
    parameters_dict['W_NMDA']=loader.get_param('weight_NMDA')
    parameters_dict['tau1_AMPA']=loader.get_param('exp2syn_tau1')
    parameters_dict['tau2_AMPA']=loader.get_param('exp2syn_tau2')

    parameters_dict['tau1_NMDA']=loader.get_param('NMDA_tau_r_NMDA')
    parameters_dict['tau2_NMDA']=loader.get_param('NMDA_tau_d_NMDA')

    pickle.dump({'soma':{'Rin':Rin_soma},'neck_base':{'Rin':Rin_base,'Rtrans':Rtrans_base},'spine_head':{'Rin':Rin_head,'Rtrans':Rtrans_head},'parameters':parameters_dict}, open(model_place+'/Rins_pickles.p', 'wb'))

    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))
    # plt.show()
    plt.close()

    loader.destroy()
    model.destroy()
if specipic_cell=='*':
    specipic_cell="None"
if run_reorgenize:
    os.system('python reorgenize_results.py '+ '_'+specipic_cell+' '+before_after+' '+specipic_moo)




