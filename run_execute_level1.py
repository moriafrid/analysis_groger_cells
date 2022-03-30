import os
from open_pickle import read_from_pickle
import sys
if len(sys.argv) != 2:
    cells_name_place="cells_name.p"
    print("run_execute_level1.py not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_level1.py running with sys.argv",sys.argv)

file_type='ASC'
os.system(" ".join(['sbatch execute_python_script.sh', 'calculate_synaptic_loc.py',cells_name_place,file_type,'True']))
print('calculate_synaptic_loc.py for all cells in ',cells_name_place )

for cell_name in read_from_pickle(cells_name_place):
    for file_type in ['z_correct.swc','morphology.swc']:
        command="sbatch execute_python_script.sh cell_properties.py"
        # command="python cell_properties.py"
        send_command = " ".join([command,cell_name,file_type])
        os.system(send_command)
        print(cell_name+'_'+file_type+' :run cell_properties.py')
print('')
print('*execute_level1.sh isnt run beacouse empty except SMAQ_analysis.py')
print('**remainder: calculate_tau_m.py and choose_peelingg.py need to be run from the computer')

