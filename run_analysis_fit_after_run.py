from open_pickle import read_from_pickle
import os

resize_diam_by = str(1.0) #how much the cell sweel during the electrophisiology records
shrinkage_factor =str(1.0) #how much srinkage the cell get between electrophysiology record and LM
folder_= '/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
file_type2read=['z_correct.swc','morphology.swc','ASC','hoc']
cells=read_from_pickle('cells_name.p')
SPINE_STARTs=[str(20),str(60),str(10)]
for cell_name in cells[0:1]:
    print(cell_name)
    for file_type in file_type2read:
        for SPINE_START in SPINE_STARTs: #SPINE_STARTs
            jobid=os.system(" ".join(['sbatch execute_python_script.sh', 'analysis_fit_after_run.py',cell_name,file_type,resize_diam_by,shrinkage_factor,SPINE_START,folder_]))
            # jobid=os.system(" ".join(['python', 'analysis_fit_after_run.py',cell_name,file_type,resize_diam_by,shrinkage_factor,SPINE_START,folder_]))

            print(file_type)
