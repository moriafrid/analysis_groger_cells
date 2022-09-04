import pandas as pd
from tqdm import tqdm

from find_MOO_file import MOO_file
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import sys
from read_passive_parameters_csv import get_passive_parameter
import re
if len(sys.argv) != 3:
    cells_name_place="cells_name2.p"
    before_after='_after_shrink'
    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    before_after=sys.argv[2]
    print("creat csv for passive_val running with sys.argv",sys.argv)
save_moo=''
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
cells=read_from_pickle(cells_name_place)
data_file='cells_outputs_data_short/'


short_pulse='/fit_short_pulse'+before_after+'/'
file_type2read=['z_correct.swc','morphology.swc','hoc','ASC']
i=0
# os.system('python run_analysis_fit_after_run.py')
for cell_name in cells:
    print(cell_name)

    for before_after in ['_before_shrink','_after_shrink']:
        all_data = []
        file=[]
        for p in MOO_file(cell_name,before_after=before_after):
            file+=glob(folder_save+cell_name+p+'/F_shrinkage=*/const_param/*/hall_of_fame.p')

        # file+=glob(folder_save+cell_name+MOO_relative+'/F_shrinkage=*/const_param/*/hall_of_fame.p')

        for loc in tqdm(file):
            # df = pd.read_csv('cells_initial_information/'+cell_name+'/results_passive_fits.csv')
            passive_param_name=loc.split('/')[6]
            if 'test' in passive_param_name: continue
            file_type=loc.split('/')[3][:loc.split('/')[3].rfind('.')+4]
            shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[4])
            shrinkage_resize=[float(num) for num in shrinkage_resize]
            if 'double_spine_area' in loc.split('/')[4]:
                print('double_spine_area')
                double_spine_area='True'
            else:
                double_spine_area='False'
            spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[3])[0])
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
            # for key, value in passive_vals_dict.items():
            #         dict_for_records = {}
            #         # add metadata
            #         dict_for_records['fit_condition'] = fit_condition
            #         dict_for_records['file_type'] = file_type
            #         dict_for_records['parameter_type'] = key
            #         dict_for_records['spine_start'] =SPINE_START
            #         dict_for_records['shrinkage&resize_factors']=[shrinkage_factor,resize_diam_by]
            #         dict_for_records['double_spine_area']=double_spine_area
            #         if value is not None:
            #             dict_for_records.update(value)
            #         all_data.append(dict_for_records)
            if Moo_dict is not None:
                dict_for_records.update(Moo_dict)
            all_data.append(dict_for_records)
            output_df = pd.DataFrame.from_records(all_data)
            dict_for_records['before_shrink']=before_after.split('_')[1]
            'cells_outputs_data_short/2017_07_06_C_4-3/MOO_results_same_strange_after_shrink_correct_seg_syn_from_picture/z_correct.swc_SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/RA_best_fit_full_trace/Rins_pickles.p'
            # Rin_dict=read_from_pickle(glob(loc[:loc.find('hall_of_fame')]+'Rins_pickles.p')[0])
            # dict_for_records.update(Rin_dict)
            # all_data.append(dict_for_records)



    save_pickle_folder=folder_+folder_data+cell_name+'/'
    output_df = pd.DataFrame.from_records(all_data)
    output_df.to_csv(folder_data+cell_name+"/results_MOO"+save_moo+".csv", index=False)

    # save_pickle_folder2=folder_+folder_data+cell_name
    # output_df = pd.DataFrame.from_records(all_data)
    # output_df.to_csv(save_pickle_folder2+"/results_MOO"+before_after+".csv", index=False)
    # pickle.dump(dict_fit_condition, open(save_pickle_folder2+"/results_MOO.p", "wb"))
