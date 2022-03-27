import os
import pandas as pd
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import pickle
from read_passive_parameters_csv import get_passive_parameter

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
# file_type2read=['hoc','ASC']
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
resize_diam_by=1.2
shrinkage_factor=1.0
SPINE_STARTs=[str(10),str(20),str(60)]
SPINE_START=str(20)
i=0
    # os.system('python run_analysis_fit_after_run.py')
for cell_name in cells:
    print(cell_name)
    all_data = []
    dict_fit_condition={}
    for fit_condition in ['const_param','different_initial_conditions'][0:1]:
        print(fit_condition)
        for file_type in file_type2read:
            print(file_type)
            passive_vals_dict=get_passive_parameter(cell_name,spine_start=int(SPINE_START),fit_condition=fit_condition,file_type=file_type)
            for name in passive_vals_dict.keys():
                # if i>0: continue
                i+=1
                if passive_vals_dict[name] is None:
                    print(name +"+-20 isn't found")
                    continue
                RA,CM,RM=get_passive_val(passive_vals_dict[name])
                print(name,RA,CM,RM)
                # command="sbatch execute_level2.sh"
                # send_command = " ".join([command,cell_name,file_type,RA,CM,RM,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_])
                # print(cell_name+ ' .'+file_type+': execute level2.py, dendogram.py, Rin_Rm.py')

                command='sbatch execute_python_script.sh'

                send_command = " ".join([command, 'Rin_Rm_plot.py',cell_name,file_type,RA,CM,RM,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_])
                # os.system(send_command)
                print(cell_name+ ' .'+file_type+':  Rin_Rm_plot.py')

                send_command = " ".join([command, 'dendogram.py',cell_name,file_type,RA,CM,RM,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_])
                # os.system(send_command)
                print(cell_name+ ' .'+file_type+':  dendogram.py')

                for syn_injection in ['True','False']:
                    os.system(" ".join([command, 'attenuations.py', cell_name,file_type,RA,CM,RM,name,syn_injection,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_]))
                    print('execute level2 runing analysis_after_run.py dendogram.py and Rin_Rm.py')
                    if eval(syn_injection):
                        print(cell_name+ ' '+file_type+': attenuations.py with syn injection')
                    else:
                        print(cell_name+ ' '+file_type+': attenuations.py with current injection')



