import os
import pickle

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from neuron import h, gui


def add_few_spines(sref_list, x_vec, neck_diam, neck_len, head_diam, spine_psd_area, ra, E_PAS=-86, CM=1, RM=10000,
                   spine_head_area=None):
    def create(num, is_head=True, is_psd=False):
        if is_head and not is_psd:
            sp = h.Section(name=f"spine_head{num}")
            sp.L = L_head
            sp.diam = diam_head
        elif is_head and is_psd:
            sp = h.Section(name=f"spine_head_psd{num}")
            sp.L = psd_L_head
            sp.diam = psd_diam_head
        else:
            sp = h.Section(name=f"spine_neck{num}")
            sp.L = neck_len
            sp.diam = neck_diam
        sp.insert('pas')
        sp.g_pas = 1 / RM  # 1/Rm - Rm ohm*cm^2
        sp.e_pas = E_PAS
        sp.cm = CM
        sp.Ra = ra  # ohm*cm
        return sp

    L_head = diam_head = head_diam
    if spine_head_area is not None:
        diam_head = L_head = 2*np.sqrt(spine_head_area / 4 / np.pi)  # sphere has the same surface area as cylinder with L=diam
    psd_L_head = psd_diam_head = 2*np.sqrt(spine_psd_area / 4 / np.pi)

    spines = []
    spine_psds=[]

    for i, sec in enumerate(sref_list):
        for j, shaft_x in enumerate(x_vec[i]):
            sp_head = create(j, is_head=True, is_psd=False)
            sp_head_psd = create(j, is_head=True, is_psd=True)
            sp_neck = create(j, is_head=False)
            spine_psds.append(sp_head_psd)
            spines.append(sp_neck)  # 2j
            spines.append(sp_head)  # 2j + 1
            sp_head_psd.connect(sp_head(1), 0)  # todo direction ok?
            sp_head.connect(sp_neck(1), 0)  # todo direction ok?
            sp_neck.connect(sec(shaft_x), 0)
            print(sp_head(1), " connect to begin of ", sp_head_psd, " with diam ", sp_head_psd.diam, " length ", sp_head_psd.L)
            print(sp_neck(1), " connect to begin of ", sp_head, " with diam ", sp_head.diam, " length ", sp_head.L)
            print(sec(shaft_x), " connect to begin of ", sp_neck, " with diam ", sp_neck.diam, " length ", sp_neck.L)
    return spines, spine_psds


def add_spines(dend, syn_segs, SPINE_NECK_DIAM=0.25, SPINE_NECK_L=1.35, SPINE_PSD_AREA=2.8, HEAD_DIAM=1.0):
    return add_few_spines([dend], [syn_segs], neck_diam=SPINE_NECK_DIAM, neck_len=SPINE_NECK_L, head_diam=HEAD_DIAM,
                          spine_psd_area=SPINE_PSD_AREA, ra=dend.Ra, CM=dend.cm, RM=1/dend.g_pas, E_PAS=dend.e_pas)  # todo!


def create_multiple_dend(n_dend=1, dend_ra=100, dend_cm=1, dend_rm=10000, debd_L_um=100, dend_diam_um=1):
    dend = []
    for i in range(n_dend):  # todo problem with injection
        d = h.Section(name=f"dend[{i}]")
        d.L = debd_L_um  # um
        d.diam = dend_diam_um  # um
        d.cm = dend_cm
        d.Ra = dend_ra
        d.insert('pas')
        d.g_pas = 1 / dend_rm
        if len(dend) > 0:
            print(dend[-1], " end connect to begin of ", d)
            dend[-1].connect(d, 1, 0)  # connect the begin of d to the start of the last dendrite
        dend.append(d)
    return dend  # list of dendrites


def add_short_pulse(clamp_at_seg, delay_ms=100, dur_ms=2, amp_na=0.5):
    stim = h.IClamp(clamp_at_seg.x, sec=clamp_at_seg.sec)  # add a current clamp the the middle of the soma
    stim.delay = delay_ms
    stim.dur = dur_ms
    stim.amp = amp_na
    return stim


