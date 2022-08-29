import os
before_after='_after_shrink'
base="python "
base="sbatch execute_python_script.sh "
cell2run='None'

specific_moo='_correct_seg_find_syn_xyz'
os.system("python csv_for_MOO_results.py "+ cell2run+' '+before_after+' '+specific_moo)
os.system(base+"exp_soma_NMDA_AMPA_seperet.py "+ cell2run+' '+ before_after+' '+specific_moo)
os.system(base+"exp_V_syns_effect_on_soma.py "+ cell2run+' '+before_after+' '+specific_moo)
os.system(base+"exp_soma_NMDA_AMPA.py "+ cell2run+' '+before_after+' '+specific_moo)
# os.system(base+"exp_syns_NMDA_AMPA.py "+before_after)
os.system(base+"exp_sys_gmax.py "+ cell2run+' '+before_after+' '+specific_moo)
os.system(base+"exp_V_in_Rneck.py "+ cell2run+' '+before_after+' '+specific_moo)

