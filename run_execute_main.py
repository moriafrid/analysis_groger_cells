import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]

for cell_name in cells:
    command="sbatch execute_main.sh"
    send_command = " ".join([command, cell_name,folder_, folder_data , folder_save])
    print(cell_name+str(' :run main_cell_data.py'))
    os.system(send_command)
print("Remaind to choose the right syn")
