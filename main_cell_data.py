# from correct_noise import clear_noise
import os
import sys
from split_data import split2phenomena


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) != 5:
        cell_name= '2017_03_04_A_6-7'
        folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
        data_dir= "cells_initial_information"
        save_dir ="cells_outputs_data"
    else:
        cell_name = sys.argv[1]
        folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
        data_dir = sys.argv[3] #cells_initial_information
        save_dir =sys.argv[4] #cells_outputs_data
        print(cell_name,flush=True)

    split2phenomena(cell_name,inputs_folder=os.path.join(folder_, data_dir, cell_name),
                    outputs_folder=os.path.join(folder_, save_dir, cell_name))

    # os.system(" ".join(["cell_properties.py ",cell,"/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/","cells_initial_information","cells_outputs_data"]))
    # Rin_Rm_plot.py
    # SMAQ_analysis.py
    # dendogram.py
    # attenuations.py
