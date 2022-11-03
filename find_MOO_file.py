from glob import glob

from tqdm import tqdm

from open_pickle import read_from_pickle
from read_spine_properties import get_n_spinese


def MOO_file(cell_name=None,before_after='_after_shrink'):
    if before_after=='_before_shrink':
        MOO_relative='/MOO_results_relative_strange'+before_after+'/z_correct.swc_SPINE_START=20/'
        MOO_same='/MOO_results_same_strange'+before_after+'/z_correct.swc_SPINE_START=20/'
    else:
        if cell_name is None:
            seg_place='*'
        elif cell_name in read_from_pickle('cells_sec_from_picture.p'):
            seg_place='_syn_from_picture'
        else:
            seg_place='_find_syn_xyz'
        MOO_relative='/MOO_results_relative_strange'+before_after+'_correct_seg'+seg_place+'/z_correct.swc_SPINE_START=20/'
        MOO_same='/MOO_results_same_strange'+before_after+'_correct_seg'+seg_place+'/z_correct.swc_SPINE_START=20/'
    if cell_name is None:
        return [MOO_same, MOO_relative]

    elif get_n_spinese(cell_name)>1:
        return [MOO_relative]
    else:
        return [MOO_same]

def check_if_continue(model_place,cell_name='None'):
    cont=False
    if cell_name is None:
        cell_name=model_place.split('/')[1]
    if 'RA=300' in model_place or 'RA=120' in model_place or 'RA=200' in model_place:
        cont=True
    if cell_name in ['2017_07_06_C_3-4']:
        if 'full_trace' in model_place:
            cont=True
    else:
        if not 'full_trace' in model_place:
            cont=True
    if cell_name in read_from_pickle('cells_sec_from_picture.p'):
        if 'syn_xyz' in model_place:
            cont=True
    else:
        if not 'syn_xyz' in model_place:
            cont=True
    if 'test' in model_place.split('/')[-1] or 'test' in model_place.split('/')[-2]:
        cont=True
    if get_n_spinese(cell_name)>1 and 'same' in model_place:
        cont=True
    return cont

def model2run(specipic_cell='*',shrinkage='*'):
    folders=[]
    folder_=''
    if specipic_cell=='*':
        for moo_file in MOO_file(before_after='_before_shrink')+MOO_file(before_after='_after_shrink'):
            folders+=glob(folder_+'cells_outputs_data_short/'+specipic_cell+'/'+moo_file+'/'+shrinkage+'/const_param/*')
    else:
        for moo_file in MOO_file(specipic_cell,before_after='_before_shrink')+MOO_file(specipic_cell,before_after='_after_shrink'):
            folders+=glob(folder_+'cells_outputs_data_short/'+specipic_cell+'/'+moo_file+'/'+shrinkage+'/const_param/*')
    file2run0=[]
    if specipic_cell=='*':
        specipic_cell=None

    for model_place in tqdm(folders):
        model_place=model_place.replace('//','/')
        if check_if_continue(model_place,cell_name=specipic_cell): continue
        file2run0.append(model_place)
    file2run=[]
    for passive_val in ['RA_min_error','RA_best_fit','RA=70','RA=100','RA=120','RA=150','RA=200','RA=300']:
        for file in file2run0:
            if passive_val in file:
                file2run.append(file)
    print('length for model to run is' ,len(file2run))
    return file2run
