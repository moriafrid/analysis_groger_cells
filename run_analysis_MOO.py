import os
base="python "
base="sbatch execute_python_script.sh "
os.system(base+"exp_V_syns_soma.py")
os.system(base+"exp_soma_NMDA_AMPA.py")
os.system(base+"exp_sys_gmax.py")