def DefineSynapse_AMPA(segment, gMax=0.0004, tau_r=0.3, tau_d=3.0):
    synapse = h.ProbUDFsyn2(segment)
    synapse.tau_r = tau_r
    synapse.tau_d = tau_d
    synapse.gmax = gMax
    DefineSynapse_add_common(synapse)
    return synapse


def DefineSynapse_add_common(synapse, e=0):
    if e is not None:
        synapse.e = e
    synapse.Use = 1
    synapse.u0 = 0
    synapse.Dep = 0
    synapse.Fac = 0


def DefineSynapse_NMDA(segment, gMax=0.0004, tau_r_AMPA=0.3, tau_d_AMPA=3.0, tau_r_NMDA=2.0, tau_d_NMDA=70.0, is_prob=False):
    if is_prob:  # todo all my mod files lack gmax
        synapse = h.ProbAMPANMDA(segment)
        synapse.tau_r_AMPA = tau_r_AMPA
        synapse.tau_d_AMPA = tau_d_AMPA
        synapse.tau_r_NMDA = tau_r_NMDA
        synapse.tau_d_NMDA = tau_d_NMDA
        # synapse.gmax = gMax
        DefineSynapse_add_common(synapse)
        return synapse
    else:
        synapse_ampa = h.Exp2Syn(segment)
        synapse_ampa.tau1 = tau_r_AMPA
        synapse_ampa.tau2 = tau_d_AMPA
        # synapse_ampa.gmax = gMax
        synapse_nmda = h.NMDA(segment)
        synapse_nmda.tau_r_NMDA = tau_r_NMDA
        synapse_nmda.tau_d_NMDA = tau_d_NMDA
        # synapse_nmda.gmax = gMax
        synapse_nmda.e = 0
        synapse_ampa.e = 0
        return [synapse_ampa, synapse_nmda]


def add_synapse(segment, net_stim=None, synapse_w_ampa=1, synapse_w_nmda=1, ex_type="AMPA", params={'gMax': 0.0004},
                ampa_only=False):
    # define synapse and connect it to a segment
    if ex_type == 'AMPA':
        exSynapse = DefineSynapse_AMPA(segment, **params)
    elif ex_type == 'NMDA':
        exSynapse = DefineSynapse_NMDA(segment, **params)
    else:
        assert False, 'Not supported Excitatory Synapse Type'

    # connect synapse
    if not isinstance(exSynapse, list):
        netConnection = h.NetCon(net_stim, exSynapse)
        netConnection.delay = 0
        netConnection.weight[0] = max(synapse_w_ampa, synapse_w_nmda)
        return [exSynapse], netConnection
    net_cons = []
    for ex in exSynapse[0:1] if ampa_only else exSynapse:  # todo your code activate the NMDA as well. The trace is too long in this case I think
        net_cons.append(h.NetCon(net_stim, ex))
        net_cons[-1].delay = 0
        net_cons[-1].weight[0] = synapse_w_nmda if "nmda" in str(ex).lower() else synapse_w_ampa
    return exSynapse, net_cons


def get_impedance(x_seg, input_electrode_seg, freq_hz=0):
    imp = h.Impedance()
    imp.loc(input_electrode_seg.x, sec=input_electrode_seg.sec)  # location of input electrode (middle of section).
    imp.compute(freq_hz)
    return {"Rin": imp.input(input_electrode_seg.x, sec=input_electrode_seg.sec),
            "Rtr_M_ohm": imp.transfer(x_seg.x, sec=x_seg.sec)}


def get_segment_length_lamda(seg):
    seg_len = seg.sec.L/seg.sec.nseg  # micro meter
    R_total = 1.0 / seg.g_pas  #Rm[cm^2*oum] sce.Ra[cm*oum]
    lamda = np.sqrt((R_total / seg.sec.Ra) * (seg.diam / 10000.0) / 4.0)  # micro meter
    return (float(seg_len) / 10000.0) / lamda


