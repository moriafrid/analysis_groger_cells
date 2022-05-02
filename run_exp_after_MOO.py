import os
os.system("sbatch execute_python_script.sh exp_V_syns_soma.py")
os.system("sbatch execute_python_script.sh exp_soma_NMDA_AMPA.py")
os.system("sbatch execute_python_script.sh exp_sys_gmax.py")


