import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from add_figure import add_figure, adgust_subplot
from glob import glob
from extra_function import create_folder_dirr,SIGSEGV_signal_arises,load_ASC,load_hoc,load_swc
import sys
import pickle
import matplotlib

from read_spine_properties import get_sec_and_seg

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

print(len(sys.argv),sys.argv,flush=True)

if len(sys.argv) != 3:
    print("sys.argv not running and with length",len(sys.argv))
    cell_name= '2017_07_06_C_3-4'
    file_type2read= 'z_correct_after_shrink.swc'
else:
    print("sys.argv is correct and running")
    cell_name = sys.argv[1]
    file_type2read=sys.argv[2]
folder_=''
data_dir= "cells_initial_information"
save_dir = "cells_outputs_data_short"
print(cell_name, folder_+data_dir+"/"+cell_name+"/"+file_type2read)

path_short_pulse=folder_+save_dir+'/'+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p'
# folder_save=folder_+save_dir+'/'+cell_name+'/data/cell_properties/'+file_type2read+'SPINE_START=20/dend*'++'&F_shrinkage'++'/diam_dis/'
folder_save=folder_+save_dir+'/'+cell_name+'/data/cell_properties/'+file_type2read+'/diam_dis/'
create_folder_dirr(folder_save)

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

f=open(folder_save+'cell_propertis.txt', 'w')
f.write('The '+cell_name+ ' cell_propertis\n')
def cumpute_distances(base_sec,cell):
    for sec in h.SectionRef(sec=base_sec).child:
        add_sec(sec,cell)
        cumpute_distances(sec,cell)
def add_sec(sec,cell):
    """
    morpho dendogram
    :param sec:
    :return:
    """
    h.distance(0, 0.5, sec=cell.soma)
    dist[sec] = h.distance(1, sec=sec)

#track from the terminals to the soma
def track_one(terminal,cell,ax):

    # h.distance(0, 0.5, sec=soma)
    sec=terminal
    dis=[]
    diam=[]

    syn_secs,syn_segs=get_sec_and_seg(cell_name)
    while sec !=cell.soma:
        # dis.append(h.distance(sec.parentseg()))
        h.distance(0, 0.5, sec=cell.soma)

        dis.append(h.distance(1,sec=sec))

        sec_ref=h.SectionRef(sec=sec)
        diam.append(sec.diam)
        sec_name=sec.name().split('.')[-1]
        if sec_name in syn_secs:
            #ax.scatter(sec.diam,dis[-2]+(dis[-1]-dis[-2])*syn_segs[syn_secs.index(sec_name)])
            syn_dis.append(h.distance(syn_segs[syn_secs.index(sec_name)],sec=sec))
            syn_diam.append(sec(syn_segs[0]).diam)
            dis.append(h.distance(1,sec=sec))
            diam.append(sec.diam)
        sec=sec_ref.parent
    return np.array(dis),np.array(diam)
######################################################
# build the model
######################################################
# h.load_file("/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_03_04_A_6-7(0)(0)/03_24_A_11052017_Splice_Shrink_zvalue_LABEL_Bluecell_Zcorrected_by_Gregor.hoc")
def diam_distance_plot(cell_name,file_type2read,data_dir= "cells_initial_information",ax=None,latter='',save_fig=True,compossed_title=False):
    global syn_dis,syn_diam
    syn_dis,syn_diam=[],[]
    if ax==None:
        if not compossed_title:
            title='diam-dis'+cell_name+' \n'+file_type2read
        else:
            title=cell_name
        fig=add_figure(title,'distance from soma','diameter')
        ax=fig.axes[0]
    else:
        adgust_subplot(ax,cell_name,'distance from soma','diameter',latter=latter)
    cell_file = glob(data_dir+"/"+cell_name+"/*"+file_type2read)[0]
    if 'XYZ' not in file_type2read and 'XYZ' in cell_file:
        cell_file = glob(folder_+data_dir+"/"+cell_name+"/*"+file_type2read)[1]
    if 'ASC' in file_type2read:
        cell=load_ASC(cell_file)
    elif 'hoc'in file_type2read:
        cell=load_hoc(cell_file)
    elif 'swc' in file_type2read:
        cell=load_swc(cell_file)

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
    for sec in cell.all_sec():
        if len(sec.children())==0:
            terminals.append(sec)


    i=0
    for terminal in terminals:
        i+=1
        dis,diam=track_one(terminal,cell,ax)
        ax.plot(dis,diam,alpha=0.5)
        if len(diam)==1:
            ax.plot(dis,diam,'*')
    i=0
    for syn_dis1,syn_diam1 in zip(list(dict.fromkeys(syn_dis)),list(dict.fromkeys(syn_diam))):
        ax.scatter(syn_dis1,syn_diam1,label='distance='+str(round(syn_dis1,2))+'um')
        i+=1
    plt.legend()
    ax.text(0.02, 0.02,'Total Length='+str(round(length))+'um',transform=ax.transAxes,size=12)

    if save_fig:
        plt.savefig(folder_save+'diam-dis.png')
        plt.savefig(folder_save+'diam-dis.pdf')
        pickle.dump(fig, open(folder_save+'diam-dis.p', 'wb'))
        plt.show()
    cell=None
if __name__=="__main__":
    diam_distance_plot(cell_name,file_type2read,data_dir= "cells_initial_information",compossed_title=True)
