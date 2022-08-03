import os
import pandas as pd
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import pickle
import sys
if len(sys.argv) != 3:
    cells_name_place="cells_name2.p"
    before_after="_before_shrink"

    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    before_after=sys.argv[2]

    print("creat csv for passive_val running with sys.argv",sys.argv)
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
cells=read_from_pickle(cells_name_place)
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
resize_diam_by=1.0
shrinkage_factor=1.0

# os.system('python run_analysis_fit_after_run.py')

for cell_name in cells:
    # print(cell_name)
    all_data = []
    dict_fit_condition={}
    for fit_condition in ['const_param','different_initial_conditions'][:1]:
        # print(fit_condition)
        for file_type in ['z_correct.swc','morphology.swc','ASC']:

            for resize_diam_by ,shrinkage_factor in zip([1.0,1.1,1.0,1.2,1.5],[1.0,1.1,1.1,1.0,1.0]):
                for SPINE_START in [str(20),str(10),str(60)]:
                    for double_spine_area in ['True','False']:
                        passive_vals_dict= {}
                        initial_folder=folder_+folder_save+cell_name+'/fit_short_pulse'+before_after+'/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
                        # initial_folder=folder_+folder_save+cell_name+'/fit_short_pulse/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
                        initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
                        if eval(double_spine_area):
                            initial_folder+='_double_spine_area'
                        initial_folder+='/'+fit_condition
                        try:
                            if fit_condition=='const_param':
                                passive_val_total=read_from_pickle(glob(initial_folder+'/RA/analysis/RA_total_errors_minimums.p')[0])
                            elif fit_condition=='different_initial_conditions':
                                passive_val_total=read_from_pickle(glob(initial_folder+'/RA_min'+str(5)+'/analysis/RA_total_errors_minimums.p')[0])
                            print('is founde ',initial_folder)
                        except:
                            # print("there isn't have RA_total_errors_minimums in spine strart=" +SPINE_START+" "+initial_folder)
                            continue
                        passive_vals_dict['RA=120']=found(passive_val_total,120)
                        passive_vals_dict['RA=150']=found(passive_val_total,150)
                        passive_vals_dict['RA_min_error']=passive_val_total[0]
                        passive_vals_dict['min_CM']=found_min_parameter(passive_val_total,parameter='CM')
                        passive_vals_dict['RA_best_fit']=found_best_RA(passive_val_total)
                        passive_vals_dict['mean_best_10']=mean_best_n(passive_val_total,10)
                        if fit_condition=='different_initial_conditions' and (passive_vals_dict['RA=120'] is None or passive_vals_dict['RA=150'] is None):
                            passive_val_total=read_from_pickle(glob(initial_folder+'/RA_min'+str(100)+'/analysis/RA_total_errors_minimums.p')[0])
                            passive_vals_dict['RA=120']=found(passive_val_total,120)
                            passive_vals_dict['RA=150']=found(passive_val_total,150)
                        dict_fit_condition[fit_condition]={SPINE_START:{file_type:passive_vals_dict}}


                        # add flat fields
                        for key, value in passive_vals_dict.items():
                            dict_for_records = {}
                            # add metadata
                            dict_for_records['fit_condition'] = fit_condition
                            dict_for_records['file_type'] = file_type
                            dict_for_records['parameter_type'] = key
                            dict_for_records['spine_start'] =SPINE_START
                            dict_for_records['shrinkage&resize_factors']=[shrinkage_factor,resize_diam_by]
                            dict_for_records['double_spine_area']=double_spine_area
                            if value is not None:
                                dict_for_records.update(value)
                            all_data.append(dict_for_records)

                save_pickle_folder=folder_+folder_save+cell_name+'/fit_short_pulse'+before_after+'/'
                output_df = pd.DataFrame.from_records(all_data)
                # print(output_df.columns)
                # print(output_df)
                output_df.to_csv(save_pickle_folder+"/results_passive_fits.csv", index=False)
                pickle.dump(dict_fit_condition, open(save_pickle_folder+"/results_passive_fits.p", "wb"))

                # save_pickle_folder2=folder_+folder_data+cell_name
                # output_df = pd.DataFrame.from_records(all_data)
                # output_df.to_csv(save_pickle_folder2+"/results_passive_fits"+before_after+".csv", index=False)
                # pickle.dump(dict_fit_condition, open(save_pickle_folder2+"/results_passive_fits"+before_after+".p", "wb"))
