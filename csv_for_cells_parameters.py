import pandas as pd
from extra_function import load_swc
from open_pickle import read_from_pickle
from glob import glob
import sys


from read_spine_properties import get_n_spinese

if len(sys.argv) != 2:
    before_after='_after_shrink'
    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    before_after=sys.argv[1]
    print("creat csv for passive_val running with sys.argv",sys.argv)
data_dir= "cells_initial_information/"
save_dir='cells_outputs_data_short/'

i=0
all_data=[]
for cell_name in read_from_pickle('cells_name2.p')[:]: #['2017_03_04_A_6-7']:#
    dict_for_records={}
    print(cell_name)
    short_pulse=read_from_pickle(glob(save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')[0])
    EPSP=read_from_pickle(glob(save_dir+cell_name+"/data/electrophysio_records/syn/mean_syn.p")[0])
    cell=None
    # cell=load_swc(glob('cells_initial_information/'+cell_name+'/*after_shrink.swc')[0])

    # moo_total_dict[passive_param_name]=Moo_dict
    # for key, value in moo_total_dict.items():
    #     dict_for_records = {}
        # add metadata
    dict_for_records['cell_name']=cell_name
    # dict_for_records['total_length']=round(sum([sec.L for sec in cell.all_sec()]))
    dict_for_records['H_EPSP']=round(float(max(EPSP[0])),2)
    dict_for_records['E_PAS']=round(short_pulse['E_pas'],2)
    dict_for_records['shrinkage_resize']=[1.0,1.0]
    dict_for_records['double_spine_area']='False'
    dict_for_records['from_picture']=cell_name in read_from_pickle('cells_sec_from_picture.p')
    dict_for_records['before_shrink']=before_after.split('_')[1]
    dict_for_records['syn_num']=get_n_spinese(cell_name)
    all_data.append(dict_for_records)

    cell=None


output_df_cells = pd.DataFrame.from_records(all_data)
output_df_cells.to_csv('final_data/total_moo/'+"/cells_parameters5.csv", index=False)



