import numpy as np
from neuron import h,gui
import signal
import pickle
from matplotlib import pyplot as plt
from glob import glob
import pandas as pd
import sys
from extra_function import load_ASC,SIGSEGV_signal_arises
from read_spine_properties import get_spine_xyz,get_n_spinese, get_spine_part
from open_pickle import read_from_pickle
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

if len(sys.argv) != 4:
    print("sys.argv not running and with length",len(sys.argv))
    cells= read_from_pickle('cells_name2.p')#['2016_05_12_A']#
    file_type='.ASC'
    with_plot=False
else:
    print("sys.argv is correct and running")
    cells = read_from_pickle(sys.argv[1])
    file_type=sys.argv[2]
    with_plot=eval(sys.argv[3])
folder_=''
folder_data='cells_initial_information/'
folder_save='cells_outputs_data_short/'

def synaptic_loc(cell_dir,syn_poses_list,with_plot=False, part='all', save_place=''):

    dict2={}
    cell=None
    cell=load_ASC(cell_dir)
    h.distance(0,0.5, sec=cell.soma)

    #syn_pose should be (x,y,z) coordinates
    # h.load_file("import3d.hoc")
    # h.load_file("nrngui.hoc")
    secs,dends,dists,dends_name,dis_from_soma,sec_name,sec_num,seg_num,best_dend_pos=[],[],[],[],[],[],[],[],[]
    for i in range(len(syn_poses_list)):
        secs.append(None)
        dends.append(None)
        sec_num.append(None)
        sec_name.append(None)
        seg_num.append(None)
        dists.append(10000)
        dends_name.append(None)
        dis_from_soma.append(None)
        best_dend_pos.append(None)

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
        #calculate the section len
        lens = []
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        for i in range(sec.n3d()):
            lens.append(np.linalg.norm(initial_point - np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])))
            initial_point = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
        total_len = np.sum(lens)
        #add number_of_step dots between the initial point and the next point for all segment
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        points = [initial_point]
        for i in range(1,sec.n3d()):
            dend_pos = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
            points_diffrance = dend_pos-initial_point #between the start of the dendrite and the next point
            distance = np.linalg.norm(initial_point - dend_pos) #distance between dots
            number_of_steps =int(np.ceil(distance))*2
            for step_number in range(1, number_of_steps, 1):
                intermideate_point = initial_point.copy() + points_diffrance*step_number/number_of_steps
                points.append(intermideate_point)
            points.append(dend_pos)
            initial_point = dend_pos
        initial_point = points[0]
        all_points+=points
        accumalate_len = 0
        #test if the synapse is inside this section
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
                    sec_name[j]=str(sec)[str(sec).find('>')+2:]
                    seg_num[j]=round(accumalate_len / total_len,3)
                    sec_num[j]=int(str(sec)[str(sec).find('[')+1:-1])
                    best_dend_pos[j]=dend_pos
                    dis_from_soma[j]=h.distance(sec(seg_num[j]))
    for j in range(get_n_spinese(cell_name)):
        print(sec_name[j],dists[j],best_dend_pos[j])

    if with_plot:
        fig=plt.figure()
        for p in all_points:
            plt.scatter(p[0], p[1], color='black',s=0.5)
    dend_pos_dict={}
    for j,dend in enumerate(dends_name):
        sec=eval('cell.'+dend[0])
        initial_point = np.array([sec.x3d(0), sec.y3d(0), sec.z3d(0)])
        points_dend = [initial_point]
        for i in range(1,sec.n3d()):
            dend_pos = np.array([sec.x3d(i), sec.y3d(i), sec.z3d(i)])
            # points_diffrance = dend_pos-initial_point
            # distance = np.linalg.norm(initial_point - dend_pos)
            # number_of_steps =int(np.ceil(distance))
            # for step_number in range(1, number_of_steps, 1):
            #     intermideate_point = initial_point.copy() + points_diffrance*step_number/number_of_steps
            #     points_dend.append(intermideate_point)
            points_dend.append(dend_pos)
            dend_pos_dict[j]=points_dend
            # initial_point = dend_pos
            if with_plot:
                plt.scatter(dend_pos[0], dend_pos[1], color='g',s=0.5)
        # for p in points_dend:
        #     plt.scatter(p[0], p[1], color='g',s=0.5)
    if with_plot:
        for j, syn_pos in enumerate(syn_poses_list):
            # if type(syn_pos)!=list:
            #     syn_pos=[syn_pos]
            dis_from_soma[j]=syn_dis_from_soma(cell,dends_name[j])
            plt.scatter(syn_pos[0], syn_pos[1],s=0.7, color='cyan')
            plt.text(-50,-50,str(syn_pos)+'dis from soma='+str(dis_from_soma[j]))
        color_code={'basal':'blue','apical':'red','axon':'green','soma':'purple','synapse':'cyan','syn_trunk':'green'}
        for i in range(cell.soma.n3d()):
            plt.scatter(cell.soma.x3d(i), cell.soma.y3d(i),lw=cell.soma.diam3d(i), color=color_code['soma'])

        legend_elements = [
        plt.scatter(syn_pos[0], syn_pos[1], color='black', s=0.5, label="all_point"),
        plt.scatter(syn_pos[0], syn_pos[1], color='green',s=0.5, label="syn_trunk"),
        plt.scatter(syn_pos[0], syn_pos[1], color=color_code['soma'],s=0.5, label="soma"),
        plt.scatter(syn_pos[0], syn_pos[1], color='cyan', s=0.5, label="synapse")
            ]
        plt.legend(handles=legend_elements, loc="best")
        plt.savefig(save_place+'.pdf')
        plt.savefig(save_place)
        pickle.dump(fig, open(save_place+'.p', 'wb'))

        plt.close()
    with open(save_place + '_neuron_morphology.p', 'wb') as f:
        pickle.dump({"all_point":all_points,"synaptic_dend":dend_pos_dict,"syn_pos":xyz,"syn_sec_pos":dends_name}, f)

    dict = {'sec_name':sec_name,'sec_num':sec_num,'seg_num':seg_num,'place_name':dends_name,'dist_from_soma':dis_from_soma,'dist':dists, 'part':part}
    # print(dict)

    try_save_dict(dict,folder_save+cell_name+'/','synaptic_location')
    for i in range(len(syn_poses_list)):
        dict2[str(i)] = {'sec_name':sec_name[i],'sec_num':sec_num[i],'seg_num':seg_num[i],'place_name':dends_name[i],'dist_from_soma':dis_from_soma[i],'dist':dists[i], 'part':part,'best_found_location':best_dend_pos}
        # print(dict2)

    try_save_dict(dict2,folder_save+cell_name+'/','synaptic_location_seperate')
    return dict,dict2

