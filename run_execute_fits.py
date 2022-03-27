import os
import time
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
resize_diam_by=str(1.1)
shrinkage_factor=str(1.1)
SPINE_STARTs=[10,20,60]
base_command='sbatch execute_python_script.sh'
for cell_name in ["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]:
    for file_type in ['z_correct.swc','morphology.swc','hoc','ASC'][:2]:
        for SPINE_START in [20]:#SPINE_STARTs:
            for Ra_min in [5,100]:
                command="fit_influnce_by_initial_condition.py"
                send_command = " ".join([base_command,command, cell_name,file_type,str(Ra_min),resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
                # os.system(send_command)
                # time.sleep(5)
                print(cell_name+ ' .'+file_type+': fit_influance_by_initial_condition.py with ra_min='+str(Ra_min))
            command2="sbatch execute_fit_const.sh"
            command2="python fit_best_with_const_param.py"
            send_command = " ".join([command2, cell_name,file_type,resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
            os.system(send_command)
            # time.sleep(10)
            print(cell_name+ ' .'+file_type+': fit_best_with_const_param.py')

            # for RA_min in [0,50,100,150,200]:
            #     command="fit_with_diffrent_RA_min.py"
            #     send_command = " ".join([base_command,command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(RA_min),str(SPINE_START),folder_])
            #     os.system(send_command)
            #     print(cell_name+':fit_with_diffrent_RA_min.py RA_min='+str(RA_min))
            #
            #
            # for add2delay  in [0,1,2,3,4,5,6,7,8]:
            #     for add2fit  in range(0,20,2):
            #         command="fit_with_diffrent_time_delay.sh"
            #         send_command = " ".join([base_command,command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(add2delay),str(add2fit),str(SPINE_START),folder_])
            #         os.system(send_command)
            #         print(cell_name+':fit_with_diffrent_time_delay.py delay='+str(add2delay)+' add fit='+str(add2fit))
