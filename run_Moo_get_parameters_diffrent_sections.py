from open_pickle import read_from_pickle
import os
from glob import glob
from passive_val_function import *
import pandas as pd
from read_passive_parameters_csv import get_passive_parameter
import sys
from open_pickle import read_from_pickle
from read_spine_properties import get_n_spinese

if len(sys.argv) != 3:
    cells_name_place="cells_name2.p"
    in_parallel=False
    print("run_Moo_get_parameters not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    in_parallel=sys.argv[2]
    print("run_Moo_get_parameters running with sys.argv",sys.argv)
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
before_after='_after_shrink'



for cell_name in read_from_pickle(cells_name_place):
    if cell_name!='2017_04_03_B':continue
    passive_vals_dict= {}
    p='cells_outputs_data_short/'+cell_name+'/fit_short_pulse'+before_after+'/results_passive_fits.csv'
    print(cell_name)
    df = pd.read_csv(p)
    for resize_diam_by ,shrinkage_by in zip([1.0,1.0,1.1,1.5][:1],[1.0,1.1,1.1,1.0][:1]):#zip([1.0],[1.0]):
        for fit_condition in ['const_param','different_initial_conditions'][:1]:
            for SPINE_START in [20,60,10][:1]:
                for double_spine_area in ['False']:
                    for file_type in ['z_correct.swc']:
                        passive_vals_dict=get_passive_parameter(cell_name,before_after,double_spine_area=double_spine_area,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type)
                        next_continue=False
                        for i, passive_val_name in enumerate(['RA_min_error','RA_best_fit','RA=120','RA=150'][:]):
                            # if passive_val_name=='RA_min_error':continue
                            if next_continue: continue
                            try: passive_vals_dict[passive_val_name]
                            except:
                                # print(cell_name,file_type,shrinkage_by,resize_diam_by,fit_condition,SPINE_START, " isn't found")
                                continue
                            RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
                            if float(RA)<50:
                                continue
                            else:
                                if float(RA)>70:
                                    next_continue=True
                            command="sbatch -p ss.q,elsc.q runs_change_passive_val.sh"

                            fits_until_point=str(-1)
                            for special_sec in ['_1','_2','_3','_4','_5','_6']:
                                send_command = " ".join([command,"1",cell_name,file_type,RA,CM,RM,fit_condition,passive_val_name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area,before_after,fits_until_point])
                                print(send_command)
                                os.system(send_command+ " True "+special_sec)
                                if get_n_spinese(cell_name)>1:
                                    os.system(send_command+" False "+special_sec)
