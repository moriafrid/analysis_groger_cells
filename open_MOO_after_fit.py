#! /ems/elsc-labs/segev-i/yoni.leibner/anaconda2/bin/ipython
# 70
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


class OPEN_RES():
    def __init__(self, res_pos, curr_i=0):
        """
        curr_i should be overridden as not 0 if this is called multiple times (if called within for loop)
        """
        from extraClasses import NrnSegmentSomaDistanceScaler_, NrnSectionParameterPas, neuron_start_time, \
            EFeatureImpadance, EFeaturePeak, EFeaturePeakTime, EFeatureRDSM, NrnNetstimWeightParameter, \
            SweepProtocolRin2
        self.res_pos = res_pos
        self.dt = 0.1
        self.hall = hall = pickle.load(open(self.res_pos + 'hall_of_fame.p', 'rb'))
        # self.morph_path = hall['model'].split('morphology')[1].split('\n')[1].strip() # remove spaces
        self.morph_path = hall['model'].split('\n')[2].strip()  # remove spaces
        self.fixed_params_res = dict()
        self.optimization_params_res = dict()
        for line in hall['model'].split('params:')[1].split('\n'):
            param_name = line.split(':')[0].strip()
            if len(line.split('=')) >= 2 and line.split('=')[1].find('[') == -1:
                self.fixed_params_res[param_name.strip()] = float(line.split('=')[1])
        hall_of_phase_results = np.array(hall['hall_of_fame'].items)
        for i, param in enumerate(hall['parameters']):
            self.optimization_params_res[param] = hall_of_phase_results[:, i]

        self.mechanisms = {}
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
        self.synapses_locations = hall['syn_location']
        self.spine_properties = hall['spine']
        import re
        self.shrinkage_by, self.resize_dend_by = re.findall("\d+\.\d+", self.res_pos.split('/')[4])
        self.morphology = ephys.morphologies.NrnFileMorphology(self.morph_path, load_cell_function=load_swc,
                                                               do_replace_axon=True,
                                                               resize_dend_by=float(self.resize_dend_by),
                                                               shrinkage_by=float(self.shrinkage_by))
        self.mechanism_list = []
        sec_list = location_dict['all']
        # for mech in self.mechanisms.keys():
        self.mechanism_list.append(ephys.mechanisms.NrnMODMechanism(name='pas', prefix='pas', locations=sec_list))
        self.spine_start = int(re.findall("\d+", self.res_pos.split('/')[3])[0])
        self.F_factor = hall['F_factor']
        F_FACTOR_DISTANCE = NrnSegmentSomaDistanceScaler_(name='spine_factor',
                                                          dist_thresh_apical=self.spine_start,
                                                          dist_thresh_basal=self.spine_start,
                                                          F_factor=self.F_factor)
        self.parameters_list = []
        for parameter in self.fixed_params_res.keys():
            if parameter in ['cm', 'g_pas']:
                self.parameters_list.append(ephys.parameters.NrnSectionParameter(name=parameter, param_name=parameter,
                                                                                 value_scaler=F_FACTOR_DISTANCE,
                                                                                 value=self.fixed_params_res[parameter],
                                                                                 locations=sec_list, frozen=True))
            elif parameter in ['Ra', 'e_pas']:
                self.parameters_list.append(ephys.parameters.NrnSectionParameter(name=parameter, param_name=parameter,
                                                                                 value=self.fixed_params_res[parameter],
                                                                                 locations=sec_list, frozen=True))
        self.sim = ephys.simulators.NrnSimulator(cvode_active=False, dt=self.dt)
        self.model = ephys.models.CellModel('Model' + str(curr_i), morph=self.morphology, mechs=self.mechanism_list,
                                            params=self.parameters_list)
        self.model.instantiate(self.sim)
        self.hoc_model = getattr(self.sim.neuron.h, 'Model' + str(curr_i))[0]  # unique Model name - otherwise it will not override (despite destroy ahaaahhhaaa)
        # print("Loaded ", self.fixed_params_res)
        # print("Params: ", [(self.parameters_list[i].to_dict()['value'], self.parameters_list[i].to_dict()['name']) for i in range(len(self.parameters_list))])

    def get_model(self):
        return self.hoc_model

    def create_synapse(self, sec, pos, weight, number=0,
                       hall_of_fame_num=0, netstim=None, ignore_netstim=False):

        spine = self.create_spine(sec, pos, number=number,
                                  neck_diam=self.hall['spine'][number]["NECK_DIAM"],
                                  neck_length=self.hall['spine'][number]["NECK_LENGHT"],
                                  head_diam=self.hall['spine'][number]["HEAD_DIAM"])
        if self.hall['spine'][number]["NECK_LENGHT"]==0:
            position=spine[0]
            # spine_temp=[spine[1],spine[0]]

        else:
            position=1
            # spine_temp=spine

        if not ignore_netstim:
            syn_obj = self._add_syn_on_sec(spine[1], weight, pos=position, hall_of_fame_num=hall_of_fame_num, netstim=netstim)
        else:
            syn_obj = None
        return spine, syn_obj

    def create_spine(self, sec, pos, number=0, neck_diam=0.25, neck_length=1.35,
                     head_diam=0.944):  # np.sqrt(2.8/(4*np.pi))
        if  head_diam== 0 or neck_diam== 0:
            return [pos,sec]
        neck = self.sim.neuron.h.Section(name="spineNeck" + str(number))
        head = self.sim.neuron.h.Section(name="spineHead" + str(number))
        # self.hoc_model.all.append(neck)
        # self.hoc_model.all.append(head)
        neck.L = neck_length
        neck.diam = neck_diam
        head.L = head.diam = head_diam
        head.connect(neck(1))
        neck.connect(sec(pos))
        self.sim.neuron.h("access " + str(neck.hoc_internal_name()))
        self.hoc_model.all.append(neck)
        if sec.name().find('apic') > -1:
            self.hoc_model.apical.append(neck)
        else:
            self.hoc_model.basal.append(neck)
        self.sim.neuron.h.pop_section()
        self.sim.neuron.h("access " + str(head.hoc_internal_name()))
        self.hoc_model.all.append(head)
        if sec.name().find('apic') > -1:
            self.hoc_model.apical.append(head)
        else:
            self.hoc_model.basal.append(head)
        self.sim.neuron.h.pop_section()
        for sec in [neck, head]:
            sec.insert("pas")
            sec.g_pas = self.get_param('g_pas')
            sec.e_pas = self.get_param('e_pas')
            sec.cm = self.get_param('cm')
            sec.Ra = self.get_param('Ra')
        return [neck, head]

    def get_param(self, param_name, hall_num=0):
        if param_name in self.fixed_params_res.keys():
            return self.fixed_params_res[param_name]
        elif param_name in self.optimization_params_res.keys():
            return self.optimization_params_res[param_name][hall_num]
        raise Exception('parameter name isnt correct: ' + str(param_name))

    def _add_syn_on_sec(self, sec, weight, pos=1, netstim=None, hall_of_fame_num=0):
        if netstim == None:
            raise Exception('we need netstim!:)')
        AMPA_PART = self.sim.neuron.h.Exp2Syn(sec(pos))
        NMDA_PART = self.sim.neuron.h.NMDA(sec(pos))
        AMPA_PART.tau1 = self.get_param('exp2syn_tau1', hall_of_fame_num)
        AMPA_PART.tau2 = self.get_param('exp2syn_tau2', hall_of_fame_num)
        AMPA_PART.e = 0
        NMDA_PART.e = 0
        NMDA_PART.tau_r_NMDA = self.get_param('NMDA_tau_r_NMDA', hall_of_fame_num)
        NMDA_PART.tau_d_NMDA = self.get_param('NMDA_tau_d_NMDA', hall_of_fame_num)
        NMDA_PART.n_NMDA = self.get_param('NMDA_n_NMDA', hall_of_fame_num)
        NMDA_PART.gama_NMDA = self.get_param('NMDA_gama_NMDA', hall_of_fame_num)
        netcon_AMPA = self.sim.neuron.h.NetCon(netstim, AMPA_PART)
        netcon_NMDA = self.sim.neuron.h.NetCon(netstim, NMDA_PART)
        netcon_AMPA.weight[0] = self.get_param('weight_AMPA', hall_of_fame_num) * weight
        netcon_NMDA.weight[0] = self.get_param('weight_NMDA', hall_of_fame_num) * weight
        # netcon_NMDA.weight[0]=0
        return [AMPA_PART, netcon_AMPA], [NMDA_PART, netcon_NMDA]

    # def __del__(self):
    #     self.destroy()
        # self.hoc_model=None
        # self.model=None
        # pass

    def destroy(self):
        self.model.destroy(self.sim)
        self.hoc_model.destroy(self.sim)
        self.morphology.destroy(self.sim)
        # for curr in self.parameters_list:
        #     curr.destroy(self.sim)

