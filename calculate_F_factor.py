from neuron import h, gui
import numpy as np
from math import pi
h.load_file("import3d.hoc")
from read_spine_properties import get_F_factor_params,get_parameter
######################################################
def calculate_F_factor(cell,spine_type='mean_spine',spines_density=1.08,spine_num=1, double_spine=False,is_debug_print=False):
    #spine type can be the cell_name or "mouse_spine", "human_spine" or "shaft_spine"
    if is_debug_print:
        print("the spine_type for calculate the F_factor is "+spine_type)
    spine_area=get_parameter(spine_type,'spine_area')[0]
    spines_density_temp=get_parameter(spine_type,'spine_density')[0]
    if not np.isnan(spines_density_temp):
        if spines_density!=spines_density_temp:
            spines_density=spines_density
        else:
            spines_density=spines_density_temp
    print("spine density="+str(spines_density))
    if spine_type!='mean_spine':
        R_head,neck_diam,neck_length=get_F_factor_params(spine_type)
        head_area=4*pi*R_head**2
        neck_area=2*pi*(neck_diam/2)*neck_length
        spine_area=neck_area+head_area
        print('neck_area:',neck_area,'head_area:',head_area,'spine_area:',spine_area)

    dend_len=np.sum([sec.L for sec in cell.dend])
    try: dend_len+=np.sum([sec.L for sec in cell.apic])
    except : "no apical in this cell"
    # if double_spine:
    #     spine_area*=2
    #     print('the spine area change to be',spine_area)
    spines_area=spine_area*dend_len*spines_density
    dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
    try:dends_area+=np.sum([seg.area() for sec in cell.apic for seg in sec]) #* (1.0/0.7)
    except : "no apical in this cell"
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor
if __name__=='__main__':
    from extra_function import load_ASC,load_hoc,load_swc,SIGSEGV_signal_arises,create_folder_dirr
    cell=load_swc('cells_initial_information/2017_05_08_A_4-5/morphology_z_correct.swc')
    # cell=load_ASC('cells_initial_information/2017_05_08_A_5-4/05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Pinkcell.ASC')
    F=calculate_F_factor(cell)
