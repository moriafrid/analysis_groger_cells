import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from add_figure import add_figure
from glob import glob
from extra_function import create_folder_dirr,SIGSEGV_signal_arises,mkcell
import sys

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
print(len(sys.argv))
print(cell_name, folder_+data_dir+"/"+cell_name+"/*.ASC")

cell_file = glob(folder_+data_dir+"/"+cell_name+"/*.ASC")[0]
path_short_pulse=folder_+save_dir+'/'+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p'
folder_save=folder_+save_dir+'/'+cell_name+'/cell_properties/'

create_folder_dirr(folder_save)

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

f=open(folder_save+'cell_propertis.txt', 'w')
f.write('The '+cell_name+ ' cell_propertis\n')
######################################################
# build the model
######################################################
# h.load_file("/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_03_04_A_6-7/03_24_A_11052017_Splice_Shrink_zvalue_LABEL_Bluecell_Zcorrected_by_Gregor.hoc")

cell=mkcell(cell_file)
print (cell)
sp = h.PlotShape()
sp.show(0)  # show diameters

soma= cell.soma[0]
# insert pas to all other section
for sec in tqdm(h.allsec()):
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances


clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
clamp.amp = -0.05  ## supopsed to be 0.05nA
clamp.dur = 200
clamp.delay = 190

#short_pulse, hz, rest = read_from_pickle(path, hz=True ,rest=True)
# V = short_pulse[0]
# T = short_pulse[1]
# E_PAS = rest
# V+=E_PAS
#
# h.tstop = T[-1]
# h.v_init=E_PAS
# h.dt = 0.1
# h.steps_per_ms = h.dt

imp = h.Impedance(sec=soma)
imp.loc(soma(0.5))
imp.compute(0)
imp.input(0)
imp.compute(0)
print('the impadence is',imp.input(0))
f.write('The impadence is '+str(imp.input(0))+'\n')

#print the dendrite diameter:
soma_ref=h.SectionRef(sec=cell.soma[0])
print("the soma's childrens diameter is:")
f.write("\nThe soma's childrens diameter is\n")

for i in range(soma_ref.nchild()):
    print(soma_ref.child[i](0).diam)
    f.write(str(soma_ref.child[i](0).diam)+"\n")

length=0
for dend in cell.dend:
    length+=dend.L
print("total dendritic length is ",length)
f.write("\nThe total dendritic length is "+str(length)+ "\n")
f.close()
#track from the terminals to the soma
def track_one(terminal):
    h.distance(0, 0.5, sec=soma)
    sec=terminal
    dis=[]
    diam=[]
    while sec !=soma:
        dis.append(h.distance(sec.parentseg()))
        sec_ref=h.SectionRef(sec=sec)
        diam.append(sec.diam)
        sec=sec_ref.parent
    return np.array(dis),np.array(diam)
terminals = []
for sec in cell.dend:
    if len(sec.children())==0:
        terminals.append(sec)
plt.close()
add_figure('diam-dis relation along dendrites with diffrent collors','distance from soma','diameter')
i=0
for terminal in terminals[:-14:2]:
    i+=1
    dis,diam=track_one(terminal)
    plt.plot(dis,diam,alpha=0.5)
plt.savefig(folder_save+'diam-dis.png')
plt.savefig(folder_save+'diam-dis.pdf')
