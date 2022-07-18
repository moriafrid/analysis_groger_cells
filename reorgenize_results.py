import re

from matplotlib import pyplot as plt

from open_pickle import read_from_pickle
from glob import glob
import shutil
from read_passive_parameters_csv import get_passive_parameter
from passive_val_function import get_passive_val
from read_spine_properties import get_parameter

data_file='cells_outputs_data_short/'
from extra_function import create_folder_dirr

def copy_file(copy,paste,extra_name=''):
    if extra_name!='':
        extra_name='_'+extra_name
    if 'txt' in copy:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.txt')[0]+extra_name+'.txt'+copy.split('.txt')[1])
    else:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.p'+copy.split('.p')[1])
    if 'png' not in copy:
        fig=read_from_pickle(copy)
        # plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.png')
        plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.svg')
        plt.close()
for cell_name in read_from_pickle('cells_name2.p'):
    if cell_name not in ['2017_07_06_C_4-3','2016_04_16_A']:continue
    print(cell_name)

    shrinkage_by=1.0
    resize_diam_by=1.0

    data_file='cells_outputs_data_short/'+cell_name
    save_file='final_data/'+cell_name+'/'

    try: shutil.rmtree(save_file)
    except:pass
    create_folder_dirr(save_file)
    copy_file(glob(data_file+'/neuron_morphology_fig.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/syn/clear_syn_after_peeling.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/short_pulse/clear_short_pulse_after_peeling.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/*/I_V_curve_fit.p')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_taus.p')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_tau_m.p')[0],save_file)
    copy_file(glob(data_file+'/data/check_dynamic/check_dynamics.p')[0],save_file)

    save_file_resize=save_file
    resize='F_shrinkage='+str(shrinkage_by)+'_dend*'+str(resize_diam_by)
    copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.p')[0],save_file_resize)

    #the best fit
    next_continue=[]
    for passive_val_name in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if next_continue: continue
        passive_vals_dict=get_passive_parameter(cell_name,double_spine_area='False',shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition='const_param',spine_start=20,file_type='z_correct.swc')
        RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
        RA=str(int(float(RA)))
        if float(RA)<50:
            continue
        else:
            if float(RA)>70:
                next_continue=True
        copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.png')[0],save_file_resize,extra_name=passive_val_name)
        copy_file(glob(data_file+'/data/electrophysio_records/*IV*/-50pA.png')[0],save_file_resize,extra_name=passive_val_name)

        copy_file(glob(data_file+'/data/cell_properties/z_correct.swc/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/E_dendogram/dend_only_with_syn.p')[0],save_file_resize)
        copy_file(glob(data_file+'/data/cell_properties/z_correct.swc/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/M_dendogram/dend_only.p')[0],save_file_resize)

        try:
            copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/fit_transient_RDSM.p')[0],save_file_resize,extra_name='full_same_'+passive_val_name)
            copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/data.txt')[0],save_file_resize,extra_name='full_same_'+passive_val_name)
            copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.p')[0],save_file_resize,extra_name='same_'+passive_val_name)

        except:
            print(cell_name,"don't finish to MOO, same_syn")

        if get_parameter(cell_name,'n_syn')[0]>1:
            try:
                copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/fit_transient_RDSM.p')[0],save_file_resize,extra_name='full_relative_'+passive_val_name)
                copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/data.txt')[0],save_file_resize,extra_name='full_relative_'+passive_val_name)
                copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.p')[0],save_file_resize,extra_name='relative_'+passive_val_name)

            except:
                print(cell_name,"don't finish to MOO, relative_syn")
        # copy_file(glob(data_file+'/MOO_results_syn_par__same_strange/ASC_SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/RA_best_fit/befor_simulation.txt'))



cell_name='2017_05_08_A_4-5'
data_file='cells_outputs_data_short/'+cell_name

files=glob('cells_outputs_data_short/2017_05_08_A_4-5/MOO_results_syn_par_same_strange/*_SPINE_START=20/*')
for p in files:
    resize=p.split('/')[-1]
    file_type=p.split('/')[-2]
    save_file_resize='final_data/'+cell_name+'/'+resize+'/'
    create_folder_dirr(save_file_resize)
    shrinkage_by,resize_diam_by=[float(par) for par in re.findall("\d+\.\d+", resize)]
    double_spine_area='False'
    if 'double' in p:
        double_spine_area='True'
    copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.p')[0],save_file_resize)

    #the best fit
    next_continue=[]
    for passive_val_name in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if next_continue: continue
        passive_vals_dict=get_passive_parameter(cell_name,double_spine_area=double_spine_area,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition='const_param',spine_start=20,file_type='z_correct.swc')
        RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
        RA=str(int(float(RA)))
        if float(RA)<70:
            continue
        else:
            if float(RA)>70:
                next_continue=True
        copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.png')[0],save_file_resize,extra_name=passive_val_name)

        # copy_file(glob(data_file+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/E_dendogram/dend_only_with_syn.p')[0],save_file_resize)
        # copy_file(glob(data_file+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/M_dendogram/dend_only.p')[0],save_file_resize)
        try:
            copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/fit_transient_RDSM.p')[0],save_file_resize,extra_name='full_same_'+passive_val_name)
            copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.p')[0],save_file_resize,extra_name='same_'+passive_val_name)
        except:
            print(cell_name,"don't finish to MOO, same_syn")

        if get_parameter(cell_name,'n_syn')[0]>1:
            try:
                copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'_full_trace/fit_transient_RDSM.p')[0],save_file_resize,extra_name='full_relative_'+passive_val_name)
                copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'*/fit_transient_RDSM.p')[0],save_file_resize,extra_name='relative_'+passive_val_name)
            except:
                print(cell_name,"don't finish to MOO, relative_syn")
        # copy_file(glob(data_file+'/MOO_results_syn_par__same_strange/ASC_SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/RA_best_fit/befor_simulation.txt'))
