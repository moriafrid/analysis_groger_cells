from open_MOO_after_fit import OPEN_RES
import numpy as np
# from neuron import h
import matplotlib.pyplot as plt
from read_spine_properties import get_sec_and_seg,get_building_spine,get_n_spinese,get_parameter
import os
from glob import glob
from tqdm import tqdm
import pickle
import matplotlib
from add_figure import add_figure
from open_pickle import read_from_pickle

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

folder_= ''
folder_data=folder_+'cells_outputs_data_short/*/MOO_results*/*/F_shrinkage=*/const_param/'
save_name='/fit_transient_RDSM'

for model_place in tqdm(glob(folder_data+'*')):
    print(model_place)
    model_type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if model_type=='test': continue
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
    spines=[]
    syn_objs=[]
    for sec,seg in zip(secs,segs):
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num], number=num,netstim=netstim)
        # for sec_ in spine:
        #     sec_.cm=1.9
        #     sec_.g_pas = 1.0/8000.0
        #     sec_.Ra=120
        spines.append(spine)
        syn_objs.append(syn_obj)
        num+=1
    fig=add_figure('fit_transient_RDSM\n','time[ms]','Voltage[mV]')
    short_pulse_parameters_file=folder_+'cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse_parameters.p'
    RDSM_objective_file = folder_+'cells_initial_information/'+cell_name+"/mean_syn.p"
    E_PAS=read_from_pickle(short_pulse_parameters_file)['E_pas']
    T_data,V_data=read_from_pickle(RDSM_objective_file)
    T_data=T_data.rescale('ms')
    T_data-=T_data[0]
    plt.plot(T_data, np.array(V_data)+E_PAS, color='black',label='EP record',alpha=0.2,lw=5)

    for ii, e_pas in enumerate([model.soma[0].e_pas, -70]):
        print('e_pas=', e_pas)

        h.tstop = 400
        time = h.Vector()
        time.record(h._ref_t)
        V_soma = h.Vector()
        V_soma.record(model.soma[0](0.5)._ref_v)
        h.dt = 0.1
        h.steps_per_ms = 1.0/h.dt
        h.run()
        time=np.array(time)
        V_soma=np.array(V_soma)


        for spine in spines:
            for sec_ in spine:
                sec_.e_pas = e_pas
        passive_propert_title='Rm='+str(round(1.0/loader.get_param('g_pas'),2)) +' Ra='+str(round(loader.get_param('Ra'),2))+' Cm='+str(round(loader.get_param('cm'),2))
        # plt.suptitle('\n'+model_place.split('/')[4]+'\n'+passive_propert_title,fontsize=10)
        plt.plot(time[1000:]-time[1000], V_soma[1000:], lw=(ii+1)*2, label='e_pas='+str(round(e_pas, 2)), alpha=0.5)



    # plt.plot([], [], ' ', label='gmax_AMPA='+str(round(loader.get_param('weight_AMPA')*1000,3))+' [nS] \ngmax_NMDA=' +str(round(loader.get_param('weight_NMDA')*1000,3))+' [nS]\nrelative strenght '+str(reletive_strengths))
    plt.legend()
    plt.show()
    plt.close()
