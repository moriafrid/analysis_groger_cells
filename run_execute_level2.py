import os
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
resize_diam_by=str(1.0)
shrinkage_factor=str(1.0)
os.system('python run_analysis_fit_after_run.py')
SPINE_START=str(20)
for cell_name in [cells[2]]:
    print(cell_name)
    for fit_condition in ['const_param','different_initial_conditions']:
        print(fit_condition)
        for file_type in ['ASC','hoc']:
            passive_vals_dict= {}
            if fit_condition=='const_param':
                passive_val_total=read_from_pickle(glob(folder_+folder_save+cell_name+'/fit_short_pulse_'+file_type+'/dend*'+resize_diam_by+'&F_shrinkage='+shrinkage_factor+'/'+fit_condition+'/RA/analysis/RA_total_errors_minimums.p')[0])
            if fit_condition=='different_initial_conditions':
                passive_val_total=read_from_pickle(glob(folder_+folder_save+cell_name+'/fit_short_pulse_'+file_type+'/dend*'+resize_diam_by+'&F_shrinkage='+shrinkage_factor+'/'+fit_condition+'/RA0_100:300:2+RA0_50:100:0.5/RA_total_errors_minimums.p')[0])
            passive_vals_dict['RA=120']=found(passive_val_total,120)
            passive_vals_dict['RA=150']=found(passive_val_total,150)
            passive_vals_dict['RA_min_error']=passive_val_total[0]
            passive_vals_dict['min_CM']=found_min_parameter(passive_val_total,parameter='CM')
            passive_vals_dict['RA_best_fit']=found_best_RA(passive_val_total)
            passive_vals_dict['mean_best_10']=mean_best_n(passive_val_total,10)

            for name in passive_vals_dict.keys():
                if passive_vals_dict[name] is None:
                    print(name +"+-20 isn't found")
                    continue
                RA,CM,RM=get_passive_val(passive_vals_dict[name])
                command="sbatch execute_level2.sh"
                send_command = " ".join([command, cell_name,file_type,RA,CM,RM,name,resize_diam_by,shrinkage_factor,SPINE_START,folder_])
                os.system(send_command)
                print(cell_name+ ' .'+file_type+': execute level2.py, dendogram.py, Rin_Rm.py')
                for syn_injection in ['True','False']:
                    os.system(" ".join(['sbatch execute_python_script.sh', 'attenuations.py', cell_name,file_type,RA,CM,RM,name,syn_injection,resize_diam_by,shrinkage_factor,SPINE_START,folder_]))
                    print('execute level2 runing analysis_after_run.py dendogram.py and Rin_Rm.py')
                    if eval(syn_injection):
                        print(cell_name+ ' .'+file_type+': attenuations.py with syn injection')
                    else:
                        print(cell_name+ ' .'+file_type+': attenuations.py with current injection')



