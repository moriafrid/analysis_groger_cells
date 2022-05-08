import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from add_figure import add_figure
from glob import glob
from extra_function import create_folder_dirr,SIGSEGV_signal_arises,load_ASC,load_hoc,load_swc
import sys
import pickle
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

print(len(sys.argv),sys.argv,flush=True)

if len(sys.argv) != 3:
    print("sys.argv not running and with length",len(sys.argv))
    cell_name= '2017_03_04_A_6-7(0)'
    file_type2read= 'z_correct.swc'
else:
    print("sys.argv is correct and running")
    cell_name = sys.argv[1]
    file_type2read=sys.argv[2]
folder_=''
data_dir= "cells_initial_information"
save_dir = "cells_outputs_data_short"
print(cell_name, folder_+data_dir+"/"+cell_name+"/*"+file_type2read)
cell_file = glob(folder_+data_dir+"/"+cell_name+"/*"+file_type2read)[0]

path_short_pulse=folder_+save_dir+'/'+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p'
# folder_save=folder_+save_dir+'/'+cell_name+'/data/cell_properties/'+file_type2read+'SPINE_START=20/dend*'++'&F_shrinkage'++'/diam_dis/'
folder_save=folder_+save_dir+'/'+cell_name+'/data/cell_properties/'+file_type2read+'/diam_dis/'

create_folder_dirr(folder_save)

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

f=open(folder_save+'cell_propertis.txt', 'w')
f.write('The '+cell_name+ ' cell_propertis\n')
def cumpute_distances(base_sec):
    for sec in h.SectionRef(sec=base_sec).child:
        add_sec(sec)
        cumpute_distances(sec)
def add_sec(sec):
    """
    morpho dendogram
    :param sec:
    :return:
    """
    h.distance(0, 0.5, sec=cell.soma)
    dist[sec] = h.distance(1, sec=sec)

#track from the terminals to the soma
def track_one(terminal):
    # h.distance(0, 0.5, sec=soma)
    sec=terminal
    dis=[]
    diam=[]
    while sec !=soma:
        # dis.append(h.distance(sec.parentseg()))
        h.distance(0, 0.5, sec=soma)

        dis.append(h.distance(1,sec=sec))
        sec_ref=h.SectionRef(sec=sec)
        diam.append(sec.diam)
        sec=sec_ref.parent
    return np.array(dis),np.array(diam)
######################################################
# build the model
######################################################
# h.load_file("/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_03_04_A_6-7(0)(0)/03_24_A_11052017_Splice_Shrink_zvalue_LABEL_Bluecell_Zcorrected_by_Gregor.hoc")
if 'ASC' in file_type2read:
    cell=load_ASC(cell_file)
elif 'hoc'in file_type2read:
    cell=load_hoc(cell_file)
elif 'swc' in file_type2read:
    cell=load_swc(cell_file)
print (cell)
sp = h.PlotShape()
sp.show(0)  # show diameters
try:
    for sec in cell.axon:
        h.delete_section(sec=sec)
except:
    print(cell_name.split('/')[-1] +' dont have axon inside')
soma= cell.soma
# insert pas to all other section
for sec in tqdm(cell.all_sec()):
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
soma_ref=h.SectionRef(sec=soma)
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

terminals = []
for sec in cell.dend:
    if len(sec.children())==0:
        terminals.append(sec)
plt.close()
fig=add_figure('diam-dis relation along dendrites with diffrent collors\n'+cell_name+' '+file_type2read,'distance from soma','diameter')
i=0
for terminal in terminals:
    i+=1
    dis,diam=track_one(terminal)
    plt.plot(dis,diam,alpha=0.5)
    if len(diam)==1:
        plt.plot(dis,diam,'*')
plt.savefig(folder_save+'diam-dis.png')
plt.savefig(folder_save+'diam-dis.pdf')
pickle.dump(fig, open(folder_save+'diam-dis.p', 'wb'))
plt.show()
