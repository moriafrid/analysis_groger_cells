from open_pickle import read_from_pickle
import os
from glob import glob
from passive_val_function import *
import pandas as pd

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
dataset_jobs_folder='/running'
spine_type='mouse_spine'
in_parallel=True
# in_parallel = sys.argv[1]
# for resize_diam_by in [1,1.2,round(1.0/0.7,4)]:
#     for shrinkage_by in [1,1.2, round(1.0/0.7,4)]:
file_type=['z_correct.swc','morphology.swc'][0]
SPINE_STARTs=[10,20,60]
for cell_name in read_from_pickle('cells_name.p')[0:1]:
    passive_vals_dict= {}
    p='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information/2017_05_08_A_4-5/results_passive_fits.csv'
    df = pd.read_csv(p)
    for resize_diam_by ,shrinkage_by in zip([1],[1]):
        for fit_condition in ['const_param','different_initial_conditions']:
            for SPINE_START in SPINE_STARTs[1:2]:
                #creat the value to run on
                df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type), :].to_dict('records')
                curr = df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type), :]
                passive_vals_dict={}
                for name in curr.parameter_type:
                    passive_vals_dict[name]= curr.loc[df.parameter_type == name,].to_dict('records')[0]

                for i, passive_val_name in enumerate(passive_vals_dict.keys()):
                    if i>0: continue
                    if passive_vals_dict[passive_val_name] is None:
                        print(passive_val_name +"+-20 isn't found")
                        continue
                    RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
                    if in_parallel:
                        command="sbatch -p ss.q runs_change_passive_val_parallel.sh"
                        send_command = " ".join([command, '30',cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                    else:
                        command="sbatch -p ss.q runs_change_passive_val.sh"
                        send_command = " ".join([command,"1",cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                    print(send_command)
                    os.system(send_command)

                # passive_val_name='RA_const'
                # dict_1=read_from_pickle('../data/fit/'+spine_type+'/'+name2run+'/const_param/RA/analysis/RA_const_10_minimums.p')
                # for i,key in enumerate(dict_1.keys()):
                #     if i !=1: continue
                #     if in_parallel:
                #         command="sbatch -p ss.q runs_change_passive_val_parallel.sh"
                #         send_command = " ".join([command, '30',cell_name,RA,CM,RM,str(shrinkage_by),str(resize_diam_by),passive_val_name,folder_])
                #     else:
                #         command="sbatch -p ss.q runs_change_passive_val.sh"
                #         send_command = " ".join([command,"1",cell_name,RA,CM,RM,str(shrinkage_by),str(resize_diam_by),passive_val_name,folder_])
                #
                #     print(send_command)
                #     os.system(send_command)
                # #
