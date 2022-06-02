from glob import glob
from extra_function import load_ASC, load_swc
from neuron import h
from open_pickle import read_from_pickle
file=['ASC','z_correct.swc']
path=glob('cells_initial_information/*/*.ASC')
path1=glob('cells_initial_information/*/*z_correct.swc')
for cell_name in read_from_pickle('cells_name2.p')[-1:]:
    path=glob('cells_initial_information/'+cell_name+'/*.ASC')[0]
    path1=glob('cells_initial_information/'+cell_name+'/*z_correct.swc')[0]
    if '(0)' in path: continue
    print(cell_name)
    cell=None
    cell=load_ASC(path)
    h.PlotShape()
    print('len ASC dend',len(cell.dend))
    print(sum([sec.L for sec in cell.dend]))
    a=1

    cell=None
    cell=load_swc(path1)
    print('len z_correct.swc dend',len(cell.dend))
    print(sum([sec.L for sec in cell.dend]))

    a=1
