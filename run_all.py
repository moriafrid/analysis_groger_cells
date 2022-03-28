import os
cells_name_place='cells_name.p'
folder=""
commet_main=" ".join(["python run_excute_main.py", folder, cells_name_place ])
os.system(commet_main)

os.system("python run_execute_level1.py")
os.system("python run_execute_fits.py")
os.syatem("csv_for_passive_val_results.py")
os.system("python run_execute_level2.py")
os.system("python run_Moo_get_parameters.py")

