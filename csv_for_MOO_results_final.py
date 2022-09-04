import pandas as pd
from tqdm import tqdm

from find_MOO_file import MOO_file
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import sys
from read_passive_parameters_csv import get_passive_parameter
import re

from read_spine_properties import get_n_spinese

if len(sys.argv) != 3:
    cells_name_place="cells_name2.p"
    before_after='_after_shrink'
    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    cells_name_place=sys.argv[1]
    before_after=sys.argv[2]
    print("creat csv for passive_val running with sys.argv",sys.argv)
save_moo='_Rin_result'
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"
cells=read_from_pickle(cells_name_place)
data_file='cells_outputs_data_short/'


short_pulse='/fit_short_pulse'+before_after+'/'
i=0
# os.system('python run_analysis_fit_after_run.py')

for cell_name in cells:
    print(cell_name)
    all_data = []
    file=[]
    for p in MOO_file(cell_name,before_after=before_after):
        for passive_param_name in ['RA_min_error','RA_best_fit','RA=100','RA=120','RA=150','RA=200','RA=300']:
            file+=glob(folder_save+cell_name+p+'/F_shrinkage=1.0*1.0/const_param/'+passive_param_name+'/Rins_pickles.p')
    moo_total_dict={}
    for loc in tqdm(file):
        moo_total_dict={}
        print(loc)
        # df = pd.read_csv('cells_initial_information/'+cell_name+'/results_passive_fits.csv')
        passive_param_name=loc.split('/')[6]
        if 'test' in passive_param_name: continue
        # file_type=loc.split('/')[3][:loc.split('/')[3].rfind('.')+4]
        shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[4])
        shrinkage_resize=[float(num) for num in shrinkage_resize]
        if 'double_spine_area' in loc.split('/')[4]:
            print('double_spine_area')
            double_spine_area='True'
        else:
            double_spine_area='False'
        # spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", loc.split('/')[3])[0])
        if "full_trace" in passive_param_name:
            passive_param_name=passive_param_name[:passive_param_name.rfind('_full_trace')]

        result_dict=read_from_pickle(loc)

        for i in range(get_n_spinese(cell_name)):
            Moo_dict = {}
            for value in ['PSD','distance']:
                Moo_dict[value]=result_dict['parameters'][value][i]
            relative_PSD=result_dict['parameters']['PSD']/max(result_dict['parameters']['PSD'])
            for value in ['W_AMPA','W_NMDA']:
                Moo_dict[value]=result_dict['parameters'][value]*1000*relative_PSD[i]/sum(relative_PSD)

            for value in ['tau1_AMPA','tau2_AMPA','tau1_NMDA','tau2_NMDA','E_PAS','RA','RM','CM']:
                Moo_dict[value]=result_dict['parameters'][value]
            Moo_dict['soma_Rin']=result_dict['soma']['Rin']

            for value in ['neck_base','spine_head']:
                for value1 in ['Rin','Rtrans']:
                    Moo_dict[value+'_'+value1]=result_dict[value][value1][i]
            moo_total_dict[passive_param_name]=Moo_dict
            for key, value in moo_total_dict.items():
                dict_for_records = {}
                # add metadata
                dict_for_records['cell_name']=cell_name
                dict_for_records['passive_parameter']=passive_param_name
                dict_for_records['RA']=result_dict['parameters']['RA']
                dict_for_records['relative']=result_dict['parameters']['reletive_strengths']
                dict_for_records['shrinkage&resize_factors']=shrinkage_resize
                dict_for_records['double_spine_area']=double_spine_area
                dict_for_records['before_shrink']=before_after.split('_')[1]
                dict_for_records['syn_num']=i
                if value is not None:
                    dict_for_records.update(value)
                all_data.append(dict_for_records)

        # all_data.append(dict_for_records)
        output_df = pd.DataFrame.from_records(all_data)
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
