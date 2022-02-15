import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['ASC','hoc']

for cell_name in cells:
    for file_type in file_type2read:
        command="sbatch execute_main.sh"
        send_command = " ".join([command, cell_name,file_type,folder_, folder_data , folder_save])
        os.system(send_command)
        print(cell_name+str(' :run execute_level1.sh'))

print("cell_properties.py, find_synaptic_loc.py, plot_neuron_3D.py, Rin_Rm_plot.py, find_Rinput.py")
