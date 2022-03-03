from neuron import gui,h
import pandas as pd
from read_spine_properties import get_n_spinese,get_building_spine
#get spines prameters and creat spine:
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

for sec in cell.all_sec():
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
sp = h.PlotShape()
sp.show(0)  # show diameters
sp.color(2, sec=spine_sec )

#creat stimulus
clamp=[]
syn_shape=[]
Rin_dend,Rin_syn=[],[]
    imp = h.Impedance(sec=spine_head)
    imp.loc(1, sec=spine_head)
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_syn.ppend( imp.input(1, spine_head))

    imp.append(h.Impedance(sec=spines_sec[i]))
    imp[i].loc(spines_seg[i], sec=spines_sec[i])
    imp[i].compute(freq)  # check if you need at 10 Hz
    Rin_dend.appen(imp.input(spines_sec[i], sec=spines_seg[i]))

    imp = h.Impedance(sec=soma)
    imp.loc(0.5, sec=soma)
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_soma_0 = imp.input(0.5, sec=soma)

for sec in cell.dend:
    sec.diam = sec.diam*resize_diam_by
if norm_Rin:
    syn=syns[0]
    imp=h.Impedance(sec=spine_head)
    imp.loc(1, sec=spine_head)
    imp.compute(freq) #check if you need at 10 Hz
    Rin_syn_resize_dend = imp.input(1, sec=spine_head)

    imp=h.Impedance(sec=spine_sec)
    imp.loc(spine_seg, sec=spine_sec)
    imp.compute(freq) #check if you need at 10 Hz
    Rin_dend_resize_dend = imp.input(spine_seg, sec=spine_sec)

    imp = h.Impedance(sec=soma)
    imp.loc(0.5, sec=soma)
    imp.compute(freq)  # check if you need at 10 Hz
    Rin_soma_resize_dend = imp.input(0.5, sec=soma)
