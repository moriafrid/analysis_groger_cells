import os
import sys
from open_pickle import read_from_pickle
if len(sys.argv) != 2:
    cells_name_place="cells_name2.p"
    print("run_execute_fits.py not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    print("run_execute_fits.py running with sys.argv",sys.argv)
before_after="_before_shrink"

# os.system(" ".join(['sbatch execute_python_script.sh', 'plot_neuron_3D.py',cells_name_place,'ASC']))
print('plot_neuron_3D.py for all cells in ',cells_name_place,'with file type of','ASC') ##moria - not plot_neuron_3D working
folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
base_command='sbatch execute_python_script.sh'
SPINE_START=20


for cell_name in read_from_pickle(cells_name_place):
    print(cell_name)
    for resize_diam_by ,shrinkage_by in zip([1.0,1.1,1.0,1.5],[1.0,1.1,1.1,1.0]):
        if cell_name!='2017_05_08_A_4-5' and resize_diam_by==1.5:continue
        if resize_diam_by==1.0 and shrinkage_by==1.0 and cell_name=='2017_05_08_A_4-5':
            print('true')
            do_double_spine_area=['False','True']
        else:
            do_double_spine_area=['False']
        for double_spine_area in do_double_spine_area:
            # if resize_diam_by==1.0 and shrinkage_by==1.0 and double_spine_area=='False' and cell_name=='2017_05_08_A_4-5':
            #     file_types=['z_correct.swc','morphology.swc','ASC']
            # else:
            #     file_types=['z_correct.swc']
            for file_type in ['z_correct.swc']:
                # for Ra_min in [5,100]:
                    # command="fit_influnce_by_initial_condition.py"
                    # send_command = " ".join([base_command,command, cell_name,file_type,str(Ra_min),resize_diam_by,shrinkage_factor,str(SPINE_START),folder_])
                    # # os.system(send_command)
                    # # time.sleep(5)
                    # print(cell_name+ ' .'+file_type+': fit_influance_by_initial_condition.py with ra_min='+str(Ra_min))
                command2="sbatch execute_fit_const.sh"
                command2="sbatch execute_python_script.sh fit_best_with_const_param.py"
                # command2= "python fit_best_with_const_param.py"
                send_command = " ".join([command2, cell_name,file_type,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area,before_after])
                os.system(send_command)
                print(cell_name+ ' .'+file_type,str(resize_diam_by),str(shrinkage_by),str(SPINE_START),double_spine_area,before_after)

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



