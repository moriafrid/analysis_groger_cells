from neuron import h, gui
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import signal
from extra_function import SIGSEGV_signal_arises,load_ASC,load_hoc,create_folder_dirr
import pandas as pd
from read_spine_properties import get_n_spinese
from calculate_F_factor import calculate_F_factor
import sys
freq=100
SPINE_START=60
do_calculate_F_factor=True
put_syn_on_spine_head=True
norm_Rin=False
syn_injection=True
clamp_injection=False
if not syn_injection:
    clamp_injection=True

do_resize_dend=True
if len(sys.argv) != 7:
    cell_name= '2017_05_08_A_5-4'
    file_type='hoc'
    passive_val={'RA':100,'RM':10000,'CM':1}
    syn_injection=True
    resize_diam_by=1.0
    shrinkage_factor=1.0
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
    cell_name = sys.argv[1]
    file_type=sys.argv[2] #hoc ar ASC
    passive_val=sys.argv[3]
    syn_injection=bool(sys.argv[4])
    resize_diam_by = float(sys.argv[5]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[6]) #how much srinkage the cell get between electrophysiology record and LM
    folder_= sys.argv[7] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]
folder_save=folder_+save_dir+cell_name+"/data/cell_properties/attenuations/"



signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
def change_model_pas(cell,CM = 1, RA = 250, RM = 20000.0, E_PAS = -70.0,F_factor=1.9):
   h.dt = 0.1
   h.distance(0,0.5, sec=soma)
   for sec in cell.all_sec():
       sec.Ra = RA
       sec.cm = CM  # *shrinkage_factor    #*(1.0/0.7)
       sec.g_pas = (1.0 / RM)  #*shrinkage_factor  #*(1.0/0.7)
       sec.e_pas = E_PAS
   for sec in cell.dend:
       for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
           if h.distance(seg) > SPINE_START:
               seg.cm *= F_factor
               seg.g_pas *= F_factor

def plot_records(RM, RA, CM,cell, syn,spine=None,save_name= "lambda"):
    change_model_pas(cell ,CM=CM, RA=RA, RM=RM, E_PAS = E_PAS,F_factor=F_factor)
    Vvec_soma = h.Vector()
    Vvec_soma.record(soma(0.5)._ref_v)

    Vvec_dend = h.Vector()
    Vvec_dend.record(syn[0](syn[1])._ref_v)
    Vvec_spine = h.Vector()

    Tvec = h.Vector()
    Tvec.record(h._ref_t)

    if clamp_injection:
        Ivec = h.Vector()
        Ivec.record(clamp._ref_i)
        if spine!=None:
            Vvec_spine.record(spine(1)._ref_v)


    if syn_injection:
        if spine!=None:
            Vvec_spine.record(spine(1)._ref_v)
            Ivec=Vvec_spine
        else:
            h.run()
            Ivec=range(len(Tvec))
        # Ivec.record(netcon._ref_i)
    h.run()
    npTvec = np.array(Tvec)
    npIvec = np.array(Ivec)
    npVec_soma = np.array(Vvec_soma)
    npVec_dend = np.array(Vvec_dend)
    if norm_Rin:
        npIvec/=Rin_syn_resize_dend #npIvec*(Rin_syn_0/Rin_syn_resize_dend)
        # npVec_dend=npVec_dend*(Rin_dend_0/Rin_dend_resize_dend)#/=Rin_dend_resize_dend #npVec_dend*(Rin_dend_0/Rin_dend_resize_dend)
        # npVec_soma=npVec_soma*(Rin_soma_0/Rin_soma_resize_dend)#/=Rin_soma_resize_dend#npVec_soma*(Rin_soma_0/Rin_soma_resize_dend)
    figure, axis = plt.subplots(3, 1)
    plt.suptitle(cell_name+'\nsyn'+str(i))
    axis[0].plot(npTvec,npIvec)
    # axis[0].set_title("spine voltage")
    axis[0].set_xlabel('mS')
    axis[0].set_ylabel('ms')

    axis[1].plot(npTvec, npVec_dend)
    axis[1].set_title("dend parent spine voltage")
    axis[1].set_xlabel('mS')
    axis[1].set_ylabel('mV')

    axis[2].plot(npTvec, npVec_soma)
    axis[2].set_title("soma Voltage")
    axis[2].set_xlabel('mS')
    axis[2].set_ylabel('mv')
    if clamp_injection:

        axis[0].set_title("\n current injection of " + str(clamp.amp) + "nA to the syn for " + str(pulse_size) + 'ms')
        figure.tight_layout(pad=1.0)
        folder_save2=create_folder_dirr(folder_save+'/syn'+str(i)+'/clamp_inj_freq_'+str(freq)+'/')
        plt.savefig(folder_save2+'/' + str(pulse_size) + "ms_dend*"+str(resize_diam_by)+'.png')

    elif syn_injection:
        axis[0].set_title("syn weight=" + str(syn_weight) + '\nspine head Volt/Rinput')
        figure.tight_layout(pad=1.0)
        if not norm_Rin:
            axis[0].set_title("syn weight=" + str(syn_weight) + '\nspine head Voltage')
            axis[0].set_ylabel('mv')
        folder_save2=create_folder_dirr(folder_save+'/syn'+str(i)+'/syn_injection')
        plt.savefig(folder_save2+'/weight='+str(syn_weight)+"_dend*"+str(resize_diam_by)+".png")
    plt.show()



