#! /ems/elsc-labs/segev-i/yoni.leibner/anaconda2/bin/ipython
#70
from __future__ import print_function
import bluepyopt as bpopt
import bluepyopt.ephys as ephys
import pprint
import numpy as np
import os, pickle
from add_figure import add_figure
from open_pickle import read_from_pickle
from calculate_F_factor import calculate_F_factor
import signal
def SIGSEGV_signal_arises(signalNum, stack):
    print(f"{signalNum} : SIGSEGV arises")
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

def create_spine(sim, icell, sec, seg, number=0, neck_diam=0.25, neck_length=1.35,
                 head_diam=0.944):  # np.sqrt(2.8/(4*np.pi))
    neck = sim.neuron.h.Section(name="spineNeck" + str(number))
    head = sim.neuron.h.Section(name="spineHead" + str(number))
    # icell.add_sec(neck)#?# moria why add twice??
    # icell.add_sec(head)
    neck.L = neck_length
    neck.diam = neck_diam
    head.L = head.diam = head_diam
    head.connect(neck(1))
    neck.connect(sec(seg))
    sim.neuron.h("access " + str(neck.hoc_internal_name()))
    try: icell.add_sec(neck)
    except:
        icell.all.append(neck)
        if sec.name().find('apic') > -1:
            icell.apical.append(neck)
        else:
            icell.basal.append(neck)
    # if sec.name().find('dend') > -1: #?# moria- need to be sure it is ok to remove the neck and head from the dend list
    #     icell.dend.append(neck)
    # else:
    #     icell.apical.append(neck)
    sim.neuron.h.pop_section()
    sim.neuron.h("access " + str(head.hoc_internal_name()))
    try:icell.add_sec(head) #if using in hoc or ASC file (load_hoc,load_ASC
    except:
        icell.all.append(head) #if using in swc
        if sec.name().find('apic') > -1:
            icell.apical.append(head)
        else:
            icell.basal.append(head)
    # if sec.name().find('dend') > -1: #?# moria- need to be sure it is ok to remove the neck and head from the dend list
    #     icell.dend.append(head)
    # else:
    #     icell.apical.append(head)
    sim.neuron.h.pop_section()
    for sec in [neck, head]:
        sec.insert("pas")
    neck.g_pas = 1.0 / passive_val["RM"]
    neck.cm= passive_val["CM"]
    neck.Ra=passive_val["RA"]#int(Rneck)
    # neck.e_pas=E_pas
    # head.e_pas=icell.soma[0].e_pas
    return [neck, head]


def add_morph(sim, icell, syns, spine_properties):#,spine_property=self.spine_propertie
    all = []
    # sim.neuron.h.execute('create spineNeck['+str(len(syns))+']', icell)
    # sim.neuron.h.execute('create spineHead['+str(len(syns))+']', icell)
    for i, syn in enumerate(syns):
        num = syn[0]
        num = int(num[num.find("[") + 1:num.find("]")])
        if syn[0].find("dend") > -1:
            sec = icell.dend[num]
        elif syn[0].find("apic") > -1 :
            sec = icell.apic[num]
        else:
            sec = list(icell.soma)[0]
        all.append(create_spine(sim, icell, sec, syn[1], i, neck_diam=spine_properties[i]['NECK_DIAM'], neck_length=spine_properties[i]['NECK_LENGHT'],
                            head_diam=spine_properties[i]['HEAD_DIAM']))
    return all
