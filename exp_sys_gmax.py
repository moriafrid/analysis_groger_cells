from find_MOO_file import MOO_file
from open_MOO_after_fit import OPEN_RES
import numpy as np
# from neuron import h
import matplotlib.pyplot as plt
from glob import glob
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
from tqdm import tqdm
import matplotlib
import pickle
from open_pickle import read_from_pickle
from extraClasses import neuron_start_time
import os

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
import sys
if len(sys.argv) != 4:
    specipic_cell='*'
    before_after='_after_shrink'
    specipic_moo='_correct_seg*'
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
save_name='/g_max'
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
    if type=='test': continue
    loader=None
    model=None
    try:loader = OPEN_RES(res_pos=model_place+'/', curr_i=curr_i)
    except:
       print(model_place + '/hall_of_fame.p is not exsist' )
       continue
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
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
    total_duration= neuron_start_time+500
    # V_base=V_base+E_PAS


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
    g_spine_NMDA=[]
    spines=[]
    syn_objs=[]

    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num], number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        V_spine.append(h.Vector())
        V_spine[num].record(spine[1](1)._ref_v)
        g_spine_NMDA.append(h.Vector())
        g_spine_NMDA[num].record(syn_obj[1][0]._ref_g_NMDA)
        num+=1

    # spine, syn_obj = loader.create_synapse(model.dend[82], 0.165, netstim=netstim)
    time = h.Vector()
    time.record(h._ref_t)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()

    cut_from_start_time=int(neuron_start_time/0.1)

    time_all = np.array(time)[cut_from_start_time:]
    names=["A","B"]
    fig = plt.figure()
    if get_n_spinese(cell_name) == 2:
        axs = fig.subplot_mosaic("""AB""")
    else:
        axs = fig.subplot_mosaic("""A""")
    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    fig.suptitle('NMDA g\n '+" ".join([model_place.split('/')[1],model_place.split('/')[-1],'\n'+passive_propert_title]))
    V_spine_All,g_spine_All=[],[]
    for j in range(len(V_spine)):
        V_spine_All.append(np.array(V_spine[j])[cut_from_start_time:])
        g_spine_All.append(np.array(g_spine_NMDA[j])[cut_from_start_time:])
        # g_spine_All.append(np.array(g_spine_AMPA[j])[cut_from_start_time:])
        axs[names[j]].set_title('spine'+str(j)+" "+secs[j]+" "+str(segs[j]))
        axs[names[j]].plot(time_all, g_spine_All[j], color='red', linestyle='--', label='NMDA g')
        g_max=np.argmax(g_spine_All[j])
        axs[names[j]].plot(time_all[g_max], g_spine_All[j][g_max], '*',color='black', label='NMDA g_max='+str(round(g_spine_All[j][g_max],2)),markersize=10)

        axs[names[j]].set_xlabel('time [s]')
        axs[names[j]].set_ylabel('leakness [Simans]')
        axs[names[j]].legend()
    plt.legend()
    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))

    # plt.show()
    plt.close()
    loader.destroy()
    model.destroy()
    # plt.plot(time_all, V_spine_All-V_spine_All[0], color='k', label='all',alpha=0.3)
    # plt.plot(time_all, g_spine_All, color='red', linestyle='--', label='NMDA gmax')
    # plt.plot(time_all, g_spine_All, color='b', linestyle='--', label='AMPA gmax')
os.system("sbatch execute_python_script.sh "+ "csv_for_MOO_results_final.py")

if specipic_cell=='*':
    specipic_cell="None"
if run_reorgenize:
    os.system('python reorgenize_results.py '+ '_'+specipic_cell+' '+before_after+' '+specipic_moo)

