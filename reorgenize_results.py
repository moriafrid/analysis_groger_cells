from open_pickle import read_from_pickle
from glob import glob
import shutil
from read_passive_parameters_csv import get_passive_parameter
from passive_val_function import get_passive_val
data_file='cells_outputs_data_short/'
from extra_function import create_folder_dirr

def copy_file(copy,paste,extra_name=''):
    shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.p'+copy.split('.p')[1])
for cell_name in read_from_pickle('cells_name2.p'):
    data_file='cells_outputs_data_short/'+cell_name
    save_file='final_data/'+cell_name+'/'
    try: shutil.rmtree(save_file)
    except:pass
    create_folder_dirr(save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/syn/clear_syn_after_peeling.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/syn/clear_syn_after_peeling.png')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/short_pulse/clear_short_pulse_after_peeling.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/short_pulse/clear_short_pulse_after_peeling.png')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/*/I_V_curve_fit.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/*/I_V_curve_fit.p')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_taus.png')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_taus.p')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_tau_m.png')[0],save_file)
    copy_file(glob(data_file+'/fit_short_pulse/tau_m_calculation/calculate_tau_m.p')[0],save_file)

    shrinkage_by=1.0
    resize_diam_by=1.0
    resize='F_shrinkage='+str(shrinkage_by)+'_dend*'+str(resize_diam_by)
    save_file_resize='final_data/'+cell_name+'/'+resize+'/'

    create_folder_dirr(save_file_resize)
    copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.png')[0],save_file_resize)
    copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.png')[0],save_file_resize)

    #the best fit

    passive_result=glob(data_file+'/MOO_results_syn_par*/z_correct.swc_SPINE_START=20/'+resize+'/const_param/*/fit_transient_RDSM.p')

    next_continue=[]
    for passive_val_name in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if next_continue: continue
        passive_vals_dict=get_passive_parameter(cell_name,double_spine_area='False',shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition='const_param',spine_start=20,file_type='z_correct.swc')
        RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name])
        if float(RA)<50:
            continue
        else:
            if float(RA)>70:
                next_continue=True
        # copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.png')[0],save_file_resize)
        # copy_file(glob(data_file+'/fit_short_pulse/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.png')[0],save_file_resize)



        # copy_file(glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf'))
        # copy_file(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')
        # copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.png')[0],save_file_resize,extra_name='same')
        # copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.p')[0],save_file_resize,extra_name='same')
        #
        # copy_file(glob(data_file+'/MOO_results_syn_par_same_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/'+passive_val_name+'/fit_transient_RDSM.png',extra_name='same')
        #
        # copy_file(glob(data_file+'/MOO_results_syn_par_relative_strange/z_correct.swc_SPINE_START=20/'+resize+'/const_param/RA_best_fit/fit_transient_RDSM.png',extra_name='same')
        #
        # copy_file(glob('/MOO_results_syn_par__same_strange/ASC_SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/RA_best_fit/befor_simulation.txt'))
