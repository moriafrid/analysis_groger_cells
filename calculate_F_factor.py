from neuron import h, gui
import numpy as np
from math import pi

h.load_file("import3d.hoc")
from glob import glob
from extra_function import load_ASC,load_hoc
from read_spine_properties import get_F_factor_params
######################################################
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
    F_factor=(spines_area+dends_area)/dends_area
    return F_factor
#
# def calculate_F_factor(cell_name,spine_type,file_type,data_folder,spines_density=1.08,spine_num=1):
#     print("the spine_type for calculate the F_factor is "+spine_type)
#     R_head,neck_diam,neck_length,spines_density_temp=get_F_factor_params(spine_type)
#     if not np.isnan(spines_density_temp):
#         spines_density=spines_density_temp
#     print(data_folder+"/"+cell_name+'/*'+file_type)
#     cell=None
#     if file_type== 'ASC':
#         cell=load_ASC(glob(data_folder+"/"+cell_name+'/*.ASC')[0])
#     elif file_type== 'hoc':
#         cell=load_hoc(glob(data_folder+"/"+cell_name+'/*.hoc')[0])
#     dend_len=np.sum([sec.L for sec in cell.dend])
#     try: dend_len+=np.sum([sec.L for sec in cell.apic])
#     except : "no apical in this cell"
#     # try: dend_len+=np.sum([sec.L for sec in cell.basal])
#     # except : "no basal in this cell"
#     head_area=4*pi*R_head**2
#     neck_area=2*pi*(neck_diam/2)*neck_length
#     spine_area=neck_area+head_area
#     spines_area=spine_area*dend_len*spines_density
#     dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
#     F_factor=(spines_area+dends_area)/dends_area
#     return F_factor
#from spine_classes import SpinesParams, GeneralSpine

# def calculate_F_factor(cell_name,spine_type,data_folder,spines_density=1.08,spine_num=1):
#     print("the spine_type for calculate the F_factor is "+spine_type)
#     if spine_type=="groger_spine":
#         spine=SpinesParams(cell_name,spine_num=spine_num)
#     else:
#         spine=GeneralSpine(spine_type)
#     R_head,neck_diam,neck_length=spine.get_F_factor_params()
#
#     print(data_folder+"/"+cell_name+'/*ASC')
#     cell=mkcell(glob(data_folder+"/"+cell_name+'/*ASC')[0])
#     dend_len=np.sum([sec.L for sec in cell.dend])
#     spine_in_Micron_density=spines_density#12/10 #[N_spine/micrometer] number of spines in micrometer on the dendrite
#     head_area=4*pi*R_head**2
#     neck_area=2*pi*(neck_diam/2)*neck_length
#     spine_area=neck_area+head_area
#     spines_area=spine_area*dend_len*spine_in_Micron_density
#     dends_area=np.sum([seg.area() for sec in cell.dend for seg in sec]) #* (1.0/0.7)
#     F_factor=(spines_area+dends_area)/dends_area
#     return F_factor

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


