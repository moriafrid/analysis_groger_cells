import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['corretc_z.swc','morphology.swc','ASC','hoc']

for cell_name in cells:
    os.system(" ".join(['sbatch execute_python_script.sh', 'calculate_synaptic_loc.py',cell_name,folder_,'True']))
    print('calculate_synaptic_loc.py',cell_name )
    os.system(" ".join(['sbatch execute_python_script.sh', 'plot_neuron_3D.py',cell_name,folder_]))
    print('plot_neuron_3D.py',cell_name)
# os.system(" ".join(['sbatch execute_python_script.sh', 'calculate_tau_m.py',"2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7",folder_]))
# print('calculate_tau_m.py')
# os.system(" ".join(['sbatch execute_python_script.sh', 'calculate_tau_m.py']))
for cell_name in cells:
    for file_type in file_type2read:
        command="sbatch execute_level1.sh"
        send_command = " ".join([command, cell_name,file_type,folder_, folder_data , folder_save])
        os.system(send_command)
        print(cell_name+str(' :run execute_level1.sh'))


print("execute_level1 running: cell_properties.py,  Rin_Rm_plot.py")
print('')
print('**remainder: calculate_tau_m.py and choose_peelingg.py need to be run from the computer')
