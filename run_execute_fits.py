import os
import time
import sys
from open_pickle import read_from_pickle
if len(sys.argv) != 2:
    cells_name_place="cells_name.p"
    print("run_execute_level1.py not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_level1.py running with sys.argv",sys.argv)

# os.system(" ".join(['sbatch execute_python_script.sh', 'plot_neuron_3D.py',cells_name_place,'ASC']))
print('plot_neuron_3D.py for all cells in ',cells_name_place,'with file type of','ASC')
folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
base_command='sbatch execute_python_script.sh'
for cell_name in read_from_pickle(cells_name_place)[2:]:
    for file_type in ['z_correct.swc','morphology.swc'][0:1]:
        for SPINE_START in [20,60,10][0:1]:#SPINE_STARTs:
            for resize_diam_by ,shrinkage_by in zip([1.0,1.1,1.2,1.5][1:2],[1.0,1.1,1.0,1.0][1:2]):
                for double_spine_area in ['True','False'][1:2]:
                    # for Ra_min in [5,100]:
                        # command="fit_influnce_by_initial_condition.py"
                        # send_command = " ".join([base_command,command, cell_name,file_type,str(Ra_min),resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
                        # # os.system(send_command)
                        # # time.sleep(5)
                        # print(cell_name+ ' .'+file_type+': fit_influance_by_initial_condition.py with ra_min='+str(Ra_min))
                    command2="sbatch execute_fit_const.sh"
                    # command2="sbatch execute_python_script.sh fit_best_with_const_param.py"

                    command2="python fit_best_with_const_param.py"
                    send_command = " ".join([command2, cell_name,file_type,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area])
                    os.system(send_command)
                    # time.sleep(10)
                    print(cell_name+ ' .'+file_type+': fit_best_with_const_param.py')

                # for RA_min in [0,50,100,150,200]:
                #     command="fit_with_diffrent_RA_min.py"
                #     send_command = " ".join([base_command,command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(RA_min),str(SPINE_START),folder_])
                #     os.system(send_command)
                #     print(cell_name+':fit_with_diffrent_RA_min.py RA_min='+str(RA_min))
                #
                #
                # for add2delay  in [0,1,2,3,4,5,6,7,8]:
                #     for add2fit  in range(0,20,2):
                #         command="fit_with_diffrent_time_delay.sh"
                #         send_command = " ".join([base_command,command, cell_name,file_type,resize_diam_by,shrinkage_factor,str(add2delay),str(add2fit),str(SPINE_START),folder_])
                #         os.system(send_command)
                #         print(cell_name+':fit_with_diffrent_time_delay.py delay='+str(add2delay)+' add fit='+str(add2fit))
