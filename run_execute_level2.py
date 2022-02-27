import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['hoc','ASC']
resize_diam_by=str(1)
shrinkage_factor=str(1)
passive_val={'RA':100,'CM':1,'RM':10000}

for cell_name in cells:
    for file_type in ['hoc','ASC']:
        command="sbatch execute_level2.sh"
        send_command = " ".join([command, cell_name,file_type,passive_val,resize_diam_by,shrinkage_factor,folder_])
        os.system(send_command)
        print(cell_name+ ' .'+file_type+': analysis_fit_after_run.py')
        os.system(" ".join(['sbatch execute_python_script.sh', 'attenuations.py', cell_name,file_type,passive_val,resize_diam_by,shrinkage_factor,folder_]))


