from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
from glob import glob
import signal
import sys
from extra_function import load_ASC,load_hoc,load_swc,SIGSEGV_signal_arises,create_folder_dirr
from read_spine_properties import get_n_spinese,get_spine_xyz
from open_pickle import read_from_pickle
import pandas as pd
from calculate_F_factor import calculate_F_factor
import pandas as pd
from read_passive_parameters_csv import get_passive_parameter


do_calculate_F_factor=True
print("the number of parameters that sys loaded in Rin_Rm_plot.py is ",len(sys.argv),flush=True)
print(len(sys.argv), sys.argv)
if len(sys.argv) != 8:
    print("the function doesn't run with sys.argv",flush=True)
    cell_name= '2017_05_08_A_5-4'
    file_type2read='z_correct.swc'
    fit_condition='const_param'
    passive_val={'RA':100.0,'CM':1.0,'RM':10000.0}
    name='test'
    resize_diam_by=1.2
    shrinkage_factor=1.0
    SPINE_START=20
else:
    print("the sys.argv len is correct",flush=True)
    cell_name = sys.argv[1]
    file_type2read=sys.argv[2] #hoc ar ASC
    fit_condition=sys.argv[3]
    name=sys.argv[4]
    resize_diam_by = float(sys.argv[5]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[6]) #how much srinkage the cell get between electrophysiology record and LM
    SPINE_START=int(sys.argv[7])
    passive_val=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_factor,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type2read)[name]
folder_=''

print(name, passive_val)
print(name,passive_val)
data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
folder_data=folder_+save_dir+cell_name
cell_file = glob(folder_+data_dir+cell_name+"/*"+file_type2read)[0]
print("cell file is " +cell_file)
folder_save=folder_+save_dir+cell_name+"/data/cell_properties/"+file_type2read+'/SPINE_START='+str(SPINE_START)+'/'
folder_save+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
folder_save+='/'+name+'/Rin_Rm/'
create_folder_dirr(folder_save)
parameters=read_from_pickle(folder_data+'/data/electrophysio_records/short_pulse_parameters.p')
def change_model_pas(CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0, F_factor ={}):
    #input the neuron property
    h.dt = 0.1
    h.distance(0,0.5, sec=soma)
    for sec in cell.all_sec(): ##check if we need to insert Ra,cm,g_pas,e_pas to the dendrit or just to the soma
        sec.Ra = RA
        sec.cm = CM
        sec.g_pas = 1.0 / RM
        sec.e_pas = E_PAS
    for sec in cell.dend:
        for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
            # how many segment have diffrent space larger then SPINE_START that decided
            if h.distance(seg) > SPINE_START:
                seg.cm *= F_factor
                seg.g_pas *= F_factor


signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
######################################################
# build the model
######################################################
cell=None
if file_type2read=='ASC':
    cell=load_ASC(cell_file)
elif file_type2read=='hoc':
    cell=load_hoc(cell_file)
elif 'swc' in file_type2read:
    cell=load_swc(cell_file)


#     for sec in cell.axon:
#         h.delete_section(sec=sec)
#     print("cell.axons is deleted")

soma= cell.soma
for sec in cell.all_sec():
    if sec == cell.soma: continue
    sec.diam = sec.diam*resize_diam_by

if do_calculate_F_factor:
    F_factor=calculate_F_factor(cell,"mouse_spine",file_type2read,folder_+data_dir)
else:
    F_factorF_factor=1.9
#insert pas to all other section
h.celsius = 30
CM=passive_val['CM']
RM=passive_val['RM']
RA=passive_val['RA']
E_pas=parameters['E_pas']
for sec in cell.all_sec():
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances

