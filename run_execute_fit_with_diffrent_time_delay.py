import os

folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read='ASC'
resize_diam_by=str(1)
shrinkage_factor=str(1)

for cell_name in [cells[1]]:
    for add2delay  in [0,1,2,3,4,5,6,7,8]:
        for add2fit  in range(0,20,2):
            command="sbatch execute_fit_with_diffrent_time_delay.sh"
            send_command = " ".join([command, cell_name,'ASC',resize_diam_by,shrinkage_factor,str(add2delay),str(add2fit),folder_])
            os.system(send_command)
            print(':fit_with_diffrent_time_delay.py delay='+str(add2delay)+' add fit='+str(add2fit))
