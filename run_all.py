import os
from open_pickle import read_from_pickle
#set invisible top and right, for the 1st column (can remove the if)
# for ax in fig.get_axes():  #show only specific spines
#     if not ax.get_subplotspec().is_first_col():
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#
#
# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['svg.fonttype'] = 'none'
#fontsize as parameter for xlabel etc (for everything, title...)

cells_name_place='cells_name2.p'


commet_main=" ".join(["python run_execute_main.py", cells_name_place ])
os.system(commet_main)

for cell_name in read_from_pickle(cells_name_place):
    os.system('python file_converter_to_swc_z_corrections.py '+cell_name)
    # os.system('python creat_morphology_dict.py '+cell_name)
    os.systen('python plot_morphology_David.py '+cell_name)


commet_level1=" ".join(["python plot_morphology_David.py", cells_name_place ])
os.system(commet_level1)

os.system('python choose_short_pulse.py')

os.system('python check_short_pulse_edges.py')

os.system('python calculate_tau_m.py')

commet_level1=" ".join(["python run_execute_fits.py", cells_name_place ])
os.system(commet_level1)

os.syatem("csv_for_passive_val_results.py")

commet_level1=" ".join(["python run_execute_level2.py", cells_name_place ])
os.system(commet_level1)

os.system('python choose_syn.py')

os.system('python run_Moo_get_parameters.py')

os.system("python run_analysis_MOO.py")


# os.system("python run_execute_fits.py")
# os.system("python run_execute_level2.py")
# os.system("python run_Moo_get_parameters.py")


