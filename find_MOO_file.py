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
