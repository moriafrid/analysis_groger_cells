import os
cells_name_place='cells_name.p'
commet_main=" ".join(["python run_execute_main.py", cells_name_place ])
os.system(commet_main)

commet_level1=" ".join(["python run_execute_level1.py", cells_name_place ])
os.system(commet_level1)

# os.system("python rusqueue n_execute_fits.py")
# os.syatem("csv_for_passive_val_results.py")
# os.system("python run_execute_level2.py")
# os.system("python run_Moo_get_parameters.py")

