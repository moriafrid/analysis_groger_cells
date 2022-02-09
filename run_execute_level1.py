import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read='ASC'

for cell in cells:
    command="sbatch execute_main.sh"
    send_command = " ".join([command, cell,file_type2read,folder_, folder_data , folder_save])
    os.system(send_command)
