# from correct_noise import clear_noise
import os
import sys
from split_data import split2phenomena
from open_pickle import read_from_pickle

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) != 4:
        cell_name= '2016_04_16_A' #'2017_03_04_A_6-7'
        data_dir= "cells_initial_information"
        save_dir = "cells_outputs_data_short"
        print('main dont run with sys.argv len is '+str(len(sys.argv)))
    else:
        cell_name = sys.argv[1]
        print(cell_name,flush=True)
        data_dir=sys.argv[2]
        save_dir=sys.argv[3]
    folder_=""
    # split2phenomena(cell_name,inputs_folder=os.path.join(folder_, data_dir, cell_name),
    #             outputs_folder=os.path.join(folder_, save_dir, cell_name))
    for cell_name in read_from_pickle('cells_name2.p'):
        split2phenomena(cell_name,inputs_folder=os.path.join(folder_, data_dir, cell_name),
                        outputs_folder=os.path.join(folder_, save_dir, cell_name))
