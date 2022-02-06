from neuron import h, gui
import numpy as np
h.load_file("import3d.hoc")
from math import pi
from glob import glob
from extra_function import mkcell
from spine_classes import SpinesParams, GeneralSpine
######################################################
def calculate_F_factor(cell_name,spine_type,data_folder,spines_density=1.08,spine_num=1):
    print("the spine_type for calculate the F_factor is "+spine_type)
    if spine_type=="groger_spine":
        spine=SpinesParams(cell_name,spine_num=spine_num)
    else:
        spine=GeneralSpine(spine_type)
    R_head,neck_diam,neck_length=spine.get_F_factor_params()

    print(data_folder+"/"+cell_name+'/*ASC')
    cell=mkcell(glob(data_folder+"/"+cell_name+'/*ASC')[0])
    dend_len=np.sum([sec.L for sec in cell.dend])
    spine_in_Micron_density=spines_density#12/10 #[N_spine/micrometer] number of spines in micrometer on the dendrite
    head_area=4*pi*R_head**2
    neck_area=2*pi*(neck_diam/2)*neck_length
    spine_area=neck_area+head_area
    spines_area=spine_area*dend_len*spine_in_Micron_density
    dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor

# def calculate_F_factor(cell,V_head,spine_neck_diam,spine_neck_L,spines_density=1.08):
#
#     dend_len=np.sum([sec.L for sec in cell.dend])
#     spine_in_Micron_density=spines_density#12/10 #[N_spine/micrometer] number of spines in micrometer on the dendrite
#     r_head=(V_head/(4*pi/3))**(1/3)
#     head_area=4*pi*r_head**2
#     neck_area=2*pi*(spine_neck_diam/2)*spine_neck_L
#
#     spine_area=neck_area+head_area
#
#     spines_area=spine_area*dend_len*spine_in_Micron_density
#     dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
#
#     F_factor=(spines_area+dends_area)/dends_area
#     return F_factor


