from open_pickle import read_from_pickle
import os
from glob import glob
from passive_val_function import *
import pandas as pd
from read_passive_parameters_csv import get_passive_parameter
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
dataset_jobs_folder='/running'
spine_type='mouse_spine'
in_parallel=False
# in_parallel = sys.argv[1]
# for resize_diam_by in [1,1.2,round(1.0/0.7,4)]:
#     for shrinkage_by in [1,1.2, round(1.0/0.7,4)]:
file_type=['z_correct.swc','morphology.swc'][0]
SPINE_STARTs=[10,20,60]
for cell_name in ['2017_05_08_A_5-4', '2017_05_08_A_4-5', '2017_03_04_A_6-7'][2:3]:
    passive_vals_dict= {}
    p='cells_initial_information/'+cell_name+'/results_passive_fits.csv'
    df = pd.read_csv(p)
    for resize_diam_by ,shrinkage_by in zip([1.0,1.2,1.1][1:],[1.0,1.0,1.1][1:]):
        for fit_condition in ['const_param','different_initial_conditions'][:1]:
            for SPINE_START in [20]:
                passive_vals_dict=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type='z_correct.swc')
                for i, passive_val_name in enumerate(['RA=120','RA=150','RA_min_error','RA_best_fit'][:3]):
                    # if i!=2: continue
                    if passive_vals_dict[passive_val_name] is None:
                        print(passive_val_name +"+-20 isn't found")
                        continue

                    RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
                    print(cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START))
                    if in_parallel:
                        command="sbatch -p ss.q,elsc.q runs_change_passive_val_parallel.sh"
                        send_command = " ".join([command, '30',cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                    else:
                        command="sbatch -p ss.q,elsc.q runs_change_passive_val.sh"
                        send_command = " ".join([command,"1",cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                    print(send_command)
                    os.system(send_command)
