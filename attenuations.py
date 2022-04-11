from neuron import h, gui
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import signal
from extra_function import SIGSEGV_signal_arises,load_ASC,load_hoc,load_swc,create_folder_dirr
import pandas as pd
from calculate_F_factor import calculate_F_factor
import sys
from read_spine_properties import get_n_spinese,get_building_spine
import json
from open_pickle import read_from_pickle
from read_passive_parameters_csv import get_passive_parameter
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

freq=100
do_calculate_F_factor=True
put_syn_on_spine_head=True
norm_Rin=False
syn_injection=True
clamp_injection=False

print("the number of parameters that sys loaded in attenuation.py is ",len(sys.argv),flush=True)
print(len(sys.argv), sys.argv)
do_resize_dend=True
if len(sys.argv) != 9:
    print("the function doesn't run with sys.argv",flush=True)
    cell_name= '2017_05_08_A_5-4'
    file_type='z_correct.swc'
    fit_condition='const_param'
    passive_val={'RA':100.0,'CM':1.0,'RM':10000.0}
    name='test'
    syn_injection=False
    resize_diam_by=1.2
    shrinkage_factor=1.0
    SPINE_START=20
else:
    print("the sys.argv len is correct",flush=True)
    cell_name = sys.argv[1]
    file_type=sys.argv[2] #hoc ar ASC
    fit_condition=sys.argv[3]
    name=sys.argv[4]
    syn_injection=eval(sys.argv[5])
    resize_diam_by = float(sys.argv[6]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[7]) #how much srinkage the cell get between electrophysiology record and LM
    SPINE_START=int(sys.argv[8])
    passive_val=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_factor,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type)[name]
folder_=''

if not syn_injection:
    clamp_injection=True

print(name, passive_val)

data_dir= "cells_initial_information/"
save_dir = "cells_outputs_data_short/"
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]
folder_save=folder_+save_dir+cell_name+"/data/cell_properties/"+file_type+'/SPINE_START='+str(SPINE_START)+'/'
folder_save+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
folder_save+='/'+name+'/'
folder_save+="attenuations/"
create_folder_dirr(folder_save)

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

def plot_records(RM, RA, CM,cell, syns,spines=None,save_name= "lambda"):
    change_model_pas(cell ,CM=CM, RA=RA, RM=RM, E_PAS = E_PAS,F_factor=F_factor)
    Vvec_soma = h.Vector()
    Vvec_soma.record(soma(0.5)._ref_v)
    Tvec = h.Vector()
    Tvec.record(h._ref_t)

    Vvec_dend,Vvec_spine,Ivec=[],[],[]
    for i,syn in enumerate(syns):
        Vvec_dend.append(h.Vector())
        Vvec_dend[i].record(syn[0](syn[1])._ref_v)

    for i,spine in enumerate(spines):
        Vvec_spine.append(h.Vector())
        if clamp_injection:
            Ivec.append(h.Vector())
            Ivec[i].record(clamp[i]._ref_i)
            if spines!=None:
                Vvec_spine[i].record(spine(1)._ref_v)

        if syn_injection:
            if spines!=None:
                Vvec_spine[i].record(spine(1)._ref_v)
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
    if norm_Rin: ##check for the rigth norming
        npIvec/=Rin_syn_resize_dend #npIvec*(Rin_syn_0/Rin_syn_resize_dend)
        # npVec_dend=npVec_dend*(Rin_dend_0/Rin_dend_resize_dend)#/=Rin_dend_resize_dend #npVec_dend*(Rin_dend_0/Rin_dend_resize_dend)
        # npVec_soma=npVec_soma*(Rin_soma_0/Rin_soma_resize_dend)#/=Rin_soma_resize_dend#npVec_soma*(Rin_soma_0/Rin_soma_resize_dend)
    figure, axis = plt.subplots(3, len(spines))
    if len(spines) == 1:
        axis = axis[..., np.newaxis]
    print("Before plot: ", len(spines), axis.shape)
    plt.suptitle(cell_name+'\n'+name+' '+str(passive_val)+'\ndend*'+str(resize_diam_by)+' shrinkage_factor='+str(shrinkage_factor))
    for i in range(len(spines)):
        axis[0,i].plot(npTvec,npIvec[i])
        # axis[0,i].set_title("spine voltage")
        axis[0,i].set_xlabel('mS')
        axis[0,i].set_ylabel('ms')
        if clamp_injection:
            axis[0,i].set_title("\n current injection of " + str(clamp[i].amp) + "nA\nsyn"+str(i)+" for " + str(pulse_size) + 'ms')
            figure.tight_layout(pad=1.0)
        elif syn_injection:
            axis[0,i].set_title("syn"+str(i)+" weight=" + str(syn_weight) + '\nspine head Volt/Rinput')
            figure.tight_layout(pad=1.0)
            if not norm_Rin:
                axis[0,i].set_title("syn"+str(i)+" weight=" + str(syn_weight) + '\nspine head Voltage')
                axis[0,i].set_ylabel('mv')

        axis[1,i].plot(npTvec, npVec_dend[i])
        axis[1,i].set_title(sec.name().split('.')[-1]+str(spines_seg[i])+" voltage")
        axis[1,i].set_xlabel('mS')
        axis[1,i].set_ylabel('mV')

        axis[2,0].plot(npTvec, npVec_soma)
        axis[2,0].set_title("soma Voltage")
        axis[2,0].set_xlabel('mS')
        axis[2,0].set_ylabel('mv')
    if clamp_injection:
        # folder_save2=create_folder_dirr(folder_save+'/clamp_inj_freq_'+str(freq)+'/')
        plt.savefig(folder_save+'/clamp_inj_freq_'+str(freq)+'_for_' + str(pulse_size) + "ms_dend*"+str(resize_diam_by)+'.png')
        plt.savefig(folder_save+'/clamp_inj_freq_'+str(freq)+'_for_' + str(pulse_size) + "ms_dend*"+str(resize_diam_by)+'.pdf')

    elif syn_injection:
        # folder_save2=create_folder_dirr(folder_save+'/syn_injection')
        plt.savefig(folder_save+'/syn_injection_weight='+str(syn_weight)+"_dend*"+str(resize_diam_by)+".png")
        plt.savefig(folder_save+'/syn_injection_weight='+str(syn_weight)+"_dend*"+str(resize_diam_by)+".pdf")

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
cell=None
if file_type=='ASC':
    cell =load_ASC(cell_file)