change_model_pas(CM=CM, RA = RA, RM =RM, E_PAS = E_pas,F_factor= F_factor)
imp = h.Impedance(sec=soma)
imp.loc(0.5, sec=soma)
add_figure('Rin to Rm for diffrent Ra'+'\n'+name+' '+str(passive_val),'Rm [Ohm/cm^2]','Rin [M ohm]')
Rm_arr = np.hstack([np.arange(10, 2511, 100), np.arange(2510, 20011, 1000)])
for Ra in [1e-9, 70, 100, 150, 200]:
    res = []
    for Rm in Rm_arr:
        change_model_pas(CM=CM, RA=Ra, RM=Rm, E_PAS=E_pas,F_factor= F_factor)
        imp.compute(0)
        res.append(imp.input(0.5, sec=soma))
    plt.plot(Rm_arr, res, label='Ra='+str(Ra)+'[Ohm*cm]')
plt.axhline(89.1, color='k', linestyle='--',label='Rin=89.1[Mohm]')
# plt.axhline(73.705, color='k', linestyle='--',label='Rin=73.705[Mohm]')
plt.xlabel('Rm (ohm/cm**2)')
plt.ylabel('Rin (M ohm)')
plt.legend()
plt.savefig(folder_save+'/Rin_Rm')
freqs=np.linspace(0,200,num=100)
dict_syn=pd.read_excel(folder_+save_dir+"synaptic_location_seperate.xlsx",index_col=0)
# for spine_sec,spine_seg in zip(spines_sec,spines_seg):
for spine_num in range(get_n_spinese(cell_name)):
    spine_seg=dict_syn[cell_name+str(spine_num)]['seg_num']
    spine_sec=eval('cell.'+dict_syn[cell_name+str(spine_num)]['sec_name'])
    spine_xyz=get_spine_xyz(cell_name,spine_num=spine_num)
    Rin_syn=[]
    change_model_pas(CM=CM, RA = RA, RM =RM, E_PAS = E_pas,F_factor= F_factor) #moria need to change for good passive value
    for freq in freqs:
        imp_0 = h.Impedance(sec=spine_sec)
        imp_0.loc(spine_seg, sec=spine_sec)
        imp_0.compute(freq)  # check if you need at 10 Hz
        Rin_syn.append( imp_0.input(spine_seg, sec=spine_sec))
    add_figure('Rin to freq'+'\n'+name+' '+str(passive_val),'freq [hz]','Rinput [M ohm]')
    plt.plot(freqs,Rin_syn)
    imp_0.compute(100)
    plt.plot(100,   imp_0.input(spine_seg, sec=spine_sec)  ,'*')
    plt.legend(['Rin2freq',str([10,   round(imp_0.input(spine_seg, sec=spine_sec),2)])])
    plt.savefig(folder_save+'/Rin_freq for spinenum '+str(spine_num))
    Rin,dis=[],[]
    freq=100
    h.distance(0,0.5, sec=soma)

    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS=E_pas,F_factor= F_factor)
    # change_model_pas(CM=1.88, RA=98, RM=12371, E_PAS=-77.3,F_factor= F_factor)

    for sec in cell.all_sec():
        imp_0 = h.Impedance(sec=spine_sec)
        seg_len=sec.L / 15
        imp_0.loc(0.5, sec=soma)
        imp_0.compute(freq)  # check if you need at 10 Hz
        for seg in 1/15*np.arange(15):
            # imp_0.transfer(sec(seg))
            # imp_0.input(seg, sec=sec)
            Rin.append( imp_0.transfer(spine_sec(spine_seg)))
            dis.append(h.distance(spine_sec(spine_seg)))
    add_figure('transfer impadence at freq '+str(freq)+'Hz'+'\n'+name+' '+str(passive_val),'ditance form soma [micron]','transfer_resistance[ohm]' )
    plt.plot(dis,Rin,'.')
    dis_syn=h.distance(spine_sec(spine_seg))
    Rin_syn=imp_0.transfer(spine_sec(spine_seg))
    plt.plot( dis_syn,Rin_syn ,'*',label=[round(dis_syn,2),round(Rin_syn,2)])
    plt.text(0,0,'Cm,Ra,Rm=[2,70,5684]')
    plt.legend()
    plt.savefig(folder_save+'/transfer resistance for spinemum '+str(spine_num))

print('Rin_Rm.py is complite to run for '+cell_name)


