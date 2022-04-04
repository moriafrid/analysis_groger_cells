from open_pickle import read_from_pickle
import os
from glob import glob
from passive_val_function import *
import pandas as pd
from read_passive_parameters_csv import get_passive_parameter
import sys
from open_pickle import read_from_pickle
if len(sys.argv) != 3:
    cells_name_place="cells_name.p"
    in_parallel=False
    print("run_Moo_get_parameters not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    in_parallel=sys.argv[2]
    print("run_Moo_get_parameters running with sys.argv",sys.argv)
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"

os.system('python csv_for_passive_val_results.py')

file_types=['z_correct.swc','morphology.swc'][:1]
SPINE_STARTs=[60]
for cell_name in read_from_pickle(cells_name_place)[1:2]:
    passive_vals_dict= {}
    # p='cells_initiall_information/'+cell_name+'/results_passive_fits.csv'
    p='cells_outputs_data_short/'+cell_name+'/fit_short_pulse/results_passive_fits.csv'
    df = pd.read_csv(p)
    for resize_diam_by ,shrinkage_by in zip([1.0],[1.0]):#zip([1.0,1.1,1.2],[1.0,1.1,1.0]):
        for fit_condition in ['const_param','different_initial_conditions'][:1]:
            for file_type in file_types:
                for SPINE_START in [60,10]:
                    passive_vals_dict=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type)
                    for i, passive_val_name in enumerate(['RA=120','RA=150','RA_min_error','RA_best_fit']):
                        # if i!=2: continue
                        try: passive_vals_dict[passive_val_name]
                        except:
                            print(cell_name,file_type,shrinkage_by,resize_diam_by,fit_condition,SPINE_START, " isn't found")
                            continue

                        RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
                        if float(RA)<50:continue

                        print(cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START))
                        if in_parallel:
                            command="sbatch -p ss.q,elsc.q runs_change_passive_val_parallel.sh"
                            send_command = " ".join([command, '30',cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                        else:
                            command="sbatch -p ss.q,elsc.q runs_change_passive_val.sh"
                            send_command = " ".join([command,"1",cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),folder_])
                        print(send_command)
                        os.system(send_command+ " True")
                        from read_spine_properties import get_n_spinese
                        if get_n_spinese(cell_name)>1:
                            os.system(send_command+" False")

# command="sbatch -p ss.q,elsc.q runs_change_passive_val.sh"
# p4=" ".join([command,'1', '2017_05_08_A_5-4', 'morphology.swc', '120.0', '2.974997902411084', '6992.0', 'const_param', 'RA=120', '1.0', '1.0', '20'])
# p5=" ".join([command,'1', '2017_05_08_A_4-5', 'morphology.swc', '74.0', '2.072525235725758', '7485.0', 'const_param', 'RA_best_fit', '1.0', '1.0', '20'])
# os.system(p4)
# os.system(p5)
#  p1='1', '2017_05_08_A_4-5', 'z_correct.swc', '120.0', '1.9249102108707408', '8059.0', 'const_param', 'RA=120', '1.1', '1.1', '20'
#  p2='1', '2017_05_08_A_4-5', 'z_correct.swc', '150.0', '2.076686932986252', '7470.0', 'const_param', 'RA=150', '1.1', '1.1', '20'
#  p3='1', '2017_05_08_A_4-5', 'z_correct.swc', '82.0', '1.7502935111595734', '8863.0', 'const_param', 'RA_best_fit', '1.1', '1.1', '20'

 # p6='1', '2017_05_08_A_4-5', 'morphology.swc', '120.0', '1.9249102108707408', '8059.0', 'const_param', 'RA=120', '1.1', '1.1', '20', '_'
 # p7='1', '2017_05_08_A_4-5', 'morphology.swc', '150.0', '2.076686932986252', '7470.0', 'const_param', 'RA=150', '1.1', '1.1', '20', '_'
 # p8='1', '2017_05_08_A_4-5', 'morphology.swc', '82.0', '1.7502935111595734', '8863.0', 'const_param', 'RA_best_fit', '1.1', '1.1', '20', '_'
 # p9='1', '2017_05_08_A_4-5', 'morphology.swc', '120.0', '1.8406325806131112', '8428.0', 'const_param', 'RA=120', '1.2', '1.0', '20', '_'
 # p10='1', '2017_05_08_A_4-5', 'morphology.swc', '150.0', '1.94934046109667', '7958.0', 'const_param', 'RA=150', '1.2', '1.0', '20', '_'
 # p11='1', '2017_05_08_A_4-5', 'morphology.swc', '107.0', '1.7956767437674848', '8639.0', 'const_param', 'RA_best_fit', '1.2', '1.0', '20', '_
