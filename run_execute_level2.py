import os
from passive_val_function import *
from read_passive_parameters_csv import get_passive_parameter
import sys
import pandas as pd
from open_pickle import read_from_pickle
if len(sys.argv) != 2:
    cells_name_place="cells_name2.p"
    print("run_execute_level2.py not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_level2.py running with sys.argv",sys.argv)
cells=read_from_pickle(cells_name_place)

before_after='_after_shrink'

file_type2read=['z_correct.swc','morphology.swc']
# SPINE_START=str(20)

os.system('python csv_for_passive_val_results.py cells_name2.p')
i=0
    # os.system('python run_analysis_fit_after_run.py')
for cell_name in read_from_pickle(cells_name_place):
    if not cell_name in ['2017_03_04_A_6-7']:continue #'2017_07_06_C_4-3','2017_07_06_C_3-4',

    # if cell_name=='2017_07_06_C_4-3':
    #     before_after='_before_shrink'
    # else:
    #     before_after='_after_shrink'
    #     continue
    # if not cell_name in ['2017_03_04_A_6-7']:continue
    # if not cell_name in ['2017_07_06_C_4-3','2016_04_16_A']:continue#['2017_02_20_B','2017_07_06_C_3-4']:continue
    passive_vals_dict= {}
    # p='cells_initiall_information/'+cell_name+'/results_passive_fits.csv'
    p='cells_outputs_data_short/'+cell_name+'/fit_short_pulse'+before_after+'/results_passive_fits.csv'
    print(cell_name)
    df = pd.read_csv(p)
    for resize_diam_by ,shrinkage_by in zip([1.0,1.0,1.1,1.5][:2],[1.0,1.1,1.1,1.0][:2]):#zip([1.0],[1.0]):
        for fit_condition in ['const_param','different_initial_conditions'][:1]:
            for SPINE_START in [20,60,10][:1]:
                if cell_name!='2017_05_08_A_4-5' and resize_diam_by==1.5:continue
                if resize_diam_by==1.0 and shrinkage_by==1.0:
                    do_double_spine_area=['True','False']
                else:
                    do_double_spine_area=['False']
                for double_spine_area in do_double_spine_area:
                    # if resize_diam_by==1.0 and shrinkage_by==1.0 and double_spine_area=='False' and SPINE_START==20:
                    #     file_types=['z_correct.swc','morphology.swc']
                    # else:
                    #     file_types=['z_correct.swc']
                    for file_type in ['z_correct.swc']:
                        passive_vals_dict=get_passive_parameter(cell_name,before_after,double_spine_area=double_spine_area,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type)
                        next_continue=False
                        for i, name in enumerate(['RA_min_error','RA_best_fit','RA=120','RA=150']):

                            if next_continue: continue
                            try: passive_vals_dict[name]
                            except:
                                print('passive_vals_dict is empty')
                                continue
                            RA,CM,RM=get_passive_val(passive_vals_dict[name])
                            if float(RA)<50:
                                continue
                            else:
                                if float(RA)>70:
                                    next_continue=True
                            print(name,RA,CM,RM)
                            command="sbatch execute_level2.sh"
                            # command ="python dendogram.py"
                            send_command = " ".join([command,cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area,before_after])
                            os.system(send_command)
                            print(send_command)
                            print(cell_name+ ' .'+file_type+': execute level2.py, dendogram.py, Rin_Rm.py','attenuations.py')


                            # command='sbatch execute_python_script.sh'
                            # command='python'

                            #
                            # send_command = " ".join([command, 'Rin_Rm_plot.py',cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START])
                            # os.system(send_command)
                            # print(cell_name+ ' .'+file_type+':  Rin_Rm_plot.py')

                            # send_command = " ".join([command, 'dendogram.py',cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_factor),SPINE_START])
                            # # os.system(send_command)
                            # print(cell_name+ ' .'+file_type+':  dendogram.py')
                            #
                            # for syn_injection in ['True','False']:
                            #     os.system(" ".join([command, 'attenuations.py', cell_name,file_type,fit_condition,name,syn_injection,str(resize_diam_by),str(shrinkage_factor),SPINE_START]))
                            #     print('execute level2 runing analysis_after_run.py dendogram.py and Rin_Rm.py')
                            #     if eval(syn_injection):
                            #         print(cell_name+ ' '+file_type+': attenuations.py with syn injection')
                            #     else:
                            #         print(cell_name+ ' '+file_type+': attenuations.py with current injection')