def compute_distances(base_seg, stop_seg=None, dend_spine_x=None, is_print=False):  # from bottom up (this is the spine)
    sec_length = 0
    curr = base_seg.sec
    while curr.parentseg() is not None:  # run using parent (backwards) to make sure it's a single path
        curr = curr.parentseg().sec
        if curr == stop_seg.sec:  # if this sec is the stop one - only calc segment addition
            add_vals = [get_segment_length_lamda(seg) for seg in curr
                        if (seg.x < stop_seg.x if dend_spine_x is None else False)]
            sec_length += sum(add_vals)
            if is_print:
                print("Debug <compute_distances>: parent loop stopped at stop_seg and added ", add_vals)
            break
        sec_length += sum([get_segment_length_lamda(seg) for seg in curr])
        if is_print:
            print("Debug <compute_distances>: parent loop added ", [get_segment_length_lamda(seg) for seg in curr])

    if "spine" in str(base_seg.sec):
        add_vals = [get_segment_length_lamda(base_seg.sec(x)) for x in [0, 0.5, 1] if x < base_seg.x]
        sec_length += sum(add_vals)
        if is_print:
            print("Debug <compute_distances>: added spine ", base_seg.sec, add_vals)
    else:
        add_vals = [get_segment_length_lamda(seg) for seg in base_seg.sec if seg.x < base_seg.x]
        sec_length += sum(add_vals)
        if is_print:
            print("Debug <compute_distances>: added curr ", base_seg, add_vals)
    return sec_length


def get_distance(x_seg, input_electrode_seg, dend_spine_x=0.5, is_print=False):
    h.distance(0, x_seg.x, sec=x_seg.sec)
    return {"distance_um": h.distance(input_electrode_seg.x, sec=input_electrode_seg.sec),
            "distance_lambda": compute_distances(base_seg=input_electrode_seg, stop_seg=x_seg,
                                                 dend_spine_x=dend_spine_x, is_print=is_print)}


def record_all(stim, dend, spines, spines_psds, ampa_nmda_synapse,
               delay_ms=0, sim_time_ms=1000, dend_spine_x=0.5):
    t = h.Vector()
    t.record(h._ref_t)  # record time
    sim_na = np.array([])
    if stim is not None:
        sim_na = h.Vector()
        sim_na.record(stim._ref_amp)

    # Record voltage from all segments in the dendrite
    allSegments = np.concatenate([[seg for seg in sec] for sec in dend])  # define the order of matrix
    dend_distances = []
    dend_vs = []
    for seg in allSegments:
        dend_vs.append(h.Vector())
        dend_vs[-1].record(seg._ref_v)
        dend_distances.append(get_distance(x_seg=dend[0](0), dend_spine_x=None, input_electrode_seg=seg))
        dend_distances[-1]["name"] = f"{seg.sec}-{seg.x}"

    allSpines = np.concatenate([[sec(x) for x in [0, 0.5, 1]] for sec in spines + spines_psds])  # define the order of matrix
    spine_vs, spine_imp, spine_distances = [], [], []
    for seg in allSpines:
        spine_vs.append(h.Vector())
        spine_vs[-1].record(seg._ref_v)
        spine_imp.append(get_impedance(x_seg=dend[0](dend_spine_x), input_electrode_seg=seg, freq_hz=0))
        spine_imp[-1]["name"] = f"{seg.sec}-{seg.x}"
        spine_distances.append(get_distance(x_seg=dend[0](dend_spine_x), dend_spine_x=dend_spine_x, input_electrode_seg=seg))
        spine_distances[-1]["name"] = f"{seg.sec}-{seg.x}"

    spine_conductance_ampa, spine_conductance_nmda = [], []
    for seg in ampa_nmda_synapse:
        if "nmda" in str(seg).lower():
            spine_conductance_nmda.append(h.Vector())
            spine_conductance_nmda[-1].record(seg._ref_g_NMDA)
        else:
            spine_conductance_ampa.append(h.Vector())
            spine_conductance_ampa[-1].record(seg._ref_g)

    spine_names = [f"{seg.sec}-{seg.x}" for seg in allSpines]
    dendrite_names = [f"{seg.sec}-{seg.x}" for seg in allSegments]

    h.v_init = -70  # set starting voltage
    h.tstop = sim_time_ms  # set simulation time
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt
    h.run()

    dend_vs = np.array(dend_vs)[:, np.array(t) >= delay_ms]
    spine_vs = np.array(spine_vs)[:, np.array(t) >= delay_ms]
    spine_conductance_ampa = np.array(spine_conductance_ampa)[:, np.array(t) >= delay_ms]
    spine_conductance_nmda = np.array(spine_conductance_nmda)[:, np.array(t) >= delay_ms]
    print("debug v ", dend_vs.max(), dend_vs.min(), dend_vs.shape, t)
    if len(sim_na) > 0:
        print("debug ", sim_na.max(), sim_na.min(), sim_na.max())
        sim_na = np.array(sim_na)[np.array(t) >= delay_ms]

    t = np.array(t)[np.array(t) >= delay_ms]
    return allSegments, allSpines, dict(time=t, dendrite_v=dend_vs, dendrite_names=dendrite_names,
                                        spine_distances=spine_distances, dend_distances=dend_distances,
                                        stim_pulse_na=sim_na, spine_v=spine_vs, spine_names=spine_names,
                                        spine_conductance_ampa=spine_conductance_ampa,
                                        spine_conductance_nmda=spine_conductance_nmda)


