from open_pickle import read_from_pickle
import os

resize_diam_by = str(1.0) #how much the cell sweel during the electrophisiology records
shrinkage_factor =str(1.0) #how much srinkage the cell get between electrophysiology record and LM
folder_= '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
file_type2read=['z_corretc.swc','morphology.swc','.ASC','.hoc']
cells=read_from_pickle('cells_name.p')
SPINE_START=str(20)
for cell_name in cells:
    for file_type in file_type2read:
        os.system(" ".join(['sbatch execute_python_script.sh', 'analysis_after_run.py',cell_name,file_type,resize_diam_by,shrinkage_factor,SPINE_START,folder_]))
