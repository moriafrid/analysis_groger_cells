import numpy as np
from neuron import h,gui
import signal
import pickle
from matplotlib import pyplot as plt
from extra_function import load_ASC
from glob import glob
import xlsxwriter
def synaptic_loc_one(cell_ASC,syn_pos):###need a lot of correction moria
    cell=load_ASC(cell_ASC)
    #syn_pose should be (x,y,z) coordinates
    h.load_file("import3d.hoc")
    h.load_file("nrngui.hoc")
    # secs,dends,dists,dends_name=[],[],[],[]
    # for i in range(len(syn_poses)):
    #     secs.append(None)
    #     dends.append(None)
    #     dists.append(10000)
    #     dends_name.append(None)
    dist=10000
    for sec in h.allsec():
        if sec in cell.soma:continue
        lens = []
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        for i in range(sec.n3d()):
            lens.append(np.linalg.norm(initial_point - np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])))
            initial_point = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
        total_len = np.sum(lens)
        accumalate_len = 0
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        for i in range(sec.n3d()):
            print(i)
            dend_pos = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
            accumalate_len += np.linalg.norm(initial_point - dend_pos)
            initial_point = dend_pos

            if np.linalg.norm(syn_pos - dend_pos) < dist:
                dist=np.linalg.norm(syn_pos - dend_pos)
                sec=[sec, accumalate_len / total_len]
                dend=[sec,round(accumalate_len / total_len,3)]
                dend_name=[str(sec)[str(sec).find('>')+2:],round(accumalate_len / total_len,3)]
    return {'place_name':dend_name,'place_as_sec':dend}

def synaptic_loc(cell_dir,syn_poses_list,return_more_than_one=False, part='all', save_place=''):
    cell=None
    cell=load_ASC(cell_dir)
    #syn_pose should be (x,y,z) coordinates
    # h.load_file("import3d.hoc")
    h.load_file("nrngui.hoc")
    secs,dends,dists,dends_name,dis_from_soma=[],[],[],[],[]
    for i in range(len(syn_poses_list)):
        secs.append(None)
        dends.append(None)
        dists.append(10000)
        dends_name.append(None)
        dis_from_soma.append(None)

    if part == 'all':
        relevant_sections = cell.all_sec()
    elif part == 'basal':
        relevant_sections = cell.dend
    elif part == 'apical':
        if len(cell.apic)==0:
            relevant_sections = cell.dend
        else:
            relevant_sections = cell.apic
    else:
        raise BaseException('the part is not good '+str(part))
    all_points = []
    for sec in relevant_sections:
        lens = []
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        for i in range(sec.n3d()):
            lens.append(np.linalg.norm(initial_point - np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])))
            initial_point = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
        total_len = np.sum(lens)
        accumalate_len = 0
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
        initial_point = points[0]
        all_points+=points
        for point in points[1:]:
            dend_pos = point
            accumalate_len += np.linalg.norm(initial_point - dend_pos)
            initial_point = dend_pos
            for j, syn_pos in enumerate(syn_poses_list):
                if np.linalg.norm(syn_pos - dend_pos) < dists[j]:
                    dists[j] = np.linalg.norm(syn_pos - dend_pos)
                    secs[j] = [sec, accumalate_len / total_len]
                    dends[j]=[sec,round(accumalate_len / total_len,3)]
                    dends_name[j]=[str(sec)[str(sec).find('>')+2:],round(accumalate_len / total_len,3)]
    plt.figure()
    for p in all_points:
        plt.scatter(p[0], p[1], color='k',s=0.5)

    sec=eval('cell.'+dends_name[0][0])
    initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
    points_dend = [initial_point]
    for i in range(1,sec.n3d()):
        dend_pos = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
        points_diffrance = dend_pos-initial_point
        distance = np.linalg.norm(initial_point - dend_pos)
        number_of_steps =int(np.ceil(distance))
        for step_number in range(1, number_of_steps, 1):
            intermideate_point = initial_point.copy() + points_diffrance*step_number/number_of_steps
            points_dend.append(intermideate_point)
        points_dend.append(dend_pos)
        initial_point = dend_pos
    for p in points_dend:
        plt.scatter(p[0], p[1], color='g',s=0.5)

    for j, syn_pos in enumerate(syn_poses_list):
        dis_from_soma[j]=syn_dis_from_soma(cell,dends_name[j])
        plt.scatter(syn_pos[j][0], syn_pos[j][1],s=0.7, color='cyan')
        plt.text(-50,-50,str(syn_pos)+'dis from soma='+str(dis_from_soma[j]))
    color_code={'basal':'blue','apical':'red','axon':'green','soma':'purple','synapse':'cyan','syn_trunk':'green'}
    # soma_point=[]
    for i in range(cell.soma.n3d()):
        # soma_point.append(np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)]))
        plt.scatter(sec.x3d(i), sec.y3d(i),s=0.5, color=color_code['soma'])

    legend_elements = [
    plt.scatter(syn_pos[0][0], syn_pos[0][1], color='black', lw=0.1, label="all_point"),
    plt.scatter(syn_pos[0][0], syn_pos[0][1], color='green', lw=0.1, label="syn_trunk"),
    plt.scatter(syn_pos[0][0], syn_pos[0][1], color=color_code['soma'],lw=0.1, label="soma"),
    plt.scatter(syn_pos[0][0], syn_pos[0][1], color='cyan', lw=0.1, label="synapse")
        ]
    plt.legend(handles=legend_elements, loc="best")
    plt.savefig(save_place+'.pdf')
    plt.savefig(save_place)
    plt.close()
    with open(save_place + '_neuron_morphology.p', 'wb') as f:
        pickle.dump({"all_point":all_points,"syn_pos":xyz,"syn_sec_pos":dends_name}, f)
    if return_more_than_one:
        return {'place_name':dends_name,'place_as_sec':dends,'dist_from_soma':dis_from_soma,'dist':dists, 'part':part}
    else:
        return {'place_name':dends_name[0],'place_as_sec':dends[0],'dist_from_soma':dis_from_soma,'dist':dists[0], 'part':part}

def syn_dis_from_soma(cell,syn_loc):
    h.distance(0, 0.5, sec=cell.soma)
    synapses_dis_from_soma=[syn_loc[0], h.distance(eval('cell.' + syn_loc[0])(syn_loc[1]))]
    return synapses_dis_from_soma

if __name__=='__main__':
    from extra_function import load_ASC,SIGSEGV_signal_arises
    signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
    from read_spine_properties import get_spine_xyz,get_n_spinese, get_spine_part
    folder_data='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/'
    folder_save='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
    for cell_name in ['2017_05_08_A_4-5','2017_05_08_A_5-4','2017_03_04_A_6-7']:
        dict={}
        xyz,dend_part=[],[]
    # for cell_name in ['2017_05_08_A_5-4']:
        dir=glob(folder_data+cell_name+'/*ASC')[0]
        for i in range(get_n_spinese(cell_name)):
            xyz.append(get_spine_xyz(cell_name,i))
            dend_part.append(get_spine_part(cell_name,i))
            print(cell_name,[xyz])
        dict[cell_name]=synaptic_loc(dir,[xyz], part='all', save_place=folder_save+cell_name+'/synapses',return_more_than_one=True),xyz
            # dict[cell_name+'_'+str(i)]=synaptic_loc(dir,[xyz], part=dend_part),xyz

    with open(folder_save + 'synaptic_location.p', 'wb') as f:
        pickle.dump( dict, f)
    with open(folder_save+'synaptic_location.txt', 'w') as f:
        f.write('synaptic_location')
        f.write(dict)
    a=1