def syn_dis_from_soma(cell,syn_loc):
    h.distance(0, 0.5, sec=cell.soma)
    synapses_dis_from_soma=h.distance(eval('cell.' + syn_loc[0])(syn_loc[1]))
    return synapses_dis_from_soma
def try_save_dict(dict,folder_save,name):
    try:
        with open(folder_save + name+'.p', 'wb') as f:
            pickle.dump(dict, f)
    except Exception as e:
        print("Error trying to save pickle: " + str(e))
        pass

    with open(folder_save+name+'.txt', 'w') as f:
        try:
            f.write('synaptic_location')
            f.write(dict)
        except Exception as e:
            print("Error trying to save txt: " + str(e))
            pass
    try:
        df1 = pd.DataFrame(dict)
        df1.to_excel(folder_save+name+".xlsx")
    except Exception as e:
        print("Error trying to save xlsx: " + str(e))
        pass
if __name__=='__main__':
    dict2={}
    dict3,dict4={},{}
    name2save=''
    cell_withou_xyz=[]
    for cell_name in cells:
        xyz,dend_part=[],[]
        if len(glob(folder_data+cell_name+'/*'+file_type))<1:continue
        dir=glob(folder_data+cell_name+'/*'+file_type)[0]
        if 'shrinkXYZ' in dir:
            dir=glob(folder_data+cell_name+'/*'+file_type)[1]
        if cell_name in ['2017_07_06_C_3-4','2017_07_06_C_4-3']:
            dir=glob(folder_data+cell_name+'/*/'+cell_name+file_type)[0]
        for i in range(get_n_spinese(cell_name)):
            print('one syn dict:',dict)
            xyz.append(list(get_spine_xyz(cell_name,i)))
            dend_part.append(get_spine_part(cell_name,i))

        dict1,dict2=synaptic_loc(dir,xyz, part='all', save_place=folder_save+cell_name+'/synapses',with_plot=with_plot)
        dict3[cell_name]=dict1
        for key in dict2.keys():
            dict4[cell_name+key]=dict2[key]
        print('more then one syn dict',cell_name,[xyz])
    try_save_dict(dict3,folder_save,'synaptic_location')
    try_save_dict(dict4,folder_save,'synaptic_location_seperate')
    # with open("cells_without_xyz.p", 'wb') as handle:
    #     pickle.dump(cell_withou_xyz, handle, protocol=pickle.HIGHEST_PROTOCOL)
