from neuron import h,gui
from read_passive_parameters_csv import get_passive_parameter
from glob import glob
from extra_function import load_swc, load_ASC,load_hoc
from calculate_F_factor import calculate_F_factor
import pandas as pd
from read_spine_properties import get_n_spinese,get_building_spine

folder_=''
data_dir='cells_initial_information/'
save_dir = "cells_outputs_data_short/"

file_type='z_correct.swc'
cell_name='2017_05_08_A_4-5'
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]

def create_spine( icell, sec, seg, number=0, neck_diam=0.25, neck_length=1.35,head_diam=0.944):
    neck = h.Section(name="spineNeck" + str(number))
    head = h.Section(name="spineHead" + str(number))
    neck.L = neck_length
    neck.diam = neck_diam
    head.diam = head_diam
    head.L = head_diam
    head.connect(neck(1))
    neck.connect(sec(seg))
    h("access " + str(neck.hoc_internal_name()))
    icell.add_sec(neck)
    h.pop_section() #?# moria understand if and why this is important
    h("access " + str(head.hoc_internal_name()))
    icell.add_sec(head)
    h.pop_section()

    # for sec in [neck, head]:
    #     sec.insert("pas")
    # neck.g_pas = 1.0 / passive_val["RM"]
    # neck.cm= passive_val["CM"]
    # neck.Ra=passive_val["RA"]#int(Rneck)
    return icell,[neck, head]

def add_morph(cell, syn,spine_property,number=0):
    cell,spine=create_spine(cell, syn[0],syn[1] ,number=number, neck_diam=spine_property['NECK_DIAM'], neck_length=spine_property['NECK_LENGHT'],head_diam=spine_property['HEAD_DIAM'])
    return cell,spine

cell=None
if file_type=='ASC':
    cell =load_ASC(cell_file)
elif file_type=='hoc':
    cell =load_hoc(cell_file)
elif 'swc' in file_type:
    cell =load_swc(cell_file)

F_factor=calculate_F_factor(cell,'mouse_spine')
soma = cell.soma
# h.celsius = 36
sp = h.PlotShape()

dict_syn=pd.read_excel(folder_+save_dir+"synaptic_location_seperate.xlsx",index_col=0)
syns,spines,spines_sec,spines_seg,spines_head=[],[],[],[],[]
number_of_spine= get_n_spinese(cell_name)
for spine_num in range(number_of_spine):
    spine_seg=dict_syn[cell_name+str(spine_num)]['seg_num']
    spine_sec=eval('cell.'+dict_syn[cell_name+str(spine_num)]['sec_name'])
    syns.append([spine_sec,spine_seg])
    spines_sec.append(spine_sec)
    spines_seg.append(spine_seg)
    spines_property=get_building_spine(cell_name,spine_num)
    cell,[spine_neck, spine_head]=add_morph(cell, [spine_sec,spine_seg] ,get_building_spine(cell_name,spine_num),number=spine_num)
    spines.append([spine_neck, spine_head])
    spines_head.append(spine_head)
    sp.show(0)  # show diameters
    sp.color(2, sec=spine_sec )
for sec in cell.all_sec():
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
sp = h.PlotShape()
a=1
