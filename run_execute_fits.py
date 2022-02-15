import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read='ASC'
resize_diam_by=1
shrinkage_factor=1
for cell_name in cells:
    for file_type in file_type2read:
        command="sbatch execute_initial_condition.sh"
        send_command = " ".join([command, cell_name,file_type2read,resize_diam_by,shrinkage_factor,folder_])
        os.system(send_command)

        # command="sbatch best_with_const_param.sh"
        # send_command = " ".join([command, cell_name,file_type2read,resize_diam_by,shrinkage_factor,folder_])
        # os.system(send_command)
