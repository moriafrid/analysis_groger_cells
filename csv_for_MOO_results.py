import os
import pandas as pd
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import pickle
import sys
from read_passive_parameters_csv import get_passive_parameter
import re
if len(sys.argv) != 3:
    cells_name_place="cells_name2.p"
    before_after='_before_shrink'

    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    before_after=sys.argv[2]

    print("creat csv for passive_val running with sys.argv",sys.argv)
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
cells=read_from_pickle(cells_name_place)
data_file='cells_outputs_data_short/'
MOO_relative='/MOO_results_relative_strange'+before_after
MOO_same='/MOO_results_same_strange'+before_after
short_pulse='/fit_short_pulse'+before_after+'/'
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
i=0
# os.system('python run_analysis_fit_after_run.py')
for cell_name in cells:
    print(cell_name)
    all_data = []
    files1= glob(folder_save+cell_name+MOO_relative+'/*_SPINE_START=*/F_shrinkage=*/const_param/*/hall_of_fame.p')
    files2= glob(folder_save+cell_name+MOO_same+'/*_SPINE_START=*/F_shrinkage=*/const_param/*/hall_of_fame.p')

    for loc in files1+files2:
        # df = pd.read_csv('cells_initial_information/'+cell_name+'/results_passive_fits.csv')
        if loc.split('/')[6]=='test': continue
        file_type=loc.split('/')[3][:loc.split('/')[3].rfind('.')+4]
        # if file_type=='morphology.swc':
        #     print("reminder- morpology.swc is jeust the same like z_corretc")
        #     continue
        shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[4])
        shrinkage_resize=[float(num) for num in shrinkage_resize]
        if 'double_spine_area' in loc.split('/')[4]:
            print('double_spine_area')
            double_spine_area='True'
        else:
            double_spine_area='False'
        spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[3])[0])
        passive_param_name=loc.split('/')[6]
        if "full_trace" in passive_param_name:
            passive_param_name=passive_param_name[:passive_param_name.rfind('_full_trace')]
        #this function should return all the
        passive_vals_dict=get_passive_parameter(cell_name,before_after,passive_param_name=passive_param_name,double_spine_area=double_spine_area,
                                                shrinkage_resize=shrinkage_resize,spine_start=spine_start,fit_condition=loc.split('/')[5],
                                                file_type=file_type)
        results_Moo=read_from_pickle(loc)
        params=results_Moo['parameters']
        values=np.mean(results_Moo['hall_of_fame'],axis=0)
        Moo_dict={}
        for par,val in zip(params,values):
            Moo_dict[par]=val
        i=0
        value=passive_vals_dict
        dict_for_records = {}

        if value is not None:
            dict_for_records.update(value)
        # dict_for_records['parameters_type']=key
        dict_for_records['double_spine_area']=double_spine_area
        if "same" in loc.split('/')[2]:
            dict_for_records['same_strange']=True
        elif "relative" in loc.split('/')[2]:
            dict_for_records['same_strange']=False
        if Moo_dict is not None:
            dict_for_records.update(Moo_dict)
        all_data.append(dict_for_records)
        output_df = pd.DataFrame.from_records(all_data)




    # save_pickle_folder=folder_+folder_save+cell_name+'/'
    # output_df = pd.DataFrame.from_records(all_data)
    # output_df.to_csv(save_pickle_folder+"/results_MOO"+before_after+".csv", index=False)

    save_pickle_folder2=folder_+folder_data+cell_name
    output_df = pd.DataFrame.from_records(all_data)
    output_df.to_csv(save_pickle_folder2+"/results_MOO"+before_after+".csv", index=False)
    # pickle.dump(dict_fit_condition, open(save_pickle_folder2+"/results_MOO.p", "wb"))
