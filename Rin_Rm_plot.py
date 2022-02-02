import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
import os
from tqdm import tqdm
from add_figure import add_figure
import quantities as pq
from glob import glob
from calculate_F_factor import calculate_F_factor
import signal
import sys
from extra_function import mkcell,SIGSEGV_signal_arises
from spinse_class import SpinesParams

SPINE_START = 60
resize_diam_by=1
CM=2#2/2
RM=5684*2#*2
RA=70
do_calculate_F_factor=True

if len(sys.argv) != 5:
    cell_name= '2017_05_08_A_4-5'
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir= "cells_initial_information"
    save_dir ="cells_outputs_data"
else:
    cell_name = sys.argv[1]
    folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir = sys.argv[3] #cells_initial_information
    save_dir =sys.argv[4] #cells_outputs_data


spine=SpinesParams(cell_name)

#F_factor is the correction from the spine A(spine area)/area(without spine)
# F_factor = {} - take the F_factor for the specific segment
def change_model_pas(CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0, F_factor = 1.9):
    #input the neuron property    h.dt = 0.1

    h.distance(0,0.5, sec=soma) # it isn't good beacause it change the synapse distance to the soma
    #h.distance(0, sec=soma)
    for sec in cell.all: ##check if we need to insert Ra,cm,g_pas,e_pas to the dendrit or just to the soma
        sec.Ra = RA
        sec.cm = CM
        sec.g_pas = 1.0 / RM
        sec.e_pas = E_PAS
    for sec in cell.dend:
        for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
            # how many segment have diffrent space larger then SPINE_START that decided
            if h.distance(seg) > SPINE_START:
                if do_calculate_F_factor:
                    F_factor=spine.calculate_F_factor(folder_)
                seg.cm *= F_factor
                seg.g_pas *= F_factor


signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
######################################################
# build the model
######################################################

fname = "05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Bluecell_spinec91.ASC"
# cell=instantiate_swc('/ems/elsc-labs/segev-i/moria.fridman/project/data_analysis_git/data_analysis/try1.swc')
cell =mkcell(data_folder+cell_name+)

## delete all the axons
for sec in cell.axon:
   h.delete_section(sec=sec)

soma= cell.soma[0]

for sec in h.allsec():
    if sec == cell.soma[0]: continue
    sec.diam = sec.diam*resize_diam_by

#insert pas to all other section
h.celsius = 30

for sec in tqdm(h.allsec()):
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
change_model_pas(CM=CM, RA = RA, RM =RM, E_PAS = -77.3)
imp = h.Impedance(sec=soma)
imp.loc(0.5, sec=soma)
add_figure('Rin to Rm for diffrent Ra','Rm [Ohm/cm^2]','Rin [M ohm]')
Rm_arr = np.hstack([np.arange(10, 2511, 100), np.arange(2510, 20011, 1000)])
for Ra in [1e-9, 70, 100, 150, 200]:
    res = []
    for Rm in Rm_arr:
        change_model_pas(CM=CM, RA=Ra, RM=Rm, E_PAS=-77.3)
        imp.compute(0)
        res.append(imp.input(0.5, sec=soma))
    plt.plot(Rm_arr, res, label='Ra='+str(Ra)+'[Ohm*cm]')
plt.axhline(89.1, color='k', linestyle='--',label='Rin=89.1[Mohm]')
# plt.axhline(73.705, color='k', linestyle='--',label='Rin=73.705[Mohm]')
plt.xlabel('Rm (ohm/cm**2)')
plt.ylabel('Rin (M ohm)')
plt.legend()
plt.savefig('data/Rin_Rm')
plt.show()
freqs=np.linspace(0,200,num=100)
Rin_syn=[]
change_model_pas(CM=1.88, RA=95, RM=12392, E_PAS=-77.3)
for freq in freqs:
    imp_0 = h.Impedance(sec=cell.dend[82])
    imp_0.loc(0.165, sec=cell.dend[82])
    imp_0.compute(freq)  # check if you need at 10 Hz
    Rin_syn.append( imp_0.input(0.165, sec=cell.dend[82]))
add_figure('Rin to freq','freq [hz]','Rinput [M ohm]')
plt.plot(freqs,Rin_syn)
imp_0.compute(100)
plt.plot(100,   imp_0.input(0.165, sec=cell.dend[82])  ,'*')
plt.legend(['Rin2freq',str([10,   round(imp_0.input(0.165, sec=cell.dend[82]),2)])])
plt.savefig('data/Rin_freq')
plt.show()
Rin,dis=[],[]
freq=100
h.distance(0,0.5, sec=soma)

change_model_pas(CM=2, RA=70, RM=5684, E_PAS=-77.3)
# change_model_pas(CM=1.88, RA=98, RM=12371, E_PAS=-77.3)

for sec in h.allsec():
    imp_0 = h.Impedance(sec=sec)
    seg_len=sec.L / 15
    imp_0.loc(0.5, sec=soma)
    imp_0.compute(freq)  # check if you need at 10 Hz
    for seg in 1/15*np.arange(15):
        # imp_0.transfer(sec(seg))
        # imp_0.input(seg, sec=sec)
        Rin.append( imp_0.transfer(sec(seg)))
        dis.append(h.distance(sec(seg)))
add_figure('transfer impadence at freq '+str(freq)+'Hz','ditance form soma [micron]','transfer_resistance[ohm]' )
plt.plot(dis,Rin,'.')
sec=cell.dend[82]
seg=0.165
dis_syn=h.distance(sec(seg))
Rin_syn=imp_0.transfer(sec(seg))
plt.plot( dis_syn,Rin_syn ,'*',label=[round(dis_syn,2),round(Rin_syn,2)])
plt.text(0,0,'Cm,Ra,Rm=[2,70,5684]')
plt.legend()
plt.savefig('data/transfer resistance')
plt.show()

# Rin,dis=[],[]
# h.distance(0,0.5, sec=soma)
# for sec in h.allsec():
#     imp_0 = h.Impedance(sec=sec)
#     seg_len=sec.L / 15
#     for seg in 1/15*np.arange(15):
#         imp_0.loc(seg, sec=sec)
#         imp_0.compute(0)  # check if you need at 10 Hz
#         imp_0.transfer(soma)
#         Rin.append( imp_0.input(seg, sec=sec))
#         dis.append(h.distance(sec(seg)))
# plt.plot(dis,Rin,'.')
# plt.show()
a=1



