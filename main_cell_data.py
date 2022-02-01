# from correct_noise import clear_noise
import os

from split_data import split2phenomena


if __name__ == '__main__':
    # cell = sys.argv[1]
    cell="2017_03_04_A_6-7"
    print(cell,flush=True)

    #### creat the data

    folder_ = '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'  # moria
    split2phenomena(inputs_folder=os.path.join(folder_, 'cells_initial_information', cell),
                    outputs_folder=os.path.join(folder_, 'cells_outputs_data', cell),
                    important_outputs_folder=os.path.join(folder_, 'cells_important_outputs_data', cell),)

    os.system(" ".join(["cell_properties.py ",cell,"/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/","cells_initial_information","cells_outputs_data"]))
    # Rin_Rm_plot.py
    # SMAQ_analysis.py
    # dendogram.py
    # attenuations.py