def create_spine( icell, sec, seg, number=0, neck_diam=0.25, neck_length=1.35,head_diam=0.944):
    neck = h.Section(name="spineNeck" + str(number))
    head = h.Section(name="spineHead" + str(number))
    neck.L = neck_length
    neck.diam = neck_diam
    head.diam = head_diam
    head.L = head_diam
    head.connect(neck(1))
    neck.connect(sec(seg))
    h("access " + str(neck.hoc_internal_name()))
    icell.add_sec(neck)
    # icell.dend.append(neck)

    # if Rneck == "normal_neck":
    #     icell.all.append(neck)
    #     if sec.name().find('dend') > -1:
    #         icell.basal.append(neck)
    #     else:
    #         icell.apical.append(neck)
    h.pop_section() #?# moria understand if and why this is important
    h("access " + str(head.hoc_internal_name()))
    icell.add_sec(head)
    # icell.dend.append(head)

    # if sec.name().find('dend') > -1:
    #     icell.basal.append(head)
    # else:
    #     icell.apical.append(head)
    # sim.neuron.h.pop_section()
    h.pop_section()

    for sec in [neck, head]:
        sec.insert("pas")
    neck.g_pas = 1.0 / passive_val["RM"]
    neck.cm= passive_val["CM"]
    neck.Ra=passive_val["RA"]#int(Rneck)
    return icell,[neck, head]

def add_morph(cell, syn,spine_property,number=0):
    # sim.neuron.h.execute('create spineNeck['+str(len(syns))+']', icell)
    # sim.neuron.h.execute('create spineHead['+str(len(syns))+']', icell)
    cell,spine=create_spine(cell, syn[0],syn[1] ,number=number, neck_diam=spine_property['NECK_DIAM'], neck_length=spine_property['NECK_LENGHT'],head_diam=spine_property['HEAD_DIAM'])
    return cell,spine
    # num = syn[0]
        # num = int(num[num.find("[") + 1:num.find("]")])
        # if syn[0].find("dend") > -1:
        #     sec = cell.dend[num]
        # elif syn[0].find("apic") > -1:
        #     sec = cell.apic[num]
        # else:
        #     sec = cell.soma[0]
        # all.append(create_spine(cell, sec, syn[0],syn[1] ,number=i, neck_diam=spine_property[str(i)]['NECK_DIAM']), neck_length=spine_property[str(i)]['NECK_LENGHT'],
        #                         head_diam=spine_property[str(i)]['HEAD_DIAM'])
    # return all
# cell=instantiate_swc('/ems/elsc-labs/segev-i/moria.fridman/project/data_analysis_git/data_analysis/try1.swc')
cell=None
if file_type=='ASC':
   cell =load_ASC(cell_file)
elif file_type=='hoc':
   cell =load_hoc(cell_file)
if do_calculate_F_factor:
   F_factor=calculate_F_factor(cell,'mouse_spine')
else:
   F_factor = 1.9

# for sec in cell.axon:
#     h.delete_section(sec=sec)
#     does_axon_inside_cell=False
soma = cell.soma
# h.celsius = 36

# from find_synaptic_loc import synaptic_loc
# syn_poses={}
# syn_poses['05_08_A_01062017']=[(-5.56, -325.88, -451.42)]
# syns = synaptic_loc(cell,syn_poses[cell_name],del_axon=False)['place_as_sec']


dict_syn=pd.read_excel(folder_+save_dir+"synaptic_location_seperate.xlsx",index_col=0)
syns=[]
for sec in cell.all_sec():
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances

    # if sec.name() in [name for (name, seg) in dict_syn[cell_name]['place_name']]:
    #     seg = [seg for (name, seg) in dict_syn[cell_name][0]['place_name'] if sec.name() == name][0]  # get seg num - todo should be syn[1]
    #     syns.append(sec)
for spine_num in range(get_n_spinese(cell_name)):
   spine_seg=dict_syn[cell_name+str(spine_num)]['seg_num']
   spine_sec=eval('cell.'+dict_syn[cell_name+str(spine_num)]['sec_name'])
   syns.append([spine_sec,spine_seg])

# if resize_diam_by!=1.0:
#     imp_0 = h.Impedance(sec=syn[0])
#     imp_0.loc(0.165, sec=syn[0])
#     imp_0.compute(0)  # check if you need at 10 Hz
#     Rin_syn_0 = imp_0.input(syn[1], sec=syn[0])
# # for sec in cell.dend:
# #     sec.diam = sec.diam*resize_diam_by
# if norm_Rin:
#     imp=h.Impedance(sec=syn[0])
#     imp.loc(syn[1], sec=syn[0])
#     imp.compute(0) #check if you need at 10 Hz
#     Rin_syn_resize_dend = imp.input(syn[1], sec=syn[0])
#@# I need to think on a way to do it more clever

