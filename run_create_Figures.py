import os
import sys
if len(sys.argv)!=3:
    sec_from_picture=True
    specipic_moo='correct_seg_syn_from_picture'# correct_seg_syn_find_syn_xyz
else:
    sec_from_picture=sys.argv[1]
    specipic_moo=sys.argv[2]
before_after='_after_shrink'
specipic_cell="None"

for specipic_moo in ['correct_seg_syn_from_picture','correct_seg_syn_find_syn_xyz']:
    os.system('python reorgenize_results.py '+ '_'+specipic_cell+' '+before_after+' '+specipic_moo)
    base="python "
    base="sbatch execute_python_script.sh "
    folder2run='final_data/'+specipic_moo
    os.system(base+" create_Figure1.py "+folder2run)
    os.system(base+" create_Figure2.py "+folder2run)
    os.system(base+" create_Figure3.py "+folder2run)
    os.system(base+" create_Figure_collect_data.py "+folder2run)

'create_Figure_collect_data.py'
