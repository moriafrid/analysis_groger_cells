import os
from open_pickle import read_from_pickle
import sys
folder_=""
if len(sys.argv) != 2:
    # folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
    cells_name_place="cells_name2.p"
    print("run_execute_main not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_main running with sys.argv",sys.argv)

cells=read_from_pickle(cells_name_place)
print("Remaind to choose the right syn")
folder_data="cells_initial_information"
folder_save="cells_outputs_data_short"
for cell_name in cells:
    # command="sbatch execute_main.sh"
    # send_command = " ".join([command, cell_name,folder_, folder_data , folder_save])
    command= "python main_cell_data.py"
    send_command = " ".join([command, cell_name])
    print(cell_name+str(' :run main_cell_data.py'))
    os.system(send_command)
print("Remaind to choose the right syn")
