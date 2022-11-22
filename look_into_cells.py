import pickle
from glob import glob
from neuron import h
from extra_function import load_ASC, load_swc
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg
for cell_name in read_from_pickle('cells_name2.p')[8:]:
    path1=glob('cells_initial_information/'+cell_name+'/*shrinkXYZ.ASC')[0]
    cell=load_ASC(path1)
    print(cell_name)
    dicty={}
    path=glob('cells_initial_information/'+cell_name+'/*after_shrink.swc')[0]
    print(cell_name)
    cell=None
    cell=load_swc(path)
    i=0
    for sec,seg in zip(get_sec_and_seg(cell_name,file_type='swc',from_picture=cell_name in read_from_pickle('cells_sec_from_picture.p'))[0],get_sec_and_seg(cell_name,file_type='swc',from_picture=cell_name in read_from_pickle('cells_sec_from_picture.p'))[1]):
        print(h.distance(cell.soma(0.5),eval('cell.'+sec)(seg)))
        dicty['syn'+str(i)+'_distance']=h.distance(cell.soma(0.5),eval('cell.'+sec)(seg))
        i+=1
    dicty['total_L']=sum([sec.L for sec in cell.dend])
    # for sec,seg in zip(get_sec_and_seg(cell_name,file_type='ASC',from_picture=False)[0],get_sec_and_seg(cell_name,file_type='ASC',from_picture=False)[1]):
    #     print(h.distance(cell.soma(0.5),eval('cell.'+sec)(seg)))
    #
    # path=glob('cells_initial_information/'+cell_name+'/morphology.swc')[0]
    # cell=None
    # cell=load_swc(path)
    # h.distance(0,0.5,cell.soma)
    #
    # for sec,seg in zip(get_sec_and_seg(cell_name,file_type='swc',from_picture=False)[0],get_sec_and_seg(cell_name,file_type='swc',from_picture=False)[1]):
    #     print(h.distance(eval('cell.'+sec)(seg)))
    #
    # for sec,seg in zip(get_sec_and_seg(cell_name,file_type='swc',from_picture=True)[0],get_sec_and_seg(cell_name,file_type='swc',from_picture=True)[1]):
    #     print(h.distance(cell.soma(0.5),eval('cell.'+sec)(seg)))
    #
    # path=glob('cells_initial_information/'+cell_name+'/*after_shrink.swc')[0]
    # print(cell_name)
    # cell=None
    # cell=load_swc(path)
    # i=0
    # for sec,seg in zip(get_sec_and_seg(cell_name,file_type='swc',from_picture=cell_name in read_from_pickle('cells_sec_from_picture.p'))[0],get_sec_and_seg(cell_name,file_type='swc',from_picture=cell_name in read_from_pickle('cells_sec_from_picture.p')[1])):
    #     print(h.distance(cell.soma(0.5),eval('cell.'+sec)(seg)))
    #     dicty['syn'+str(i)+'_distance']
    #     i+=1
    # path=glob('cells_initial_information/'+cell_name+'/*before_shrink.swc')[0]
    # print(cell_name)
    # cell=None
    # cell=load_swc(path)
    # for sec,seg in zip(get_sec_and_seg(cell_name,file_type='swc',before_after='_before_shrink',from_picture=False)[0],get_sec_and_seg(cell_name,file_type='swc',from_picture=False)[1]):
    #     print(h.distance(cell.soma(0.5),eval('cell.'+sec)(seg)))
    # h.PlotShape()

    print('len ASC dend',len(cell.dend))
    print(sum([sec.L for sec in cell.dend]))
    pickle.dump(dicty, open('cells_initial_information/'+cell_name+'/cell_parameters_pickles.p', 'wb'))
    a=1
