import os
import shutil
import sys
from glob import glob
from open_pickle import read_from_pickle
from create_folder import create_folder_dirr

if len(sys.argv)!=3:
    sec_from_picture=True
    specipic_moo='correct_seg_syn_from_picture'# correct_seg_syn_find_syn_xyz
else:
    sec_from_picture=sys.argv[1]
    specipic_moo=sys.argv[2]
before_after='_after_shrink'
specipic_cell="None"

for specipic_moo in ['correct_seg_syn_from_picture','correct_seg_find_syn_xyz']:
    # os.system('python reorgenize_results.py '+ specipic_cell+' '+before_after+' _'+specipic_moo)
    base="python "
    base="sbatch execute_python_script.sh "
    folder2run='final_data/'+specipic_moo
    os.system(base+" create_Figure1.py "+folder2run)
    os.system(base+" create_Figure2.py "+folder2run)
    os.system(base+" create_Figure3.py "+folder2run)
    for cell_name in read_from_pickle('cells_name2.p'):
        os.system(base+" create_Figure_collect_data.py "+cell_name+" "+folder2run)
os.system(base+" create_Figure2.py ")
os.system(base+" create_Figure3.py ")

for cell_name in read_from_pickle('cells_name2.p'):
    print(cell_name)
    if cell_name in read_from_pickle('cells_sec_from_picture.p'):#['2017_07_06_C_4-3','2017_02_20_B','2016_05_12_A']: #cell that taken from picture
        specipic_moo='correct_seg_syn_from_picture'
    else:#cell that coming from xyz searching
        specipic_moo='correct_seg_find_syn_xyz'
    for p in glob('final_data/'+specipic_moo+'/Figure*/'+cell_name+'*'):
        if 'Figure3' in p or 'Figure2' in p: continue
        folder_save=create_folder_dirr('final_data/'+p.split('/')[2])
        shutil.copyfile(p,folder_save+'/'+p.split('/')[-1])
