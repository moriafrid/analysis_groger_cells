import os
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['hoc','ASC']
resize_diam_by=str(1)
shrinkage_factor=str(1)
SPINE_START=20
for cell_name in cells:
    for file_type in ['z_correct.swc','morphology.swc','hoc','ASC']:
        command="sbatch execute_initial_condition.sh"
        send_command = " ".join([command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
        os.system(send_command)
        print(cell_name+ ' .'+file_type+': fit_influance_by_initial_condition.py')
        command="sbatch execute_const_param.sh"
        send_command = " ".join([command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
        os.system(send_command)
        print(cell_name+ ' .'+file_type+': best_with_const_param.py')

        # for RA_min in [0,50,100,150,200]:
        #     command="sbatch execute_fit_with_diffrent_RA_min.sh"
        #     send_command = " ".join([command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(RA_min),str(SPINE_START),folder_])
        #     os.system(send_command)
        #     print(cell_name+':fit_with_diffrent_RA_min.py RA_min='+str(RA_min))
        #
        #
        # for add2delay  in [0,1,2,3,4,5,6,7,8]:
        #     for add2fit  in range(0,20,2):
        #         command="sbatch execute_fit_with_diffrent_time_delay.sh"
        #         send_command = " ".join([command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(add2delay),str(add2fit),str(SPINE_START),folder_])
        #         os.system(send_command)
        #         print(cell_name+':fit_with_diffrent_time_delay.py delay='+str(add2delay)+' add fit='+str(add2fit))
