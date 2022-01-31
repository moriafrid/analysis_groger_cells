# from correct_noise import clear_noise
import sys
import os
from clear_noises import clear_noise
from split_data import split2phenomena
from find_Rinput import find_Rinput
from check_dynamics import check_dynamics
from open_pickle import read_from_pickle

if __name__ == '__main__':
    # cell = sys.argv[1]
    cell="2017_05_08_A_4-5"
    #### creat the data

    folder_ = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'  # moria
    split2phenomena(inputs_folder=os.path.join(folder_, 'cells_initial_information', cell),
                    important_outputs_folder=os.path.join(folder_, 'cells_important_outputs_data', cell),
                    all_outputs_folder=os.path.join(folder_, 'cells_outputs_data', cell))

    #### find the fit for Rm
    # folder_iv_curves = folder_data+'traces_img/2017_05_08_A_0006/'
    # R, Rinput_list = find_Rinput(folder_iv_curves)

    # found the nueron property
