import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from extra_function import load_ASC,SIGSEGV_signal_arises
from read_spine_properties import get_spine_xyz,get_n_spinese
import signal
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
from glob import glob
from open_pickle import read_from_pickle
import sys
print(len(sys.argv),sys.argv,flush=True)

if len(sys.argv) != 3:
    print("sys.argv not running and with length",len(sys.argv))
    cells= read_from_pickle('cell_name.p')
    file_type='ASC'
else:
    print("sys.argv not running and with length",len(sys.argv))
    cells = read_from_pickle(sys.argv[1])
    file_type=sys.argv[2]
folder_=''
folder_data='cells_initial_information/'
folder_save='cells_outputs_data_short/'

def plot_morphology(cell_dir,dots_dir,syn_pose_list,with_axon=False, save_place=''):
    #syn_pose should be (x,y,z) coordinates
    cell=None
    cell=load_ASC(cell_dir,delete_axon=not with_axon)
    h.load_file("nrngui.hoc")
    color_code={'basal':'blue','apical':'black','axon':'red','soma':'purple','synapse':'cyan','synaptic_dend':'green'}
    plt.figure()
    ax = plt.axes(projection ="3d")

    plt.title("neuron morphology")
    for sec in cell.all_sec():
        all_points = []

        if sec in cell.apic:
            sec_type='apical'
        elif sec in cell.dend:
            sec_type='basal'
        elif sec in cell.axon:
            sec_type='axon'
        elif sec == cell.soma:
            sec_type='soma'
        else:
            raise "this isn't a section"
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        points = [initial_point]
        for i in range(1,sec.n3d()):
            dend_pos = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
            points_diffrance = dend_pos-initial_point
            distance = np.linalg.norm(initial_point - dend_pos)
            number_of_steps =int(np.ceil(distance))
            for step_number in range(1, number_of_steps, 1):
                intermideate_point = initial_point.copy() + points_diffrance*step_number/number_of_steps
                points.append(intermideate_point)
            points.append(dend_pos)
            initial_point = dend_pos
        # initial_point = points[0]
        all_points+=points

        for p in all_points:
            ax.scatter3D(p[0],p[1],p[2], color=color_code[sec_type],s=0.1,label=sec_type)
    points_dend=read_from_pickle(dots_dir)['synaptic_dend']
    for i in range(len(points_dend.keys())):
        for p in points_dend[i]:
                ax.scatter3D(p[0],p[1],p[2], color=color_code['synaptic_dend'],s=0.1,label='synaptic_dend')
    for j, syn_pos in enumerate(syn_pose_list):
        ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["synapse"],s=1,label=syn_pos)
    legend_elements = [
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["soma"], s=1, label="soma"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["apical"],  s=1, label="apical"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["basal"],  s=1, label="basal"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["synaptic_dend"],  s=1, label="synaptic_dend"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["synapse"],  s=1, label="synapse")
    ]
    plt.legend(handles=legend_elements, loc="best")
    plt.savefig(save_place+'.pdf')
    plt.savefig(save_place+'.png')

    plt.close()


if __name__=='__main__':
    for cell_name in cells:
        if len(glob(folder_data+cell_name+'/*'+file_type))<1:continue
        xyz=[]
        for i in range(get_n_spinese(cell_name)):
            xyz.append(get_spine_xyz(cell_name,i))
        cell_dir=glob(folder_data+cell_name+'/*ASC')[0]
        dict_dots_dir=folder_save+cell_name+'/synapses_neuron_morphology.p'
        plot_morphology(cell_dir,dict_dots_dir,xyz,with_axon=False, save_place=folder_save+cell_name+'/neurom morphology'+file_type)



