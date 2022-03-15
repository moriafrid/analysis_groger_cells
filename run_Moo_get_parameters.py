from open_pickle import read_from_pickle
import os
from glob import glob
from passive_val_function import *
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data/"
dataset_jobs_folder='/running'
spine_type='mouse_spine'
in_parallel=False
# in_parallel = sys.argv[1]
# for resize_diam_by in [1,1.2,round(1.0/0.7,4)]:
#     for shrinkage_by in [1,1.2, round(1.0/0.7,4)]:
file_type=['z_correct.swc','morphology.swc']
for cell_name in read_from_pickle('cells_name.p'):
    for resize_diam_by ,shrinkage_by in zip([1],[1]):
        for fit_condition in ['const_param','different_initial_conditions']:
            name2run='F_shrinkage='+str(round(shrinkage_by,2))+'_dend*'+str(round(resize_diam_by,2))
            passive_val_name='RA_initial'

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

            for i,key in enumerate(dict_1.keys()):
                if i !=1: continue
                if in_parallel:
                    command="sbatch -p ss.q runs_change_passive_val_parallel.sh"
                    send_command = " ".join([command, '30',str(dict_1[key]['RM']),str(round(dict_1[key]['RA'],4)),str(dict_1[key]['CM']),str(resize_diam_by),str(shrinkage_by),passive_val_name])
                else:
                    command="sbatch -p ss.q runs_change_passive_val.sh"
                    send_command = " ".join([command,"1",str(dict_1[key]['RM']),str(round(dict_1[key]['RA'],4)),str(dict_1[key]['CM']),str(shrinkage_by),str(resize_diam_by),passive_val_name])
                print(send_command)
                os.system(send_command)
            ##pass 1 argument = size of ipcluster
    #pass 2 argument = RM
    #pass 3 argument = RA
    #pass 4 argument = CM
    #pass 5 argument = shrinkage_by
    #pass 6 argumant = resize_dend_by
    #pass 7 argument = passive_vel_name


            passive_val_name='RA_const'
            dict_1=read_from_pickle('../data/fit/'+spine_type+'/'+name2run+'/const_param/RA/analysis/RA_const_10_minimums.p')
            for i,key in enumerate(dict_1.keys()):
                if i !=1: continue
                if in_parallel:
                    command="sbatch -p ss.q runs_change_passive_val_parallel.sh"
                    send_command = " ".join([command, '30',str(dict_1[key]['params']['RM']),str(round(dict_1[key]['params']['RA'],4)),str(dict_1[key]['params']['CM']),str(shrinkage_by),str(resize_diam_by),passive_val_name])
                else:
                    command="sbatch -p ss.q runs_change_passive_val.sh"
                    send_command = " ".join([command,"1",str(dict_1[key]['params']['RM']),str(round(dict_1[key]['params']['RA'],4)),str(dict_1[key]['params']['CM']),str(shrinkage_by),str(resize_diam_by),passive_val_name])

                print(send_command)
                os.system(send_command)
            #
