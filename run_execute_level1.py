import os
from glob import glob
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data_short"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['z_correct.swc','morphology.swc','old.ASC','old.hoc','new.ASC','new.hoc']

for file_type in file_type2read:
    if 'ASC' in file_type:
        os.system(" ".join(['sbatch execute_python_script.sh', 'calculate_synaptic_loc.py',cells[0],cells[1],cells[2],file_type,folder_,'True']))
        print('calculate_synaptic_loc.py for',cells )
        # os.system(" ".join(['sbatch execute_python_script.sh', 'plot_neuron_3D.py',cell_name,folder_]))
        print('plot_neuron_3D.py',cells[0],cells[1],cells[2],file_type,folder_)
for cell_name in cells:
    for file_type in file_type2read:
        if len(glob('cells_initial_information/'+cell_name+'/*'+file_type))<1:
            print(cell_name,file_type, ' is continue')
            continue
        for file_type in file_type2read:
            command="sbatch execute_python_script.sh"
            command="python cell_properties.py"
            send_command = " ".join([command,"cell_properties.py" ,cell_name,file_type,folder_, folder_data , folder_save])
            # os.system(send_command)
            print(cell_name+'_'+file_type+' :run cell_properties.py')
print('')
print('execute_level1 isnt run beacouse empty except SMAQ_analysis.py')
print('**remainder: calculate_tau_m.py and choose_peelingg.py need to be run from the computer')

