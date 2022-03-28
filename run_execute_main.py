import os
from open_pickle import read_from_pickle
import sys
if len(sys.argv) != 3:
    folder_=""
    # folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
    cells_name_place="cells_name.p"
    print("run_execute not running with sys.argv",len(sys.argv))
else:
    folder_=sys.argv[1]
    cells=sys.argv[2]
    print("run_execute running with sys.argv",sys.argv)

print("Remaind to choose the right syn")
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=read_from_pickle(cells_name_place)
for cell_name in cells:
    command="sbatch execute_main.sh"
    send_command = " ".join([command, cell_name,folder_, folder_data , folder_save])
    print(cell_name+str(' :run main_cell_data.py'))
    os.system(send_command)
print("Remaind to choose the right syn")
