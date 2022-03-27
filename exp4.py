from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
import os
from glob import glob
from tqdm import tqdm
from add_figure import add_figure
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg,get_building_spine

from extra_function import create_folder_dirr
import sys
if len(sys.argv) != 7:
   cell_name= '2017_05_08_A_5-4'
   file_type='z_correct.swc'
   resize_diam_by=1.0
   shrinkage_factor=1.0
   SPINE_START=30
   folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
   cell_name = sys.argv[1]
   file_type=sys.argv[2] #hoc ar ASC
   resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
   shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
   SPINE_START=int(sys.argv[5])
   folder_= sys.argv[6] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
folder_data=folder_+'cells_outputs_data/'+cell_name+'/MOO_results/'+file_type+'/F_shrinkage='+str(shrinkage_factor)+'_dend*'+str(resize_diam_by)+'/const_param/'
folder_save=folder_+'/hall_of_fame_together/'
type='outomatic'

create_folder_dirr(folder_save)

for model_place in glob(folder_data+'*'):
    type=model_place.split('/')[-1]
    if type=='test': continue

    add_figure('AMPA and NMDA impact on voltage ' + type,'mV', 'mS')
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
        for sec,seg in zip(secs,segs):
            dict_spine_param=get_building_spine(cell_name,num)
            spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,params=dict_spine_param, number=num,netstim=netstim, hall_of_fame_num=i)
            V_spine.append(h.Vector())
            V_spine[num].record(spine[1](1)._ref_v)
            num+=1
            print(num)
        h.dt = 0.1
        h.steps_per_ms = 1.0 / h.dt
        h.run()
        names=["A","B"]

        figure, axis = plt.subplots(1, len(V_spine))
        if len(V_spine) == 1:
            axis = axis[..., np.newaxis]
        if len(secs)>1:
            fig = plt.figure(figsize=(10,10))
            axs = fig.subplot_mosaic("""AB""")
        else:
            axs = fig.subplot_mosaic("""A""")

        time=np.array(time)[1900:]

        for i in range(len(V_spine)):
            V_spine[i]=np.array(V_spine)[1900:]
            axs[i].plot(time,V_spine[i], label='hall_'+str(i),alpha=0.1)
            # axis[0,i].set_title("spine voltage")
            axis[i].set_xlabel('ms')
            axis[i].set_ylabel('mv')

        # plt.plot(time, V_spine, label='hall_'+str(i),alpha=0.1)
    passive_propert_title='Rm='+str(round(1.0/model.dend[82].g_pas,2)) +' Ra='+str(round(model.dend[82].Ra,2))+' Cm='+str(round(model.dend[82].cm,2))
    plt.title('AMPA and NMDA impact on voltage ' +" ".join(model_place.split('/')[-1].split('_')[2:]) + '\n' + passive_propert_title)
    plt.legend()
    plt.savefig(folder_save+type+'.png')
