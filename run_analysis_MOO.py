import os
before_after='_before_shrink'
base="python "
base="sbatch execute_python_script.sh "
os.system("python csv_for_MOO_results.py "+before_after)
os.system(base+"exp_V_syns_soma.py "+ before_after   )
os.system(base+"exp_V_syns_effect_on_soma.py "+before_after)
os.system(base+"exp_soma_NMDA_AMPA.py "+before_after)
os.system(base+"exp_syns_NMDA_AMPA.py "+before_after)
os.system(base+"exp_sys_gmax.py "+before_after)


