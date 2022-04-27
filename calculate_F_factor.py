from neuron import h, gui
import numpy as np
from math import pi

h.load_file("import3d.hoc")
from glob import glob
from extra_function import load_ASC,load_hoc
from read_spine_properties import get_F_factor_params
######################################################
def calculate_F_factor(cell,spine_type,spines_density=1.08,spine_num=1, double_spine=False,is_debug_print=False):
    #spine type can be the cell_name or "mouse_spine", "human_spine" or "shaft_spine"
    if is_debug_print:
        print("the spine_type for calculate the F_factor is "+spine_type)
    R_head,neck_diam,neck_length,spines_density_temp=get_F_factor_params(spine_type)
    if not np.isnan(spines_density_temp):
        if spines_density!=spines_density_temp:
            spines_density=spines_density
        else:
            spines_density=spines_density_temp
    print("spine density="+str(spines_density))

    dend_len=np.sum([sec.L for sec in cell.dend])
    try: dend_len+=np.sum([sec.L for sec in cell.apic])
    except : "no apical in this cell"
    # try: dend_len+=np.sum([sec.L for sec in cell.basal])
    # except : "no basal in this cell"
    head_area=4*pi*R_head**2
    neck_area=2*pi*(neck_diam/2)*neck_length
    spine_area=neck_area+head_area
    print('neck_area:',neck_area,'head_area:',head_area,'spine_area:',spine_area)
    if double_spine:
        spine_area*=2
        print('the spine area change to be',spine_area)
    spines_area=spine_area*dend_len*spines_density
    dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
    try:dends_area+=np.sum([seg.area() for sec in cell.apic for seg in sec]) #* (1.0/0.7)
    except : "no apical in this cell"
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor
