from glob import glob
from extra_function import load_ASC, load_swc
from neuron import h
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg
for cell_name in read_from_pickle('cells_name2.p')[0:]:
    path=glob('cells_initial_information/'+cell_name+'/*.ASC')[0]
    path1=glob('cells_initial_information/'+cell_name+'/*.ASC')[1]
    print(cell_name)

    cell=load_ASC(path)

    print(cell_name)
    cell=None
    cell=load_ASC(path)
    h.PlotShape()
    print('len ASC dend',len(cell.dend))
    print(sum([sec.L for sec in cell.dend]))
