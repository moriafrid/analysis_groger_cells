import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from extra_function import load_ASC,SIGSEGV_signal_arises
import signal
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
from glob import glob
def plot_morphology(cell_dir,syn_pose_list,with_axon=False, save_place=''):
    #syn_pose should be (x,y,z) coordinates
    cell=None
    cell=load_ASC(cell_dir,delete_axon=not with_axon)
    h.load_file("nrngui.hoc")
    color_code={'basal':'blue','apical':'red','axon':'green','soma':'black','synapse':'cyan'}
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
            ax.scatter3D(p[0], p[1],p[2], color=color_code[sec_type],s=0.2,label=sec_type)

    for j, syn_pos in enumerate(syn_pose_list):
        ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["synapse"],s=1,label=syn_pos)
    legend_elements = [
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["soma"], lw=0.1, label="soma"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["apical"],  lw=0.1, label="apical"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["basal"],  lw=0.1, label="basal"),
    ax.scatter3D(syn_pos[0], syn_pos[1],syn_pos[2], color=color_code["synapse"],  lw=0.1, label="synapse")
        ]
    plt.legend(handles=legend_elements, loc="best")
    # plt.legend()
    plt.savefig(save_place+'.pdf')
    plt.close()


if __name__=='__main__':
    from read_spine_properties import get_spine_xyz,get_n_spinese, get_spine_part
    folder_data='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/'
    folder_save='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
    xyz=[]

    for cell_name in ['2017_05_08_A_4-5','2017_05_08_A_5-4','2017_03_04_A_6-7']:
        for i in range(get_n_spinese(cell_name)):
            xyz.append(get_spine_xyz(cell_name,i))
        dir=glob(folder_data+cell_name+'/*ASC')[0]
        plot_morphology(dir,xyz,with_axon=False, save_place=folder_save+cell_name+'/neurom morphology')



