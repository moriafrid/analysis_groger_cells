import os

import pandas as pd

from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import pickle
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
resize_diam_by=1.0
shrinkage_factor=1.0
SPINE_STARTs=[str(10),str(20),str(60)]
SPINE_START=str(20)
RA_mins=[5,50,80,100]
i=0
# os.system('python run_analysis_fit_after_run.py')
for cell_name in cells:
    print(cell_name)
    all_data = []
    dict_fit_condition={}
    for fit_condition in ['const_param','different_initial_conditions']:
        print(fit_condition)
        for file_type in file_type2read:
            passive_vals_dict= {}
            initial_folder=folder_+folder_save+cell_name+'/fit_short_pulse/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
            # initial_folder=folder_+folder_save+cell_name+'/fit_short_pulse/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
            initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
            initial_folder+='/'+fit_condition
            if fit_condition=='const_param':
                passive_val_total=read_from_pickle(glob(initial_folder+'/RA/analysis/RA_total_errors_minimums.p')[0])
            if fit_condition=='different_initial_conditions':
                passive_val_total=read_from_pickle(glob(initial_folder+'/RA_min'+str(5)+'/analysis/RA_total_errors_minimums.p')[0])
            passive_vals_dict['RA=120']=found(passive_val_total,120)
            passive_vals_dict['RA=150']=found(passive_val_total,150)
            passive_vals_dict['RA_min_error']=passive_val_total[0]
            passive_vals_dict['min_CM']=found_min_parameter(passive_val_total,parameter='CM')
            passive_vals_dict['RA_best_fit']=found_best_RA(passive_val_total)
            passive_vals_dict['mean_best_10']=mean_best_n(passive_val_total,10)
            if fit_condition=='different_initial_conditions' and (passive_vals_dict['RA=120'] is None or passive_vals_dict['RA=150'] is None):
                passive_val_total=read_from_pickle(glob(initial_folder+'/RA_min'+str(100)+'/analysis/RA_total_errors_minimums.p')[0])
                passive_vals_dict['RA=120']=found(passive_val_total,120)
                passive_vals_dict['RA=150']=found(passive_val_total,150)
            dict_fit_condition[fit_condition]={file_type:passive_vals_dict}


            # add flat fields
            for key, value in passive_vals_dict.items():
                dict_for_records = {}
                # add metadata
                dict_for_records['fit_condition'] = fit_condition
                dict_for_records['file_type'] = file_type
                dict_for_records['parameter_type'] = key
                if value is not None:
                    dict_for_records.update(value)
                all_data.append(dict_for_records)


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
                os.system(send_command)
                print(cell_name+ ' .'+file_type+':  Rin_Rm_plot.py')

                send_command = " ".join([command, 'dendogram.py',cell_name,file_type,RA,CM,RM,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_])
                os.system(send_command)
                print(cell_name+ ' .'+file_type+':  dendogram.py')

                for syn_injection in ['True','False']:
                    os.system(" ".join([command, 'attenuations.py', cell_name,file_type,RA,CM,RM,name,syn_injection,str(resize_diam_by),str(shrinkage_factor),SPINE_START,folder_]))
                    print('execute level2 runing analysis_after_run.py dendogram.py and Rin_Rm.py')
                    if eval(syn_injection):
                        print(cell_name+ ' '+file_type+': attenuations.py with syn injection')
                    else:
                        print(cell_name+ ' '+file_type+': attenuations.py with current injection')

    save_pickle_folder=folder_+folder_save+cell_name+'/fit_short_pulse/'
    output_df = pd.DataFrame.from_records(all_data)
    print(output_df.columns)
    print(output_df)
    output_df.to_csv(save_pickle_folder+"/results_passive_fits.csv", index=False)
    pickle.dump(dict_fit_condition, open(save_pickle_folder+"/results_passive_fits.p", "wb"))

    save_pickle_folder2=folder_+folder_data+cell_name
    output_df = pd.DataFrame.from_records(all_data)
    output_df.to_csv(save_pickle_folder2+"/results_passive_fits.csv", index=False)
    pickle.dump(dict_fit_condition, open(save_pickle_folder2+"/results_passive_fits.p", "wb"))


