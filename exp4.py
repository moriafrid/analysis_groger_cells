from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
from extra_function import create_folder_dirr
import matplotlib
import pickle
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
import sys

folder_= ''
folder_data=folder_+'cells_outputs_data_short/*4-5/MOO_results_*/*/F_shrinkage=*/const_param'
# folder_save=folder_data+'/MOO_results/hall_of_fame_together/'
def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
cmap = get_cmap(10)
for model_place in glob(folder_data+'*'):
    type=model_place.split('/')[-1]
    if type=='test': continue
    folder_save=model_place+'/hall_of_fame_together/'
    create_folder_dirr(folder_save)
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
    names=["A","B"]

    figure, axis = plt.subplots(1, get_n_spinese(cell_name))
    plt.title('AMPA and NMDA impact on voltage ')
    if get_n_spinese(cell_name) == 1:
        axis = axis[..., np.newaxis]

    if get_n_spinese(cell_name) == 2:
        figure = plt.figure(figsize=(10,10))
        axis = figure.subplot_mosaic("""AB""")
    else:
        axs = figure.subplot_mosaic("""A""")
    # add_figure('AMPA and NMDA impact on voltage ' + type,'mV', 'mS')
    for i in tqdm(range(10)):
        loader = OPEN_RES(res_pos=model_place + '/')
        model=loader.get_model()
        netstim = h.NetStim()  # the location of the NetStim does not matter
        netstim.number = 1
        netstim.start = 200
        netstim.noise = 0
        h.tstop = 300
        time = h.Vector()
        time.record(h._ref_t)
        secs,segs=get_sec_and_seg(cell_name)
        num=0
        V_spine=[]
        spines=[]
        syn_objs=[]

        for sec,seg in zip(secs,segs):
            dict_spine_param=get_building_spine(cell_name,num)
            spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num],params=dict_spine_param, number=num,netstim=netstim, hall_of_fame_num=i)
            spines.append(spine)
            syn_objs.append(syn_obj)
            V_spine.append(h.Vector())
            V_spine[num].record(spine[1](1)._ref_v)
            num+=1
            print(num)
        h.dt = 0.1
        h.steps_per_ms = 1.0 / h.dt
        h.run()


        time=np.array(time)#[1900:]
        alphas=[0.8,0.3]
        for j in range(len(V_spine)):
            print(j)
            V_spine[j]=np.array(V_spine[j])#[1900:]
            axs[names[j]].plot(time,V_spine[j],label='hall_'+str(i),c=cmap(i))
            # axis[0,i].set_title("spine voltage")
            axs[names[j]].set_xlabel('ms')
            axs[names[j]].set_ylabel('mv')

        # plt.plot(time, V_spine, label='hall_'+str(i),alpha=0.1)
    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    plt.title('AMPA and NMDA impact on voltage ' +" ".join(model_place.split('/')[-1].split('_')[2:]) + '\n' + passive_propert_title)
    plt.legend()
    plt.savefig(folder_save+type+'.png')
    pickle.dump(figure, open(folder_save+type+'.p', 'wb'))
    plt.close()

