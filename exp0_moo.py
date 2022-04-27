import signal

from bluepyopt import ephys

from extraClasses import NrnNetstimWeightParameter
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
from extra_function import SIGSEGV_signal_arises
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
folder_= ''
folder_data=folder_+'cells_outputs_data_short/*6-7/MOO_results*re*/*/F_shrinkage=*/const_param'
save_name='/fit_transient_RDSM'

for model_place in tqdm(glob(folder_data+'/*')):
    print(model_place)
    model_type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    if 'relative' in model_place:
        psd_sizes=get_parameter(cell_name,'PSD')
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        reletive_strengths=np.ones(get_n_spinese(cell_name))
    if model_type!='test': continue
    loader=None
    model=None

    short_pulse_parameters_file=folder_+'cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse_parameters.p'
    RDSM_objective_file = folder_+'cells_initial_information/'+cell_name+"/mean_syn.p"
    T_data,V_data=read_from_pickle(RDSM_objective_file)
    T_data=T_data.rescale('ms')
    T_data-=T_data[0]
    E_PAS=read_from_pickle(short_pulse_parameters_file)['E_pas']

    # new
    ignore_netstim = True
    netstim = None

    try:loader = OPEN_RES(res_pos=model_place+'/')
    except:
       print(model_place + '/hall_of_fame.p is not exsist' )
       continue
    model=loader.get_model()

    # h=loader.sim.neuron.h
    # netstim = h.NetStim()  # the location of the NetStim does not matter
    # netstim.number = 1
    # netstim.start = 200
    # netstim.noise = 0

    # secs,segs=get_sec_and_seg(cell_name)
    secs=[]
    segs=[]
    import pandas as pd
    synapses_dict=pd.read_excel(folder_+'cells_outputs_data_short/'+"synaptic_location_seperate.xlsx",index_col=0)
    for i in range(get_n_spinese(cell_name)):
        sec=synapses_dict[cell_name+str(i)]['sec_name']
        seg=float(synapses_dict[cell_name+str(i)]['seg_num'])
        print(sec, seg)
        secs.append(sec)
        segs.append(seg)
    num=0
    V_spine=[]
    spines=[]
    syn_objs=[]
    for sec,seg in zip(secs,segs):
        spine, syn_obj = loader.create_synapse(eval('model.'+sec), seg,reletive_strengths[num], number=num,
                                               netstim=netstim, ignore_netstim=ignore_netstim)
        # for sec_ in spine:
        #     sec_.cm=1.9
        #     sec_.g_pas = 1.0/8000.0
        #     sec_.Ra=120
        spines.append(spine)
        syn_objs.append(syn_obj)
        num+=1

    ############################
    best_params = {}  #loader.fixed_params_res
    for k, values in loader.optimization_params_res.items():  # take 1st (best) param
        best_params[k] = values[0]
    netstims = []
    syn_locations = []
    syn_mec = []
    tau_param_locs = []
    param_locs = []
    NMDA_param_locs = []
    syn_params = []
    netstims_NMDA = []
    frozen_NMDA_weigth=True
    rec = []
    neuron_start_time = 300
    spike_timeing=T_data[np.argmax(np.array(V_data))-65]

    for i, syn in enumerate(loader.synapses_locations):
        syn_locations.append(ephys.locations.NrnSectionCompLocation(
            name='syn' + str(i),
            sec_name="spineHead" + str(i),#@#??
            comp_x=1)) #segx (0..1) of segment inside section


        # insert AMPA
        syn_mec.append(ephys.mechanisms.NrnMODPointProcessMechanism(
            name='exp2syn_' + str(i),
            suffix='Exp2Syn',
            locations=[syn_locations[-1]]))
        tau_param_locs.append(ephys.locations.NrnPointProcessLocation(
            'expsyn_loc' + str(i),
            pprocess_mech=syn_mec[-1])) #pprocess_mech (str) – point process mechanism

        # insert NMDA
        syn_mec.append(ephys.mechanisms.NrnMODPointProcessMechanism(
            name='NMDA_' + str(i),
            suffix='NMDA',
            locations=[syn_locations[-1]]))
        NMDA_param_locs.append(ephys.locations.NrnPointProcessLocation(
            'NMDA_loc' + str(i),
            pprocess_mech=syn_mec[-1]))
