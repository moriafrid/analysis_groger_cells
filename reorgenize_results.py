
import re
from matplotlib import pyplot as plt
from open_pickle import read_from_pickle
from glob import glob
import shutil
from read_passive_parameters_csv import get_passive_parameter
from passive_val_function import get_passive_val
from read_spine_properties import get_n_spinese
from extra_function import create_folder_dirr
import sys
if len(sys.argv) != 4:
    specipic_cell='*'
    before_after='_after_shrink'
    specipic_moo='_correct_seg_syn_from_picture' #_correct_seg_find_syn_xyz
    print("sys.argv isn't run")
else:
    print("the sys.argv len is correct",flush=True)
    specipic_cell = sys.argv[1]
    if specipic_cell=='None':
        specipic_cell='*'
    before_after=sys.argv[2]
    specipic_moo= sys.argv[3]


data_file='cells_outputs_data_short/'


def copy_file(copy,paste,extra_name=''):
    if extra_name!='':
        extra_name='_'+extra_name
    if 'txt' in copy:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.txt')[0]+extra_name+'.txt'+copy.split('.txt')[1])
    else:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.p'+copy.split('.p')[1])
    if 'png' not in copy and 'final_pop' not in copy and "pickles" not in copy:
        try:
            fig=read_from_pickle(copy)
            plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.png')
            # plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.svg')
            plt.close()
        except:
            print('')
#need to run again with 3,5,8 if os.system is runing
for cell_name in read_from_pickle('cells_name2.p'):
    # if cell_name!='2017_03_04_A_6-7':continue
    # if not cell_name in ['2017_07_06_C_4-3','2017_07_06_C_3-4','2017_03_04_A_6-7']:continue
    if cell_name=='2017_07_06_C_3-4':
        full=''
    else:
        full='_full_trace'
    save_file='final_data/'+specipic_moo[1:]+'/'+cell_name+'/'
    data_file='cells_outputs_data_short/'+cell_name+'/'

    MOO_relative='MOO_results_relative_strange'+before_after+specipic_moo+'/z_correct.swc_SPINE_START=20/'
    MOO_same='MOO_results_same_strange'+before_after+specipic_moo+'/z_correct.swc_SPINE_START=20/'
    # MOO_same=MOO_relative
    short_pulse='/fit_short_pulse'+before_after+'/'
    print(cell_name)

    shrinkage_by=1.0
    resize_diam_by=1.0
    try: shutil.rmtree(save_file)
    except:pass
    create_folder_dirr(save_file)
    copy_file(glob(data_file+'/neuron_morphology_fig.p')[0],save_file)
    copy_file(glob(data_file+'/neuron_morphology_fig.p')[0],save_file)
    copy_file(glob(data_file+'data/cell_properties/morphology_z_correct_before_shrink.swc/diam_dis/diam-dis.p')[0],save_file,extra_name='before_shrink')
    copy_file(glob(data_file+'data/cell_properties/morphology_z_correct.swc/diam_dis/diam-dis.p')[0],save_file,extra_name='after_shrink')
    copy_file(glob(data_file+'data/cell_properties/*XYZ.ASC/diam_dis/diam-dis.p')[0],save_file,extra_name='XYZ_ASC')

    copy_file(glob(data_file+'/data/electrophysio_records/syn/clear_syn_after_peeling.p')[0],save_file)

    copy_file(glob(data_file+'/data/electrophysio_records/short_pulse/clear_short_pulse_after_peeling.p')[0],save_file)
    copy_file(glob(data_file+'/data/electrophysio_records/*/I_V_curve_fit.p')[0],save_file)
    copy_file(glob(data_file+short_pulse+'tau_m_calculation/calculate_taus.p')[0],save_file)
    copy_file(glob(data_file+short_pulse+'tau_m_calculation/calculate_tau_m.p')[0],save_file)
    copy_file(glob(data_file+'/data/check_dynamic/check_dynamics.p')[0],save_file)

    save_file_resize=save_file
    resize='F_shrinkage='+str(shrinkage_by)+'_dend*'+str(resize_diam_by)
    copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.p')[0],save_file_resize)
    copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA_total_errors_minimums.p')[0],save_file_resize)

    #the best fit
    next_continue=[]
    for passive_val_name in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if next_continue: continue
        passive_vals_dict=get_passive_parameter(cell_name,before_after,double_spine_area='False',shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition='const_param',spine_start=20,file_type='z_correct.swc',passive_param_name=passive_val_name)
        if len(full)>0:
            full2='full_'
        else:
            full2=''
        RA,CM,RM=get_passive_val(passive_vals_dict,what_return='full_result')
        if RA<50:
            continue
        else:
            if RA>70:
                next_continue=True
        dirr_passive_result=glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/')[0]
        # os.system(" ".join(["python plot_fit_short_pulse.py",cell_name,str(RM), str(RA), str(CM),str(resize_diam_by),str(shrinkage_by),str(passive_val_name),before_after]))

        copy_file(dirr_passive_result+passive_val_name+'_pickles.p',save_file_resize)

        RA=str(int(float(RA)))
        copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.p')[0],save_file_resize,extra_name=passive_val_name)
        copy_file(glob(data_file+'/data/electrophysio_records/*IV*/-50pA.p')[0],save_file_resize,extra_name=passive_val_name)
        copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/E_dendogram/dend_only_with_syn.p')[0],save_file_resize)
        copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/M_dendogram/dend_only.p')[0],save_file_resize)

        # copy_file(glob(data_file+'/data/cell_properties/z_correct.swc/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/E_dendogram/dend_only_with_syn.p')[0],save_file_resize)
        # copy_file(glob(data_file+'/data/cell_properties/z_correct.swc/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/M_dendogram/dend_only.p')[0],save_file_resize)

        try:
            if get_n_spinese(cell_name)>1:
                for MOO_file in glob(data_file+MOO_relative+resize+'/const_param/'+passive_val_name+full+'/*.p'):
                    if 'before' in MOO_file.split('/')[-1]:continue
                    # print(MOO_file)
                    copy_file(MOO_file,save_file_resize,extra_name=full2+'relative_'+passive_val_name)
                copy_file(glob(data_file+MOO_relative+resize+'/const_param/'+passive_val_name+full+'/data.txt')[0],save_file_resize,extra_name=full2+'relative_'+passive_val_name)

            else:
                for MOO_file in glob(data_file+MOO_same+resize+'/const_param/'+passive_val_name+full+'/*.p'):
                    if 'before' in MOO_file.split('/')[-1]:continue
                    copy_file(MOO_file,save_file_resize,extra_name=full2+passive_val_name)
                copy_file(glob(data_file+MOO_same+resize+'/const_param/'+passive_val_name+full+'/data.txt')[0],save_file_resize,extra_name=+full2+passive_val_name)

        except: "the moo isn't finish"

