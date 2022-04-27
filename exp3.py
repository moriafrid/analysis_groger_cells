from open_MOO_after_fit import OPEN_RES
import numpy as np
# from neuron import h
import matplotlib.pyplot as plt
from glob import glob
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
from tqdm import tqdm
import matplotlib
import pickle
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

folder_= ''
folder_data=folder_+'cells_outputs_data_short/*/MOO_results*/*/F_shrinkage=*/const_param/'
save_name='/g_max'

for model_place in tqdm(glob(folder_data+'*')):
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if type=='test': continue
    loader=None
    try:loader = OPEN_RES(res_pos=model_place+'/')
    except:
       print(model_place + '/hall_of_fame.p is not exsist' )
       continue
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
    model=None
    model=loader.get_model()
    h=loader.sim.neuron.h
    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = 200
    netstim.noise = 0
    secs,segs=get_sec_and_seg(cell_name)
    num=0
    V_spine=[]
    g_spine_NMDA=[]
    spines=[]
    syn_objs=[]

    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num],params=dict_spine_param, number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        V_spine.append(h.Vector())
        V_spine[num].record(spine[1](1)._ref_v)
        g_spine_NMDA.append(h.Vector())
        g_spine_NMDA[num].record(syn_obj[1][0]._ref_g_NMDA)
        num+=1

    # spine, syn_obj = loader.create_synapse(model.dend[82], 0.165, netstim=netstim)
    h.tstop = 500
    time = h.Vector()
    time.record(h._ref_t)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()


    time_all = np.array(time)[1900:]
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
        V_spine_All.append(np.array(V_spine[j])[1900:])
        g_spine_All.append(np.array(g_spine_NMDA[j])[1900:])
        # g_spine_All.append(np.array(g_spine_AMPA[j])[1900:])
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

    # plt.plot(time_all, V_spine_All-V_spine_All[0], color='k', label='all',alpha=0.3)
    # plt.plot(time_all, g_spine_All, color='red', linestyle='--', label='NMDA gmax')
    # plt.plot(time_all, g_spine_All, color='b', linestyle='--', label='AMPA gmax')

