from neuron import h, gui
import numpy as np
from glob import glob
h.load_file("import3d.hoc")
from math import pi
from

######################################################
# build the model
######################################################

fname = "05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Bluecell_spinec91.ASC"
def calculate_F_factor(cell_name,r_head,spine_neck_L,spine_neck_diam,spine_density=1.08,resize_dend=1, shrinkeage=1):
    file_name=glob(cell_name+'*.ASC')[0]
    cell = mkcell(file_name)
    # cell=instantiate_swc('/ems/elsc-labs/segev-i/moria.fridman/project/data_analysis_git/data_analysis/try1.swc')
    for sec in cell.axon:
       h.delete_section(sec=sec)
    for sec in h.allsec():
        sec.diam*=resize_dend
        sec.L*=shrinkeage
    dend_len=np.sum([sec.L for sec in cell.dend])
    spine_in_Micron_density = spine_density  # 12/10 #[N_spine/micrometer] number of spines in micrometer on the dendrite
    head_area=4*pi*r_head**2
    neck_area=2*pi*(spine_neck_diam/2)*spine_neck_L
    spine_area=neck_area+head_area
    spines_area=spine_area*dend_len*spine_in_Micron_density
    dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor

def calculate_F_factor(cell,spine_type,spines_density=1.08,spine_num=1, is_debug_print=False):
    #spine type can be the cell_name or "mouse_spine", "human_spine" or "shaft_spine"
    if is_debug_print:
        print("the spine_type for calculate the F_factor is "+spine_type)
    R_head,neck_diam,neck_length,spines_density_temp=get_F_factor_params(spine_type)
    if not np.isnan(spines_density_temp):
        spines_density=spines_density_temp
    dend_len=np.sum([sec.L for sec in cell.dend])
    try: dend_len+=np.sum([sec.L for sec in cell.apic])
    except : "no apical in this cell"
    # try: dend_len+=np.sum([sec.L for sec in cell.basal])
    # except : "no basal in this cell"
    head_area=4*pi*R_head**2
    neck_area=2*pi*(neck_diam/2)*neck_length
    spine_area=neck_area+head_area
    spines_area=spine_area*dend_len*spines_density
    dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
    try:dends_area+=np.sum([seg.area() for sec in cell.apic for seg in sec]) #* (1.0/0.7)
    except : "no apical in this cell"
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor
