import os
from passive_val_function import *
from read_passive_parameters_csv import get_passive_parameter
import sys
from open_pickle import read_from_pickle
if len(sys.argv) != 2:
    cells_name_place="cells_name2.p"
    print("run_execute_level1.py not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_level1.py running with sys.argv",sys.argv)
cells=read_from_pickle(cells_name_place)
file_type2read=['z_correct.swc','morphology.swc']
# SPINE_START=str(20)

os.system('python csv_for_passive_val_results.py cells_name2.p')
i=0
    # os.system('python run_analysis_fit_after_run.py')
for cell_name in cells:
    print(cell_name)
    all_data = []
    dict_fit_condition={}
    for fit_condition in ['const_param']:
        print(fit_condition)

        for resize_diam_by ,shrinkage_by in zip([1.0,1.1,1.0,1.5],[1.0,1.1,1.1,1.0]):
            print('shrinkage_factor:',shrinkage_by,'reasize_dend_factor:',resize_diam_by)
            # if shrinkage_by!=1.0:continue
            if resize_diam_by==1.0 and shrinkage_by==1.0 and cell_name=='2017_05_08_A_4-5':
                do_double_spine_area=['True','False']
            else:
                do_double_spine_area=['False']

            for double_spine_area in do_double_spine_area:
                if resize_diam_by==1.0 and shrinkage_by==1.0 and double_spine_area=='False' and cell_name=='2017_05_08_A_4-5':
                    file_types=['z_correct.swc','morphology.swc','ASC']
                else:
                    file_types=['z_correct.swc']

                for file_type in file_types:
                    if resize_diam_by==1.0 and shrinkage_by==1.0 and double_spine_area=='False' and file_type=='z_correct.swc' and cell_name=='2017_05_08_A_4-5':
                        SPINE_STARTs=[str(20),str(60)]
                    else:
                        SPINE_STARTs=[str(20)]
                    for SPINE_START in SPINE_STARTs:
                        passive_vals_dict=get_passive_parameter(cell_name,double_spine_area=double_spine_area,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=SPINE_START,file_type=file_type)
                        for name in ['RA=120','RA=150','RA_min_error','RA_best_fit']:
                            # if i>1: continue
                            i+=1
                            try: passive_vals_dict[name]
                            except:
                                print('passive_vals_dict is empty')
                                continue
                            RA,CM,RM=get_passive_val(passive_vals_dict[name])
                            if float(RA)<50:continue
                            print(name,RA,CM,RM)
                            command="sbatch execute_level2.sh"
                            # command ="python dendogram.py"
                            send_command = " ".join([command,cell_name,file_type,fit_condition,name,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area])
                            os.system(send_command)
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