def run_one_expr(dend_params_dict, params_spine, nmda_ampa_params, synapse_w_ampa, synapse_w_nmda, ampa_only=False, is_plot=False):
    params_dict = {}

    single_dend = create_multiple_dend(n_dend=1, **dend_params_dict)[0]
    single_dend.nseg = 4 # allow some length
    spines, spines_psds = add_spines(single_dend, syn_segs=[.5], **params_spine)  # put 1 spine in the middle (0.5)
    # spine has on i & i+1 the head/neck. PSD is different section so you can define this size
    ampa_synapse, netConnection = add_synapse(segment=spines_psds[0](0.5), net_stim=Stim1, ex_type="NMDA",
                                              synapse_w_ampa=synapse_w_ampa, synapse_w_nmda=synapse_w_nmda,
                                              params=nmda_ampa_params, ampa_only=ampa_only)
    allSegments, allSpines, result_dict = record_all(stim=None, dend=[single_dend], spines=spines, ampa_nmda_synapse=ampa_synapse,
                                                     spines_psds=spines_psds, dend_spine_x=0.5)

    params_dict.update(dend_params_dict)
    params_dict.update(params_spine)
    params_dict.update(nmda_ampa_params)
    params_dict.update(dict(synapse_w_nmda=synapse_w_nmda, synapse_w_ampa=synapse_w_ampa, ampa_only=ampa_only))

    if is_plot:
        plt.figure()
        plt.subplot(3, 1, 1)
        plt.plot(result_dict["time"], result_dict["dendrite_v"].T)
        plt.title("Dendritic voltage") ; plt.xlabel("Time (ms)")
        plt.legend(result_dict["dendrite_names"])
        plt.subplot(3, 1, 2)
        plt.plot(result_dict["time"], result_dict["spine_v"].T)
        plt.title("Spine voltage") ; plt.xlabel("Time (ms)")
        plt.legend([a for a in result_dict["spine_names"]], fontsize=8,
                   bbox_to_anchor=(.7, .5), loc='center left')
        plt.subplot(3, 1, 3)
        plt.plot(result_dict["time"], result_dict["spine_conductance_ampa"].T, label="AMPA")
        plt.plot(result_dict["time"], result_dict["spine_conductance_nmda"].T, label="NMDA")
        plt.title("Conductances") ; plt.xlabel("Time (ms)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    return {"results": result_dict, "parameters": params_dict}

from tqdm import tqdm
if __name__ == '__main__':
    model_path = "..\\Human_Gabor2021\\"
    if os.path.isfile(os.path.join(model_path, "nrnmech.dll")):
        h.nrn_load_dll(os.path.join(model_path, "nrnmech.dll"))
        print("Loaded ", model_path)

    Stim1 = h.NetStim()
    Stim1.interval = 10000
    Stim1.start = 100
    Stim1.noise = 0
    Stim1.number = 1

    # defaults
    def_dend_params_dict = dict(dend_ra=80, dend_rm=10000, debd_L_um=1000, dend_diam_um=1, dend_cm=1.75)
    def_params_spine = dict(SPINE_NECK_DIAM=0.13, SPINE_NECK_L=0.82, SPINE_PSD_AREA=0.07, HEAD_DIAM=0.47)
    def_nmda_ampa_params = dict(gMax=0.0004, tau_r_AMPA=0.2, tau_d_AMPA=1.5, tau_r_NMDA=10.0, tau_d_NMDA=80.0)

    all_results = {}
    for name, list_of_vals in tqdm(zip(["dend_ra", "dend_rm", "dend_cm", "dend_diam_um"],
                                  [np.arange(start=50, stop=150, step=10),
                                   np.arange(start=6000, stop=17000, step=1000),
                                   np.arange(start=0.9, stop=2.5, step=.1),
                                   np.arange(start=0.65, stop=1.2, step=.2)])):
        all_results[name] = []
        for val in list_of_vals:
            dend_params_dict = def_dend_params_dict.copy()
            dend_params_dict[name] = val
            all_results[name].append(run_one_expr(dend_params_dict=dend_params_dict.copy(),
                                                  params_spine=def_params_spine.copy(),
                                                  nmda_ampa_params=def_nmda_ampa_params.copy(),
                                                  synapse_w_ampa=1, synapse_w_nmda=1, is_plot=True, ampa_only=True))
    for name, list_of_vals in tqdm(zip(["SPINE_NECK_DIAM", "SPINE_NECK_L", "HEAD_DIAM", "SPINE_PSD_AREA"],
                                       [np.arange(start=0.09, stop=0.18, step=0.01),
                                        np.arange(start=0.21, stop=1.3, step=0.1),
                                        np.arange(start=0.3, stop=0.6, step=.05),
                                        np.arange(start=0.01, stop=0.15, step=.01)])):
        all_results[name] = []
        for val in list_of_vals:
            params_dict = def_params_spine.copy()
            params_dict[name] = val
            all_results[name].append(run_one_expr(dend_params_dict=def_dend_params_dict.copy(),
                                                  params_spine=params_dict.copy(),
                                                  nmda_ampa_params=def_nmda_ampa_params.copy(),
                                                  synapse_w_ampa=1, synapse_w_nmda=1))

    # synapse_w_ampa, synapse_w_nmda
    for name, list_of_vals in tqdm(zip(["tau_r_AMPA", "tau_d_AMPA", "tau_r_NMDA", "tau_d_NMDA", "synapse_w_nmda", "synapse_w_ampa"],
                                       [np.arange(start=0.1, stop=0.4, step=0.05),
                                        np.arange(start=1, stop=3, step=0.5),
                                        np.arange(start=3, stop=15, step=3),
                                        np.arange(start=25, stop=100, step=10),
                                        np.arange(start=1, stop=10, step=1),
                                        np.arange(start=1, stop=10, step=1)])):
        all_results[name] = []
        for val in list_of_vals:
            params_dict = def_nmda_ampa_params.copy()
            synapse_w_nmda, synapse_w_ampa = 1, 1
            if "synapse_w" not in name:
                params_dict[name] = val
            elif name == "synapse_w_ampa":
                synapse_w_ampa = val
            elif name == "synapse_w_nmda":
                synapse_w_nmda = val
            else:
                print(f"Error wrong name {name}")
            all_results[name].append(run_one_expr(dend_params_dict=def_dend_params_dict.copy(),
                                                  params_spine=def_params_spine.copy(),
                                                  nmda_ampa_params=params_dict.copy(),
                                                  synapse_w_nmda=synapse_w_nmda, synapse_w_ampa=synapse_w_ampa))
    pickle.dump(all_results, open("for_moria" + 'results_pickles.p', 'wb'))

    # see spine in shape plot as well to see spine
    print("")
    print("wait")

    # todo split wampa and 2nmda by adjusting weight?
    # todo print correlates for conductance and other params?