class OPEN_RES():
    def __init__(self, res_pos):
        from extraClasses import NrnSegmentSomaDistanceScaler_, NrnSectionParameterPas, neuron_start_time, \
            EFeatureImpadance, EFeaturePeak, EFeaturePeakTime, EFeatureRDSM, NrnNetstimWeightParameter, \
            SweepProtocolRin2
        self.res_pos = res_pos
        self.dt=0.1
        self.hall = hall = pickle.load(open(self.res_pos + 'hall_of_fame.p', 'rb'))
        # self.morph_path = hall['model'].split('morphology')[1].split('\n')[1].strip() # remove spaces
        self.morph_path = hall['model'].split('\n')[2].strip() # remove spaces
        self.fixed_params_res = dict()
        self.optimization_params_res = dict()
        # self.reletive_strengths=[spine['weigth'] for spine in hall['spine'].values()]
        for line in hall['model'].split('params:')[1].split('\n'):
            param_name = line.split(':')[0]
            if len(line.split('='))>=2 and line.split('=')[1].find('[')==-1:
                self.fixed_params_res[param_name.strip()] = float(line.split('=')[1])
        hall_of_phase_results = np.array(hall['hall_of_fame'].items)
        for i, param in enumerate(hall['parameters']):
            self.optimization_params_res[param] = hall_of_phase_results[:, i]

        self.mechanisms={}
        somatic_loc = ephys.locations.NrnSeclistLocation('somatic', seclist_name='somatic')
        basal_loc = ephys.locations.NrnSeclistLocation('basal', seclist_name='basal')
        apical_loc = ephys.locations.NrnSeclistLocation('apical', seclist_name='apical')
        axonal_loc = ephys.locations.NrnSeclistLocation('axonal', seclist_name='axonal')
        location_dict = {'all': [somatic_loc, basal_loc, apical_loc, axonal_loc],
                         'somatic': [somatic_loc],
                         'apical': [apical_loc],
                         'basal': [basal_loc],
                         'axonal': [axonal_loc]}

        # self.spine_properties=hall['spine']

        from extra_function import load_swc
        self.synapses_locations=hall['syn_location']
        self.spine_properties=hall['spine']
        import re
        self.shrinkage_by,self.resize_dend_by=re.findall("\d+\.\d+",self.res_pos.split('/')[4])
        # self.morphology = ephys.morphologies.NrnFileMorphology(self.morph_path, load_cell_function=load_swc,do_replace_axon=True,
        #                                                   resize_dend_by=float(self.resize_dend_by),shrinkage_by=float(self.shrinkage_by))
        self.morphology = ephys.morphologies.NrnFileMorphology(self.morph_path, load_cell_function=load_swc,do_replace_axon=True,
                                                      extra_func=True, extra_func_run=add_morph, spine_poses=self.synapses_locations
                                                      ,resize_dend_by=float(self.resize_dend_by),shrinkage_by=float(self.shrinkage_by),
                                                      spine_properties=self.spine_properties)
        self.mechanism_list=[]
        sec_list=location_dict ['all']
        # for mech in self.mechanisms.keys():
        self.mechanism_list.append(ephys.mechanisms.NrnMODMechanism(name='pas', prefix='pas', locations=sec_list))
        self.spine_start=int(re.findall("\d+",self.res_pos.split('/')[3])[0])
        self.F_factor=hall['F_factor']
        F_FACTOR_DISTANCE = NrnSegmentSomaDistanceScaler_(name='spine_factor',
                                                          dist_thresh_apical=self.spine_start,
                                                          dist_thresh_basal=self.spine_start,
                                                          F_factor=self.F_factor,
                                                          shrinckage_factor=self.shrinkage_by) #the shrinkage factor is unused in that function
        self.parameters_list=[]
        for parameter in self.fixed_params_res.keys():
            if parameter in ['cm', 'g_pas']:
                self.parameters_list.append(ephys.parameters.NrnSectionParameter(name=parameter, param_name=parameter,value_scaler=F_FACTOR_DISTANCE, value=self.fixed_params_res[parameter], locations=sec_list,frozen=True))
            elif parameter in ['Ra', 'e_pas']:
                self.parameters_list.append(ephys.parameters.NrnSectionParameter(name=parameter, param_name=parameter, value=self.fixed_params_res[parameter], locations=sec_list,frozen=True))
            syn_locations = []
        syn_mec = []
        tau_param_locs = []
        param_locs = []
        NMDA_param_locs = []
        syn_params = []
        netstims = []
        netstims_NMDA = []
        rec = []
        somacenter_loc = ephys.locations.NrnSeclistCompLocation(
            name='somacenter',
            seclist_name='somatic',
            sec_index=0,
            comp_x=0.5)
        for i, syn in enumerate(self.synapses_locations):
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

        # # this only for the first synapse in that cell
            number = 1
            interval = 1
            hall_of_fame_num = 0
            #import stim_start and total_duration relatve_strenge need betaken fro spine properties from the experiment
            netstims.append(ephys.stimuli.NrnNetStimStimulus(
                total_duration=total_duration,
                number=number,
                interval=interval,
                start=stim_start,
                weight=5e-4,
                locations=[tau_param_locs[i]]))

            netstims_NMDA.append(ephys.stimuli.NrnNetStimStimulus(
                total_duration=total_duration,
                number=number,
                interval=interval,
                start=stim_start,
                weight=5e-4,
                locations=[NMDA_param_locs[i]]))

            syn_params.append(NrnNetstimWeightParameter(
                name='weight_AMPA',
                param_name='weight[0]',
                frozen=True,
                value=self.optimization_params_res['weight_AMPA'][hall_of_fame_num],
                locations=[netstims[i]],
                reletive_strength = [self.hall['spine'][i]['weight']])) #[1, 0.1,0.01]))

            syn_params.append(NrnNetstimWeightParameter(
                name='weight_NMDA',
                param_name='weight[0]',
                frozen=True,
                value=self.optimization_params_res['weight_NMDA'][hall_of_fame_num],
                locations=[netstims_NMDA[i]],
                reletive_strength = [self.hall['spine'][i]['weight']])) #[1, 0.1,0.01]))

            rec.append(ephys.recordings.CompRecording(
                name='syn'+str(i)+'.v',
                location=syn_locations[0],
                variable='v'))
        rec.append(ephys.recordings.CompRecording(
            name='soma.v',
            location=somacenter_loc,
            variable='v'))



        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='exp2syn_tau1',
            param_name='tau1',
            value=self.optimization_params_res['exp2syn_tau1'][hall_of_fame_num],
            bounds=[0.001, 2.1],#[0.1, 0.4],
            frozen=True,
            locations=tau_param_locs))
        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='exp2syn_tau2',
            param_name='tau2',
            value=self.optimization_params_res['exp2syn_tau2'][hall_of_fame_num],#1.8,  # min(AMPA_FIT[cell]['tau2'],8),
            frozen=True,
            bounds=[0.01, 4],
            locations=tau_param_locs))

        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='NMDA_tau_r_NMDA',
            param_name='tau_r_NMDA',
            value=self.optimization_params_res['NMDA_tau_r_NMDA'][hall_of_fame_num],
            frozen=True,
            bounds=[3, 15],
            locations=NMDA_param_locs))
        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='NMDA_tau_d_NMDA',
            param_name='tau_d_NMDA',
            value=self.optimization_params_res['NMDA_tau_d_NMDA'][hall_of_fame_num],
            frozen=True,
            bounds=[25, 90],
            locations=NMDA_param_locs))
        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='NMDA_n_NMDA',
            param_name='n_NMDA',
            value=self.fixed_params_res['NMDA_n_NMDA'],
            frozen=True,
            bounds=[0.1, 0.4],
            locations=NMDA_param_locs))
        syn_params.append(ephys.parameters.NrnPointProcessParameter(
            name='NMDA_gama_NMDA',
            param_name='gama_NMDA',
            value=self.fixed_params_res['NMDA_gama_NMDA'],
            frozen=True,
            bounds=[0.06, 0.09],
            locations=NMDA_param_locs))

        protocol = ephys.protocols.SweepProtocol('netstim_protocol', netstims + netstims_NMDA, [rec[-1]], cvode_active=False)
        protocol_spine_head=[]
        for i in range(len(self.synapses_locations)):
            protocol_spine_head.append(ephys.protocols.SweepProtocol('netstim_protocol', netstims+ netstims_NMDA , [rec[i]], cvode_active=False))

        self.sim=ephys.simulators.NrnSimulator(cvode_active=False,dt=self.dt)
        self.model = ephys.models.CellModel('Model', morph=self.morphology, mechs=self.mechanism_list+ syn_mec,
                                   params=self.parameters_list)
        self.model.instantiate(self.sim)
        self.hoc_model = self.sim.neuron.h.Model[-1]

    def get_model(self):
        return self.hoc_model

    def get_param(self, param_name, hall_num=0):
        if param_name in self.fixed_params_res.keys():
            return self.fixed_params_res[param_name]
        elif param_name in self.optimization_params_res.keys():
            return self.optimization_params_res[param_name][hall_num]
        raise Exception('parameter name isnt correct: '+str(param_name))
    # def create_synapse(self, sec, pos, weight,number = 0,
    #                    hall_of_fame_num = 0, netstim=None, ignore_netstim=False):
    #
    #     spine = self.create_spine(sec, pos, number = number,
    #                    neck_diam = self.hall['spine'][number]["NECK_DIAM"], neck_length = self.hall['spine'][number]["NECK_LENGHT"],
    #                    head_diam = self.hall['spine'][number]["HEAD_DIAM"])
    #
    #     if not ignore_netstim:
    #         syn_obj = self._add_syn_on_sec(spine[1], weight,pos=1, hall_of_fame_num=hall_of_fame_num, netstim=netstim)
    #     else:
    #         syn_obj = None
    #     return spine, syn_obj
    #
    #
    # def create_spine(self, sec, pos, number=0, neck_diam=0.25, neck_length=1.35,
    #                  head_diam=0.944):  # np.sqrt(2.8/(4*np.pi))
    #     neck = self.sim.neuron.h.Section(name="spineNeck" + str(number))
    #     head = self.sim.neuron.h.Section(name="spineHead" + str(number))
    #     # self.hoc_model.all.append(neck)
    #     # self.hoc_model.all.append(head)
    #     neck.L = neck_length
    #     neck.diam = neck_diam
    #     head.L = head.diam = head_diam
    #     head.connect(neck(1))
    #     neck.connect(sec(pos))
    #     self.sim.neuron.h("access " + str(neck.hoc_internal_name()))
    #     self.hoc_model.all.append(neck)
    #     if sec.name().find('apic') > -1:
    #         self.hoc_model.apical.append(neck)
    #     else:
    #         self.hoc_model.basal.append(neck)
    #     self.sim.neuron.h.pop_section()
    #     self.sim.neuron.h("access " + str(head.hoc_internal_name()))
    #     self.hoc_model.all.append(head)
    #     if sec.name().find('apic') > -1:
    #         self.hoc_model.apical.append(head)
    #     else:
    #         self.hoc_model.basal.append(head)
    #     self.sim.neuron.h.pop_section()
    #     for sec in [neck, head]:
    #         sec.insert("pas")
    #         sec.g_pas = self.get_param('g_pas')
    #         sec.e_pas = self.get_param('e_pas')
    #         sec.cm = self.get_param('cm')
    #         sec.Ra = self.get_param('Ra')
    #     return [neck, head]



    # def _add_syn_on_sec(self, sec,weight, pos=1, netstim=None, hall_of_fame_num=0):
    #     if netstim == None:
    #         raise Exception('we need netstim!:)')
    #     AMPA_PART = self.sim.neuron.h.Exp2Syn(sec(pos))
    #     NMDA_PART = self.sim.neuron.h.NMDA(sec(pos))
    #     AMPA_PART.tau1 = self.get_param('exp2syn_tau1', hall_of_fame_num)/(1+0.34)
    #     AMPA_PART.tau2 = self.get_param('exp2syn_tau2', hall_of_fame_num)/(1+0.34)
    #     AMPA_PART.e = 0
    #     NMDA_PART.e = 0
    #     NMDA_PART.tau_r_NMDA=self.get_param('NMDA_tau_r_NMDA', hall_of_fame_num)/(1+0.34)
    #     NMDA_PART.tau_d_NMDA=self.get_param('NMDA_tau_d_NMDA', hall_of_fame_num)/(1+0.34)
    #     NMDA_PART.n_NMDA=self.get_param('NMDA_n_NMDA', hall_of_fame_num)
    #     NMDA_PART.gama_NMDA=self.get_param('NMDA_gama_NMDA', hall_of_fame_num)
    #     netcon_AMPA = self.sim.neuron.h.NetCon(netstim, AMPA_PART)
    #     netcon_NMDA = self.sim.neuron.h.NetCon(netstim, NMDA_PART)
    #     netcon_AMPA.weight[0] = self.get_param('weight_AMPA', hall_of_fame_num)*weight/(1+0.34)
    #     netcon_NMDA.weight[0] = self.get_param('weight_NMDA', hall_of_fame_num)*weight/(1+0.34)
    #     # netcon_NMDA.weight[0]=0
    #     return [AMPA_PART, netcon_AMPA], [NMDA_PART, netcon_NMDA]

    def __del__(self):
        # self.hoc_model=None
        # self.destroy()
        pass

    def destroy(self):
        self.model.destroy(self.sim)


