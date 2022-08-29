import os
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
base="python "
base="sbatch execute_python_script.sh "
for cell_name in read_from_pickle('cells_name2.p'):
    create_folder_dirr('cells_initial_information/'+cell_name+'/dict_morphology/')
    for file_type in [' shrinkXYZ.ASC ',' ASC ']:
        os.system(base+' creat_morphology_dict_ASC.py '+cell_name+file_type)
    for before_after in [' _befor_shrink ',' _after_shrink ']:
        os.system(base+' creat_morphology_dict_swc.py '+cell_name+file_type)




