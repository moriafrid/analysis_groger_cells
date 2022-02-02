# from correct_noise import clear_noise
import os
import sys
from split_data import split2phenomena


if __name__ == '__main__':
    # cell = sys.argv[1]
    # folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    # data_dir = sys.argv[3] #cells_initial_information
    # save_dir =sys.argv[4] #cells_outputs_data
    cell="2017_05_08_A_5-4"
    folder_= '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir = 'cells_initial_information'
    save_dir = 'cells_outputs_data'
    print(cell,flush=True)

    #### creat the data

    folder_ = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'  # moria
    split2phenomena(cell,inputs_folder=os.path.join(folder_, data_dir, cell),
                    outputs_folder=os.path.join(folder_, save_dir, cell),
                    important_outputs_folder=os.path.join(folder_, 'cells_important_outputs_data', cell),)

    # os.system(" ".join(["cell_properties.py ",cell,"/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/","cells_initial_information","cells_outputs_data"]))
    # Rin_Rm_plot.py
    # SMAQ_analysis.py
    # dendogram.py
    # attenuations.py
