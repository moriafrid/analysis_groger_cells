from extra_function import load_swc
import os
from open_pickle import read_from_pickle
from glob import glob
from calculate_F_factor import calculate_F_factor
import pickle
for cell_name in read_from_pickle('cells_name.p'):
    for old_dirr in glob('cells_outputs_data_short/'+cell_name+'/MOO_results/z_correct.swc/F_shrinkage=1.0_dend*1.0/const_param/*/hall*.p'):
        new_dirr=old_dirr[:old_dirr.rfind('.')]+'1.p'
        print(new_dirr)
        os.rename(old_dirr,new_dirr)
for cell_name in read_from_pickle('cells_name.p'):
    print(cell_name)
    temp_cell=None
    morphology_dirr=glob('cells_initial_information/2017_03_04_A_6-7(0)/morphology_z_correct.swc')[0]
    temp_cell=load_swc(glob(morphology_dirr[:morphology_dirr.rfind('/')]+'/*'+'z_correct.swc')[0])
    F_factor=calculate_F_factor(temp_cell,'mouse_spine')
    print(F_factor)
    for dirr in glob('cells_outputs_data_short/'+cell_name+'/MOO_results/z_correct.swc/F_shrinkage=1.0_dend*1.0/const_param/*/hall*1.p'):
        base_save_folder=dirr[:dirr.rfind('/')]
        print(base_save_folder)
        dicty=read_from_pickle(dirr)
        dicty["F_factor"]=F_factor
        pickle.dump(dicty
        , open(base_save_folder + "/hall_of_fame.p", "wb"))