#@# why I need to add AMPA and NMDA recheptors for each synaptic location instead one
        #################################diff weight to synapses###################################################
        #
        stim_start = np.array(spike_timeing) + neuron_start_time
        # # this only for the first synapse in that cell
        number = 1
        interval = 1
        # for i in range(len(get_n_spine(cell_name)):
        netstims.append(ephys.stimuli.NrnNetStimStimulus(
            total_duration=np.array(T_data[-1]) + neuron_start_time,
            number=number,
            interval=interval,
            start=stim_start,
            weight=5e-4,
            locations=[tau_param_locs[i]]))

        netstims_NMDA.append(ephys.stimuli.NrnNetStimStimulus(
            total_duration=np.array(T_data[-1])+neuron_start_time,
            number=number,
            interval=interval,
            start=stim_start,
            weight=5e-4,
            locations=[NMDA_param_locs[i]]))

        syn_params.append(NrnNetstimWeightParameter(
            name='weight_AMPA',
            param_name='weight[0]',
            frozen=True,
            value=0.0099,
            # bounds=[0.000000, 0.02/sum(reletive_strengths)],#0.01],
            locations=[netstims[i]],
            reletive_strength = [reletive_strengths[i]])) #[1, 0.1,0.01]))
            # reletive_strength =   [get_parameter(cell_name,'PSD',spine_num=i)]))#[1, 0.1,0.01]))
    # this  need to add the weight to optimization

        syn_params.append(NrnNetstimWeightParameter(
            name='weight_NMDA',
            param_name='weight[0]',
            frozen=frozen_NMDA_weigth,
            value=0.0006,
            # bounds=[0.000, 0.005],
            locations=[netstims_NMDA[i]],
            reletive_strength = [reletive_strengths[i]])) #[1, 0.1,0.01]))
    #################################
    somacenter_loc = ephys.locations.NrnSeclistCompLocation(
        name='somacenter',
        seclist_name='somatic',
        sec_index=0,
        comp_x=0.5)
    rec.append(ephys.recordings.CompRecording(
        name='soma.v',
        location=somacenter_loc,
        variable='v'))
    # for syn_loc in syn_locations:
    rec.append(ephys.recordings.CompRecording(
        name='syn0.v',
        location=syn_locations[0],
        variable='v'))

    CM_FROZEN = True
    RA_FROZEN = True

    N_NMDA_FROZEN = True
    GAMMA_FROZEN = True

    AMPA_RISE_FIX = True
    AMPA_DECAY_FIX = True
    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='exp2syn_tau1',
        param_name='tau1',
        value=0.4364,
        frozen=AMPA_RISE_FIX,
        bounds=[0.001, 2.1],#[0.1, 0.4],
        locations=tau_param_locs))
    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='exp2syn_tau2',
        param_name='tau2',
        value=2.47,#1.8,  # min(AMPA_FIT[cell]['tau2'],8),
        frozen=AMPA_DECAY_FIX,
        bounds=[0.01, 4],#[1, 3],
        locations=tau_param_locs))

    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='NMDA_tau_r_NMDA',
        param_name='tau_r_NMDA',
        value=7.4,
        frozen=False,
        bounds=[7, 15],
        locations=NMDA_param_locs))
    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='NMDA_tau_d_NMDA',
        param_name='tau_d_NMDA',
        value=44.19,
        frozen=False,
        bounds=[25, 90],
        locations=NMDA_param_locs))
    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='NMDA_n_NMDA',
        param_name='n_NMDA',
        value=0.27,
        frozen=N_NMDA_FROZEN,
        bounds=[0.1, 0.4],
        locations=NMDA_param_locs))
    syn_params.append(ephys.parameters.NrnPointProcessParameter(
        name='NMDA_gama_NMDA',
        param_name='gama_NMDA',
        value=0.076,
        frozen=GAMMA_FROZEN,
        bounds=[0.06, 0.09],
        locations=NMDA_param_locs))

    protocol = ephys.protocols.SweepProtocol('netstim_protocol', netstims + netstims_NMDA, [rec[0]], cvode_active=False)
    # evaluator = ephys.evaluators.CellEvaluator(
    #     cell_model=model,
    #     param_names=param_names,
    #     fitness_protocols=fitness_protocols,
    #     fitness_calculator=fitness_calculator,
    #     sim=loader.sim)

    sim = ephys.simulators.NrnSimulator(cvode_active=False,dt=0.1)
    # model = ephys.models.CellModel('Model', morph=loader.morphology, mechs=loader.mechanism_list,
    #                                params=loader.parameters_list + syn_params,
    #                                # seclist_names=['dendritic']
    #                                )  # loader.model
    model = ephys.models.CellModel('Model', morph=loader.morphology, mechs=loader.mechanism_list + syn_mec,
                                   params=loader.parameters_list + syn_params,
                                   # seclist_names=['dendritic']
                                   )
    responses = protocol.run(cell_model=model, param_values=best_params, sim=sim)
    # responses = evaluator.run_protocols(protocols=fitness_protocols.values(), param_values=release_params)

    # h.tstop = 400
    # time = h.Vector()
    # time.record(h._ref_t)
    # V_soma = h.Vector()
    # V_soma.record(model.soma[0](0.5)._ref_v)
    # h.dt = 0.1
    # h.steps_per_ms = 1.0/h.dt
    # h.run()
    time = np.array(responses['soma.v']['time'])
    V_soma = np.array(responses['soma.v']['voltage'])

    passive_propert_title='Rm='+str(round(1.0/loader.get_param('g_pas'),2)) +' Ra='+str(round(loader.get_param('Ra'),2))+' Cm='+str(round(loader.get_param('cm'),2))
    fig=add_figure('fit_transient_RDSM\n','time[ms]','Voltage[mV]')
    plt.suptitle('\n'+model_place.split('/')[4]+'\n'+passive_propert_title,fontsize=10)
    plt.plot(time[1000:]-time[1000], V_soma[1000:], color='yellowgreen', lw=5,label='after fit')

    plt.plot(T_data, np.array(V_data)+loader.get_param('e_pas'), color='black',label='EP record',alpha=0.2,lw=5)



    plt.plot([], [], ' ', label='gmax_AMPA='+str(round(loader.get_param('weight_AMPA')*1000,3))+' [nS] \ngmax_NMDA=' +str(round(loader.get_param('weight_NMDA')*1000,3))+' [nS]\nrelative strenght '+str(reletive_strengths))

    plt.legend()
    plt.savefig(model_place+save_name+'_fig.png')
    # plt.savefig(model_place+save_name+'_fig.pdf')
    pickle.dump(fig, open(model_place+save_name+'_fig.p', 'wb'))

    plt.show()
