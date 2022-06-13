# from correct_noise import clear_noise
import os
import sys
from split_data import split2phenomena


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) != 2:
        cell_name= '2017_04_03_B'
        print('main dont run with sys.argv len is '+str(len(sys.argv)))
    else:
        cell_name = sys.argv[1]
        print(cell_name,flush=True)
    folder_=""
    data_dir= "cells_initial_information"
    save_dir = "cells_outputs_data_short"
    split2phenomena(cell_name,inputs_folder=os.path.join(folder_, data_dir, cell_name),
                    outputs_folder=os.path.join(folder_, save_dir, cell_name))
