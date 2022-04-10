from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
import os
from glob import glob
import sys
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese
from tqdm import tqdm
import pickle
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['png.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

if len(sys.argv) != 7:
  cell_name= '2017_05_08_A_5-4'
  file_type='z_correct.swc'
  resize_diam_by=1.0
  shrinkage_factor=1.0
  SPINE_START=20
else:
  cell_name = sys.argv[1]
  file_type=sys.argv[2] #hoc ar ASC
  resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
  shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
  SPINE_START=int(sys.argv[5])
folder_= ''
folder_data=folder_+'cells_outputs_data_short/*/MOO_results*/*/F_shrinkage=*/const_param/'
save_name='/Voltage Spine&Soma'

for model_place in tqdm(glob(folder_data+'*')):
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if type=='test': continue
    loader=None
    try:loader = OPEN_RES(res_pos=model_place+'/')
    except:
        print(model_place + '/hall_of_fame.p is not exsist' )
        continue
    model=None
    model=loader.get_model()
    # for sec in model.dend:
    #     if sec.cm/2>1.5:
    #         sec.cm=2
    #     else:
    #         sec.cm=1
    # model.soma[0].cm=1

    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = 200
    netstim.noise = 0
    secs,segs=get_sec_and_seg(cell_name)
    num=0
    V_spine=[]
    spines=[]
    syn_objs=[]

    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,params=dict_spine_param, number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        V_spine.append(h.Vector())
        V_spine[num].record(spine[1](1)._ref_v)
        num+=1

    h.tstop = 300
    time = h.Vector()
    time.record(h._ref_t)
    V_soma = h.Vector()
    V_soma.record(model.soma[0](0.5)._ref_v)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()

    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    V_soma=np.array(V_soma)[1900:]
    time=np.array(time)[1900:]
    names=["A","B"]

    fig = plt.figure(figsize=(10,10))

    if get_n_spinese(cell_name) == 2:
       axs = fig.subplot_mosaic("""AB""")
    else:
       axs = fig.subplot_mosaic("""A""")

    fig.suptitle('Voltage in Spine and Soma\n '+" ".join([model_place.split('/')[1],model_place.split('/')[-1] ,'\n',model_place.split('/')[4],model_place.split('/')[2]])+'\n'+passive_propert_title)

    for j in range(len(V_spine)):
        print(j)
        V_spine[j]=np.array(V_spine[j])[1900:]
        axs[names[j]].set_title('spine'+str(j)+" "+secs[j]+" "+str(segs[j]))
        axs[names[j]].plot(time, V_soma,'green',label='V_soma higth:'+str(round(np.amax(V_soma)-np.amin(V_soma),2))+'mV')
        axs[names[j]].plot(time, V_spine[j],'orange',label='V_spine'+str(j)+ ' higth:'+str(round(np.amax(V_spine[j])-np.amin(V_spine[j]),2))+'mV')
        axs[names[j]].set_xlabel('time [ms]')
        axs[names[j]].set_ylabel('voltage [mv]')
        axs[names[j]].legend()

    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))

    # plt.show()

