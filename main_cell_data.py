# from correct_noise import clear_noise
import os
import sys
import cell_properties
from split_data import split2phenomena
from find_Rinput import find_Rinput
from check_dynamics import check_dynamics
from open_pickle import read_from_pickle

if __name__ == '__main__':
    # cell = sys.argv[1]
    cell="2017_03_04_A_6-7"
    print(cell,flush=True)

    #### creat the data

    folder_ = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'  # moria
    split2phenomena(inputs_folder=os.path.join(folder_, 'cells_initial_information', cell),
                    outputs_folder=os.path.join(folder_, 'cells_outputs_data', cell),
                    important_outputs_folder=os.path.join(folder_, 'cells_important_outputs_data', cell),)

    # os.system(" ".join(["cell_properties.py ",cell]))
    # Rin_Rm_plot.py
    # SMAQ_analysis.py
    # dendogram.py
    # attenuations.py