cell_name='2017_05_08_A_4-5'
data_file='cells_outputs_data_short/'+cell_name

files=glob(data_file+MOO_same+'/*')
for p in files:
    resize=p.split('/')[-1]
    file_type=p.split('/')[-2]
    save_file_resize='final_data'+before_after+'/'+cell_name+'/'+resize+'/'
    create_folder_dirr(save_file_resize)
    shrinkage_by,resize_diam_by=[float(par) for par in re.findall("\d+\.\d+", resize)]
    double_spine_area='False'
    if 'double' in p:
        double_spine_area='True'
    copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA const against errors2.p')[0],save_file_resize)
    copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/analysis/RA_total_errors_minimums.p')[0],save_file_resize)

    #the best fit
    next_continue=[]
    for passive_val_name in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if next_continue: continue
        passive_vals_dict=get_passive_parameter(cell_name,before_after,double_spine_area=double_spine_area,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition='const_param',spine_start=20,file_type='z_correct.swc')
        RA,CM,RM=get_passive_val(passive_vals_dict[passive_val_name],what_return='full_result')
        RA=str(int(float(RA)))
        if float(RA)<70:
            continue
        else:
            if float(RA)>70:
                next_continue=True
        # dirr_passive_result=glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/')[0]
        # os.system(" ".join(["python plot_fit_short_pulse.py",cell_name,str(RM), str(RA), str(CM),str(resize_diam_by),str(shrinkage_by),str(passive_val_name),before_after]))

        # dict_passive_results_file=plot_res_short_pusle(glob(data_file+short_pulse+'/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/')[0] ,float(RM), float(RA), float(CM),resize_diam_by=resize_diam_by,shrinkage_factor=shrinkage_by,passive_val_name=passive_val_name)
        # copy_file( dirr_passive_result+passive_val_name+'_results.p',save_file_resize)

        copy_file(glob(data_file+short_pulse+'z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/fit RA='+RA+'.p')[0],save_file_resize,extra_name=passive_val_name)

        # copy_file(glob(data_file+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/E_dendogram/dend_only_with_syn.p')[0],save_file_resize)
        # copy_file(glob(data_file+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/'+passive_val_name+'/M_dendogram/dend_only.p')[0],save_file_resize)
        for MOO_file in glob(data_file+MOO_same+resize+'/const_param/'+passive_val_name+'_full_trace/*.p'):
            if 'before' in MOO_file.split('/')[-1]:continue
            copy_file(MOO_file,save_file_resize,extra_name='full_relative_'+passive_val_name)
        copy_file(glob(data_file+MOO_same+resize+'/const_param/'+passive_val_name+'_full_trace/data.txt')[0],save_file_resize,extra_name='full_same_'+passive_val_name)