from read_spine_properties import get_n_spinese,get_building_spine
number_of_spine= get_n_spinese(cell_name)
spines=[]
for i in range(number_of_spine):
    spines_property={i:get_building_spine(cell_name,i)}
    spine_seg=dict_syn[cell_name+str(spine_num)]['seg_num']
    spine_sec=eval('cell.'+dict_syn[cell_name+str(spine_num)]['sec_name'])
    cell,[spine_neck, spine_head]=add_morph(cell, [spine_sec,spine_seg] ,spines_property[i],number=i)
    if put_syn_on_spine_head:
        spines.append([spine_neck, spine_head])
    sp = h.PlotShape()
    sp.show(0)  # show diameters
    sp.color(2, sec=spine_sec )
    if clamp_injection:
        pulse_size=1000
        clamp = h.IClamp(spine_head(1)) # insert clamp(constant potentientiol) at the soma's center
        clamp.amp = 0.05 #nA
        clamp.delay = 200 #ms
        clamp.dur = pulse_size  # ms
        h.tstop = 500

    elif syn_injection: #@# replace in my specipic synapse
        # create excitatory synapse at knowen head spine
        spines=[]
        syn_shape=[]
        if put_syn_on_spine_head:
            syn_shape = h.Exp2Syn(spine_head(1))
        else:
            syn_shape=h.Exp2Syn(spine_sec(spine_seg))
        syn_shape.tau1 = 0.3
        syn_shape.tau2 = 1.8
        syn_shape.e = 0
        # syn_shape.i=0
        # syn_shape.onset=200
        # syn_shape.imax=0.5
        syn_netstim = h.NetStim()  # the location of the NetStim does not matter
        syn_netstim.number = 1
        syn_netstim.start = 200
        syn_netstim.noise = 0
        netcon = h.NetCon(syn_netstim, syn_shape)
        syn_weight = 0.002
        netcon.weight[0] = syn_weight  # activate the on_path synapse
        # create a NetStim that will activate the synapses at t=1000
        h.tstop = 1000

        ####### if there is more then 1 synapse
        # syn_shape=[]
        # for i, syn in enumerate(syns):
        #     syn_shape.append(h.Exp2Syn(syn[0](syn[1])))
        #     syn_shape[i].tau1 = 0.3
        #     syn_shape[i].tau2 = 1.8
        #     syn_shape[i].e = 0
        #
        #     # syn_shape.i=0
        #     # syn_shape.onset=200
        #     # syn_shape.imax=0.5
        #     syn_netstim = h.NetStim()  # the location of the NetStim does not matter
        #     syn_netstim.number = 1
        #     syn_netstim.start = 200
        #     syn_netstim.noise = 0
        #     netcon = h.NetCon(syn_netstim, syn_shape[i])
        #     syn_weight = 0.003
        #     netcon.weight[i] = syn_weight  # activate the on_path synapse
        #     # create a NetStim that will activate the synapses  at t=1000
        #
        # # syn_weight=0.003
        # # netcon.weight = syn_weight  # activate the on_path synapse
        # # h.tstop = 1000
    if resize_diam_by!=1.0:
        imp = h.Impedance(sec=spine_head)
        imp.loc(1, sec=spine_head)
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_syn_0 = imp.input(1, spine_head)

        imp = h.Impedance(sec=spine_sec)
        imp.loc(spine_seg, sec=spine_sec)
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_dend_0 = imp.input(sec, sec=spine_seg)

        imp = h.Impedance(sec=soma)
        imp.loc(0.5, sec=soma)
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_soma_0 = imp.input(0.5, sec=soma)

        for sec in cell.dend:
            sec.diam = sec.diam*resize_diam_by
    if norm_Rin:
        syn=syns[0]
        imp=h.Impedance(sec=spine_head)
        imp.loc(1, sec=spine_head)
        imp.compute(freq) #check if you need at 10 Hz
        Rin_syn_resize_dend = imp.input(1, sec=spine_head)

        imp=h.Impedance(sec=spine_sec)
        imp.loc(spine_seg, sec=spine_sec)
        imp.compute(freq) #check if you need at 10 Hz
        Rin_dend_resize_dend = imp.input(spine_seg, sec=spine_sec)

        imp = h.Impedance(sec=soma)
        imp.loc(0.5, sec=soma)
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_soma_resize_dend = imp.input(0.5, sec=soma)
    E_PAS=-77.5

    h.v_init=E_PAS
    h.dt = 0.1 #=hz
    h.steps_per_ms = h.dt

    RM_const = 60000.0
    RA_const = 250.0
    CM_const = 1.0

    CM=passive_val['CM']
    RM=passive_val['RM'] #20000 #5684*2
    RA=passive_val['RA']
    if put_syn_on_spine_head:
        plot_records(RM, RA, CM,cell,[spine_sec,spine_seg], spine=spine_head,save_name= "lambda for syn "+str(i))
    else:
        plot_records(RM, RA, CM,cell,[spine_sec,spine_seg],save_name= "lambda for syn "+str(i))


a=1
