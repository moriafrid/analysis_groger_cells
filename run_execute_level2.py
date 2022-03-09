import os
import json
folder_="/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/"
folder_data="cells_initial_information"
folder_save="cells_outputs_data"
cells=["2017_05_08_A_5-4", "2017_05_08_A_4-5","2017_03_04_A_6-7"]
file_type2read=['hoc','ASC']
resize_diam_by=str(1)
shrinkage_factor=str(1)
passive_val={'RA':100,'CM':2,'RM':10000}
def get_passive_val(passive_val_dict):
    RA=passive_val_dict['RA']
    CM=passive_val_dict['CM']
    RM=passive_val_dict['RM']
    return str(RA),str(CM),str(RM)
RA,CM,RM=get_passive_val(passive_val)
passive_vals_list=[]
passive_vals_list['RA=120']=
passive_vals_list['RA=150']=
passive_vals_list['RA_min']=
passive_vals_list['RA_best_fit']=

for name in passive_vals_list.keys():
    RA,CM,RM=get_passive_val(passive_vals_list[name])
print(passive_val)
for cell_name in cells:
    print(cell_name)
    for file_type in ['hoc','ASC']:
        command="sbatch execute_level2.sh"
        send_command = " ".join([command, cell_name,file_type,RA,CM,RM,name,resize_diam_by,shrinkage_factor,folder_])
        os.system(send_command)
        print(cell_name+ ' .'+file_type+': execute level2.py, dendogram.py, Rin_Rm.py')
        for syn_injection in ['True','False']:
            os.system(" ".join(['sbatch execute_python_script.sh', 'attenuations.py', cell_name,file_type,RA,CM,RM,name,syn_injection,resize_diam_by,shrinkage_factor,folder_]))
            print('execute level2 runing dendogram.py and Rin_Rm.py')
            if eval(syn_injection):
                print(cell_name+ ' .'+file_type+': attenuations.py with syn injection')
            else:
                print(cell_name+ ' .'+file_type+': attenuations.py with current injection')



