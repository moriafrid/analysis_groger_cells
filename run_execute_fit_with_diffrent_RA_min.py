import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read='ASC'
resize_diam_by=str(1)
shrinkage_factor=str(1)
SPINE_START=20
for cell_name in cells:
    for file_type2read in ['ASC','hoc']:
        for RA_min in [0,50,100,150,200]:
                command="sbatch execute_fit_with_diffrent_RA_min.sh"
                send_command = " ".join([command, cell_name,file_type2read,resize_diam_by,shrinkage_factor,str(RA_min),str(SPINE_START)folder_])
                os.system(send_command)
                print(cell_name+':fit_with_diffrent_RA_min.py RA_min='+str(RA_min))

