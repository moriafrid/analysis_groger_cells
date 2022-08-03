
from glob import glob

from matplotlib import pyplot as plt

from extra_function import load_ASC, load_swc
from neuron import h
from open_pickle import read_from_pickle
from plot_morphology_Yoni import plot_morph
from read_spine_properties import get_sec_and_seg

file=['ASC','z_correct.swc']
path=glob('cells_initial_information/*/*.ASC')
path1=glob('cells_initial_information/*/*z_correct.swc')
def sec_from_soma(cell,sec):
    section=eval('cell.'+sec)
    diam=section.diam
    child=len(section.children())
    sec_from_soma=1
    parent_list=[section]
    while section!=cell.soma:
        sec_from_soma+=1
        section=section.parentseg().sec
        parent_list.append(section)
    return sec_from_soma,child,diam
def section_with_distance_and_children(cell,sec_num,child_num,type,diam):
    #find tips:
    tips=[]
    for sec_t in eval("cell."+type):
        if len(sec_t.children())==0:
            tips.append(sec_t)
    #find section with the x distance from the soma:
    correct_sec_from_soma=[]
    for sec_t in tips:
        s=sec_t
        branch_sec=[s]
        num=1
        while s!=cell.soma:
            num+=1
            s=s.parentseg().sec
            branch_sec.append(s)
        try:
            correct_sec_from_soma.append(branch_sec[-sec_num])
        except:continue
    #check if the child_num is corrret:
    correct_sec_from_soma=list(dict.fromkeys(correct_sec_from_soma))
    with_correct_children_num=[]

    for sec_t in correct_sec_from_soma:
        if len(sec_t.children())==child_num:
            with_correct_children_num.append(sec_t)
    with_correct_diam=[]
    round_num=6
    while len(with_correct_diam)==0:
        for sec_t in with_correct_children_num:
            # print(sec_t,sec_t.diam)
            if round(sec_t.diam,round_num)==round(diam,round_num):
                with_correct_diam.append(sec_t.name())
        round_num-=1
    return with_correct_diam
if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p')[0:]:
        print(cell_name)
        fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
        fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
        shapes = (1, 2)
        ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
        ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
        plot_morph(ax1,cell_name,'_before_shrink')
        plot_morph(ax2,cell_name,'_after_shrink')
        plt.show()
        path=glob('cells_initial_information/'+cell_name+'/*before_shrink.swc')[0]
        cell=load_swc(path)
        secs,seg=get_sec_and_seg(cell_name)
        print(secs)
        sec_distances,child_nums,diams=[],[],[]
        for secy in secs:
            sec_distance,child_num,diam=sec_from_soma(cell,secy)
            sec_distances.append(sec_distance)
            child_nums.append(child_num)
            diams.append(diam)
        #check how much supposed to be:
        old_sec_finding=[]
        for i,sec_distance,child_num,diam in zip(range(len(secs)),sec_distances,child_nums,diams):
            type_sec=secs[i][:secs[i].rfind('[')]
            print('new finding:',section_with_distance_and_children(cell,sec_distance,child_num,type_sec,diam))
            old_sec_finding.append(section_with_distance_and_children(cell,sec_distance,child_num,type_sec,diam))
        cell=None
        path1=glob('cells_initial_information/'+cell_name+'/*after_shrink.swc')[0]
        # cell_name='2017_07_06_C_4-3'
        # sec_distances=[7]
        # child_nums=[2]
        # diams=[0.7499999999999999]
        cell=load_swc(path1)
        new_sec=[]
        for sec_distance,child_num,diam in zip(sec_distances,child_nums,diams):
            new_sec.append(section_with_distance_and_children(cell,sec_distance,child_num,type_sec,diam))
        print(new_sec)

        a=1
