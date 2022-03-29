import os
from passive_val_function import *
from read_passive_parameters_csv import get_passive_parameter


folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
# file_type2read=['hoc','ASC']
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
SPINE_START=str(20)
i=0
    # os.system('python run_analysis_fit_after_run.py')
for cell_name in ["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]:
    print(cell_name)
    all_data = []
    dict_fit_condition={}
    for fit_condition in ['const_param','different_initial_conditions'][0:1]:
        print(fit_condition)
        for file_type in file_type2read:
            for resize_diam_by ,shrinkage_by in zip([1.0,1.2,1.1][1:],[1.0,1.0,1.1][1:]):
                print('shrinkage_factor:',shrinkage_by,'reasize_dend_factor:',resize_diam_by)
                passive_vals_dict=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=int(SPINE_START),file_type=file_type)
                for name in ['RA=120','RA=150','RA_min_error','RA_best_fit']:
                    # if i>1: continue
                    i+=1
                    try: passive_vals_dict[name]
                    except:
                        print('passive_vals_dict is empty')
                        continue
                    RA,CM,RM=get_passive_val(passive_vals_dict[name])
                    print(name,RA,CM,RM)
                    command="sbatch execute_level2.sh"
                    send_command = " ".join([command,cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_by),SPINE_START])
                    os.system(send_command)
                    print(cell_name+ ' .'+file_type+': execute level2.py, dendogram.py, Rin_Rm.py','attenuations.py')


                    # command='sbatch execute_python_script.sh'
                    # command='python'

                    #
                    # send_command = " ".join([command, 'Rin_Rm_plot.py',cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START])
                    # os.system(send_command)
                    # print(cell_name+ ' .'+file_type+':  Rin_Rm_plot.py')

                    # send_command = " ".join([command, 'dendogram.py',cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START])
                    # # os.system(send_command)
                    # print(cell_name+ ' .'+file_type+':  dendogram.py')
                    #
                    # for syn_injection in ['True','False']:
                    #     os.system(" ".join([command, 'attenuations.py', cell_name,file_type,fit_condition,name,syn_injection,str(resize_diam_by),str(shrinkage_factor),SPINE_START]))
                    #     print('execute level2 runing analysis_after_run.py dendogram.py and Rin_Rm.py')
                    #     if eval(syn_injection):
                    #         print(cell_name+ ' '+file_type+': attenuations.py with syn injection')
                    #     else:
                    #         print(cell_name+ ' '+file_type+': attenuations.py with current injection')



