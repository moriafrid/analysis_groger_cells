import pandas as pd
from tqdm import tqdm

from find_MOO_file import MOO_file, check_if_continue, model2run
from open_pickle import read_from_pickle
from glob import glob
from passive_val_function import *
import sys
from read_passive_parameters_csv import get_passive_parameter
import re

from read_spine_properties import get_n_spinese

if len(sys.argv) != 2:
    before_after='_after_shrink'
    print("creat csv for passive_val not running with sys.argv",len(sys.argv))
else:
    before_after=sys.argv[1]
    print("creat csv for passive_val running with sys.argv",sys.argv)
save_moo='_Rin_result'
folder_=""
folder_data="cells_initial_information/"
folder_save="cells_outputs_data_short/"

i=0
# os.system('python run_analysis_fit_after_run.py')
all_data_cell=[]
for cell_name in read_from_pickle('cells_name2.p')[:]: #['2017_03_04_A_6-7']:#
    next_continue=False
    already_save=False

    print(cell_name)
    all_data = []

    moo_total_dict={}
    for loc in tqdm(model2run(cell_name)):
        loc=loc+'/Rins_pickles.p'
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
            full_trace=True
        else:
            full_trace=False
        result_dict=read_from_pickle(loc)
        if "after_shrink" in loc:
            before_after='_after_shrink'
        else:
            before_after="_before_shrink"
        if get_n_spinese(cell_name)>1:
            dict_spine_vol=read_from_pickle(loc[:loc.rfind('/')]+'/AMPA&NMDA_soma_seperete_pickles.p')[1]
            V_AMPA=[max(dict_spine_vol[name]['V_soma_AMPA']) for name in ['voltage_0','voltage_1']]
            V_NMDA=[max(dict_spine_vol[name]['V_soma_NMDA']) for name in ['voltage_0','voltage_1']]
            V_syn_AMPA=[max(dict_spine_vol[name]['V_syn_AMPA']) for name in ['voltage_0','voltage_1']]
            V_syn_NMDA=[max(dict_spine_vol[name]['V_syn_NMDA']) for name in ['voltage_0','voltage_1']]
        else:
            dict_spine_vol=read_from_pickle(loc[:loc.rfind('/')]+'/AMPA&NMDA_soma_pickles.p')['voltage']
            V_AMPA=[max(dict_spine_vol['V_AMPA'])]
            V_NMDA=[max(dict_spine_vol['V_NMDA'])]
            V_syn_AMPA=np.max(dict_spine_vol['V_syn_AMPA'],axis=1)
            V_syn_NMDA=np.max(dict_spine_vol['V_syn_NMDA'],axis=1)

        for i in range(get_n_spinese(cell_name)):
            Moo_dict = {}
            for value in ['PSD','distance','lambda','g_NMDA_spine']:
                Moo_dict[value]=result_dict['parameters'][value][i]
            relative_PSD=result_dict['parameters']['PSD']/max(result_dict['parameters']['PSD'])
            for value in ['W_AMPA','W_NMDA']:
                Moo_dict[value]=result_dict['parameters'][value]*1000*relative_PSD[i]/sum(relative_PSD)

            for value in ['tau1_AMPA','tau2_AMPA','tau1_NMDA','tau2_NMDA','E_PAS','RA','RM','CM']:
                Moo_dict[value]=result_dict['parameters'][value]
            Moo_dict['soma_Rin']=result_dict['soma']['Rin']

            Moo_dict['Rneck']=result_dict['parameters']['Rneck'][i]
            for value in ['neck_base','spine_head']:
                for value1 in ['Rin','Rtrans','V_high']:
                    if len(result_dict[value][value1])>0:
                        Moo_dict[value+'_'+value1]=result_dict[value][value1][i]
                    else:
                        Moo_dict[value+'_'+value1]=result_dict[value][value1]
            Moo_dict['V_soma_NMDA']=V_NMDA[i]-Moo_dict['E_PAS']
            Moo_dict['V_soma_AMPA']=V_AMPA[i]-Moo_dict['E_PAS']
            Moo_dict['V_syn_NMDA']=V_syn_NMDA[i]
            Moo_dict['V_syn_AMPA']=V_syn_AMPA[i]
            moo_total_dict[passive_param_name]=Moo_dict
            for key, value in moo_total_dict.items():
                dict_for_records = {}
                # add metadata
                dict_for_records['cell_name']=cell_name
                dict_for_records['full_trace']=full_trace
                dict_for_records['passive_parameter']=passive_param_name
                dict_for_records['RA']=result_dict['parameters']['RA']
                dict_for_records['relative_relation']=result_dict['parameters']['reletive_strengths']
                dict_for_records['relative']=np.mean(result_dict['parameters']['reletive_strengths'])<1
                dict_for_records['shrinkage_resize']=shrinkage_resize
                dict_for_records['double_spine_area']=double_spine_area
                dict_for_records['from_picture']=cell_name in read_from_pickle('cells_sec_from_picture.p')
                dict_for_records['before_shrink']=before_after.split('_')[1]
                dict_for_records['syn_num']=i
                if value is not None:
                    dict_for_records.update(value)
                all_data.append(dict_for_records)
                if Moo_dict['RA']>50 and not next_continue:
                    if dict_for_records['before_shrink']=='before':continue
                    if cell_name=='2017_04_03_B' and dict_for_records['passive_parameter']!='RA=70':continue
                    if cell_name=='2017_07_06_C_3-4' and dict_for_records['full_trace']==True:continue
                    #if cell_name=='2017_04_03_B' and dict_for_records['before_shrink']=='after':continue
                    #if cell_name!='2017_04_03_B' and dict_for_records['before_shrink']=='before':continue
                    if (cell_name in read_from_pickle('cells_sec_from_picture.p') and dict_for_records['from_picture']) or (not cell_name in read_from_pickle('cells_sec_from_picture.p') and not dict_for_records['from_picture']):
                        all_data_cell.append(dict_for_records)
                        already_save=True
        if already_save:
            next_continue=True



        # all_data.append(dict_for_records)
        # output_df = pd.DataFrame.from_records(all_data)
        # Rin_dict=read_from_pickle(glob(loc[:loc.find('hall_of_fame')]+'Rins_pickles.p')[0])
        # dict_for_records.update(Rin_dict)
        # all_data.append(dict_for_records)

    output_df = pd.DataFrame.from_records(all_data)
    output_df.to_csv(folder_data+cell_name+"/results_MOO"+save_moo+".csv", index=False)
output_df_cells = pd.DataFrame.from_records(all_data_cell)
output_df_cells.to_csv(folder_data+"/results_MOO"+save_moo+".csv", index=False)


    # save_pickle_folder2=folder_+folder_data+cell_name
    # output_df = pd.DataFrame.from_records(all_data)
    # output_df.to_csv(save_pickle_folder2+"/results_MOO"+before_after+".csv", index=False)
    # pickle.dump(dict_fit_condition, open(save_pickle_folder2+"/results_MOO.p", "wb"))