elif file_type=='hoc':
    cell =load_hoc(cell_file)
elif 'swc' in file_type:
    cell =load_swc(cell_file)
if do_calculate_F_factor:
   F_factor=calculate_F_factor(cell,'mouse_spine')
else:
   F_factor = 1.9

# for sec in cell.axon:
#     h.delete_section(sec=sec)
#     does_axon_inside_cell=False
soma = cell.soma
# h.celsius = 36
sp = h.PlotShape()

#get spines prameters and creat spine:
dict_syn=pd.read_excel(folder_+save_dir+"synaptic_location_seperate.xlsx",index_col=0)
syns,spines,spines_sec,spines_seg,spines_head=[],[],[],[],[]
number_of_spine= get_n_spinese(cell_name)
for spine_num in range(number_of_spine):
    spine_seg=dict_syn[cell_name+str(spine_num)]['seg_num']
    spine_sec=eval('cell.'+dict_syn[cell_name+str(spine_num)]['sec_name'])
    syns.append([spine_sec,spine_seg])
    spines_sec.append(spine_sec)
    spines_seg.append(spine_seg)
    spines_property=get_building_spine(cell_name,spine_num)
    cell,[spine_neck, spine_head]=add_morph(cell, [spine_sec,spine_seg] ,get_building_spine(cell_name,spine_num),number=spine_num)
    spines.append([spine_neck, spine_head])
    spines_head.append(spine_head)
    sp.show(0)  # show diameters
    sp.color(2, sec=spine_sec )
for sec in cell.all_sec():
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
sp = h.PlotShape()
#creat stimulus
clamp=[]
syn_shape=[]
Rin_dend,Rin_syn=[],[]
netcon=[]
for i,spine_head in enumerate(spines_head):
    if clamp_injection:
        pulse_size=200
        clamp.append(h.IClamp(spine_head(1))) # insert clamp(constant potentientiol) at the soma's center
        clamp[i].amp = -0.05 #nA
        clamp[i].delay = 100 #ms
        clamp[i].dur = pulse_size  # ms
        h.tstop = 500

    elif syn_injection: #@# replace in my specipic synapse
        syn_shape.append(h.Exp2Syn(spine_head(1)))
        # if put_syn_on_spine_head:
        #     syn_shape.append(h.Exp2Syn(spine_head(1)))
        # else:
        #     syn_shape.append(h.Exp2Syn(spine_sec(spine_seg))
        syn_shape[i].tau1 = 0.3
        syn_shape[i].tau2 = 1.8
        syn_shape[i].e = 0
        # syn_shape.i=0
        # syn_shape.onset=200
        # syn_shape.imax=0.5
        syn_netstim = h.NetStim()  # the location of the NetStim does not matter
        syn_netstim.number = 1
        syn_netstim.start = 200
        syn_netstim.noise = 0
        netcon.append(h.NetCon(syn_netstim, syn_shape[i]))
        syn_weight = 0.002
        netcon[i].weight[0] = syn_weight  # activate the on_path synapse
        h.tstop = 500

    imp=h.Impedance(sec=spine_head)
    imp.loc(1, sec=spine_head)
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_syn.append(imp.input(1, spine_head))

    imp=h.Impedance(sec=spines_sec[i])
    imp.loc(spines_seg[i], sec=spines_sec[i])
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_dend.append(imp.input(spines_seg[i], sec=spines_sec[i]))

imp = h.Impedance(sec=soma)
imp.loc(0.5, sec=soma)
imp.compute(freq)  # check if you need at 10 Hz
Rin_soma_0 = imp.input(0.5, sec=soma)

for sec in cell.dend:
    sec.diam = sec.diam*resize_diam_by
if norm_Rin:
    Rin_syn_resize_dend,Rin_dend_resize_dend=[],[]
    for i,spine_head in enumerate(spines_head):
        imp=h.Impedance(sec=spine_head)
        imp.loc(1, sec=spine_head)
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_syn_resize_dend.append( imp.input(1, spine_head))

        imp=h.Impedance(sec=spines_sec[i])
        imp.loc(spines_seg[i], sec=spines_sec[i])
        imp.compute(freq)  # check if you need at 10 Hz
        Rin_dend_resize_dend.append(imp.input(spines_seg[i], sec=spines_sec[i]))

    imp = h.Impedance(sec=soma)
    imp.loc(0.5, sec=soma)
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_soma_resize_dend = imp.input(0.5, sec=soma)
E_PAS=read_from_pickle(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')['E_pas']
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

    plot_records(RM, RA, CM,cell,syns, spines=spines_head,save_name= "lambda for syn "+str(i))
else:
    plot_records(RM, RA, CM,cell,syns,save_name= "lambda for syn "+str(i))
print( 'attenuation is run in diraction'+folder_save)

a=1
