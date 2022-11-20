import numpy as np
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from add_figure import add_figure
import os
import pickle
from glob import glob
import sys
from extra_function import create_folder_dirr
from tqdm import tqdm
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
print(len(sys.argv),sys.argv,flush=True)
def find_nearest(array, values):
    indices = np.abs(np.subtract.outer(array, values)).argmin(0)
    return indices
if len(sys.argv) != 7:
    cell_name= '2017_03_04_A_6-7'
    file_type='z_correct.swc'
    resize_diam_by=1.0
    shrinkage_factor=1.0
    SPINE_START=20
    double_spine_area='False'
    print("the function doesn't run with sys.argv",flush=True)
else:
    cell_name = sys.argv[1]
    file_type=sys.argv[2] #hoc ar ASC
    resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
    SPINE_START=int(sys.argv[5])
    double_spine_area=eval(sys.argv[6])
    print('the len of sys.argv is correct and running',flush=True)
save_dir = "cells_outputs_data_short/"
folder_=''

# location='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/2017_05_08_A_4-5(0)(0)/fit_short_pulse_ASC/dend*1.0&F_shrinkage=1.0/basic_fit'
# datas2=glob(location+'/*/final_result*.p')
def analysis_fit(location):
    save_folder=location+'/analysis'
    create_folder_dirr(save_folder)
    errors,RAs,RMs,CMs,names,diffrent_condition=[],[],[],[],[],[]
    for dirr in glob(location+'/*/*result*.p'):
        dict=read_from_pickle(dirr)
        errors.append(dict['error']['decay&max'])
        RAs.append(dict['RA'])
        RMs.append(dict['RM'])
        CMs.append(dict['CM'])
        text=dirr.split('/')[-2]
        names.append(text)
        diffrent_condition.append(float(text.split('=')[-1]))
    condition=text.split('=')[-2]
    minimums_arg = np.argsort(errors)
    dict_minimums_total=[]
    for mini in minimums_arg:
        dict_minimums_total.append({'RM': RMs[mini], 'RA': RAs[mini], 'CM': CMs[mini],'error':errors[mini]})
    pickle.dump(dict_minimums_total, open(save_folder + "/RA_total_errors_minimums.p", "wb"))
    dict_minimums={}
    fig=add_figure('diffrent RA against error\n'+dirr.split('/')[-3],'RA','errors')
    plt.plot(RAs,errors,'.')
    for mini in minimums_arg[:10]:
        plt.plot(RAs[mini], errors[mini], '*',
                 label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(
                     round(RAs[mini], 2)) + ' CM=' + str(
                     round(CMs[mini], 2)) +' '+names[mini]+ ' error=' +  str(round(errors[mini], 3)) )
    plt.legend(loc='upper left')
    plt.savefig(save_folder+'/diffrent RA against error.png')
    pickle.dump(fig, open(save_folder+'/diffrent RA against error.p', 'wb'))

    fig1=add_figure('diffrent '+condition+' against CM\n'+dirr.split('/')[-1],condition,'CM')
    plt.plot(diffrent_condition,CMs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against CM.png')
    pickle.dump(fig1, open(save_folder+'/diffrent '+condition+' against CM.p', 'wb'))

    fig2=add_figure('diffrent '+condition+' against RA after fit\n'+dirr.split('/')[-3],'RA0','RA')
    plt.plot(diffrent_condition,RAs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against RA after fit.png')
    pickle.dump(fig2, open(save_folder+'/diffrent '+condition+' against RA after fit.p', 'wb'))

    fig3=add_figure('diffrent '+condition+' against RM\n'+dirr.split('/')[-3],'RA0','RM')
    plt.plot(diffrent_condition,RMs,'.')
    plt.savefig(save_folder+'/diffrent '+condition+' against RM.png')
    pickle.dump(fig3, open(save_folder+'/diffrent '+condition+' against RM.p', 'wb'))

    pickle.dump(dict_minimums, open(save_folder + "/ "+condition+" _10_minimums.p", "wb"))


if __name__ == '__main__':
    print("Do analysis fit:", flush=True)
    initial_folder1=folder_+save_dir+cell_name+'/fit_short_pulse_after_shrink/'
    initial_folder=folder_+save_dir+cell_name+'/fit_short_pulse_after_shrink/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
    initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
    if double_spine_area:
        initial_folder+='_double_spine_area'

    if len(glob(initial_folder+'/basic_fit/analysis/*'))>0:
        analysis_fit(initial_folder+'/basic_fit')

    for loc in glob(initial_folder1+'/*/*/different_initial_conditions/RA*'):
        analysis_fit(loc)


    initial_folder=folder_+save_dir+'/*/fit_short_pulse_after_shrink/'
    paths=glob(save_dir+'/*/fit_short_pulse_after_shrink/z_correct.swc_SPINE_START=20/dend*1.0&F_shrinkage=1.0/const_param/RA/Ra_const_errors.p')
    for data in tqdm(paths):
        save_folder1=data[:data.rfind('/')]+'/analysis'
        try:os.mkdir(save_folder1)
        except FileExistsError:pass
        dict3=read_from_pickle(data)
        RA0=dict3['RA']
        RAs,RMs,CMs,errors=[],[],[],[]
        errors=dict3['error']['decay&max']
        error_all=dict3['error']
        RAs=[value['RA'] for value in dict3['params']]
        RMs=[value['RM'] for value in dict3['params']]
        CMs=[value['CM'] for value in dict3['params']]
        fig3=add_figure('RA const against errors\n'+file_type,'RA const','error')
        fig3.set_size_inches(6,7)
        fig3.subplots_adjust(left=0.2,right=0.95,top=0.9,bottom=0.15)
        plt.plot(RA0,errors)
        minimums_arg=np.argsort(errors)
        dict_minimums_total=[]
        for mini in minimums_arg:
            dict_minimums_total.append({'RM': RMs[mini], 'RA': RAs[mini], 'CM': CMs[mini],'error':errors[mini]})
        pickle.dump(dict_minimums_total, open(save_folder1 + "/RA_total_errors_minimums.p", "wb"))
        dict_minimums2={}
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
            err={}
            for key2 in error_all.keys():
                if 'Rin' in key2: continue
                err[key2]=error_all[key2][mini]
            dict_minimums2['RA_const=' + str(RA0[mini])]={'params': {'RM': RMs[mini], 'RA': RAs[mini], 'CM': CMs[mini]},'error':err }
        pickle.dump(dict_minimums2, open(save_folder1 + "/RA_const_10_minimums.p", "wb"))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors')
        plt.savefig(save_folder1+'/RA const against errors.pdf')
        pickle.dump(fig3, open(save_folder1+'/RA const against errors.p', 'wb'))

        fig4=add_figure('','RA [Ohm*cm]','error')
        fig4.set_size_inches(6,5)
        fig4.subplots_adjust(left=0.2,right=0.95,top=0.9,bottom=0.15)
        plt.plot(RA0,errors)
        RA070= find_nearest(RA0,70)
        RA0120= find_nearest(RA0,120)
        RA0150= find_nearest(RA0,150)
        RA_min= minimums_arg[0]
        RA0_best_fit=find_nearest(errors[RA_min:],0.1)+RA_min
        for mini,name in zip([RA070,RA_min,RA0_best_fit],['RA=70','Ra_min','RA0_best_fit']):
            plt.plot(RA0[mini], errors[mini], '*',label=name+' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)),lw=8)
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors2')
        pickle.dump(fig4, open(save_folder1+'/RA const against errors2.p', 'wb'))
        # plt.show()

        end_plot=60
        fig5=add_figure('RA const against errors\n'+file_type,'RA const','error')
        plt.plot(RA0[:end_plot],errors[:end_plot])
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors until point '+str(end_plot))
        pickle.dump(fig5, open(save_folder1+'/RA const against errors until point '+str(end_plot)+'.p', 'wb'))

        fig6=add_figure('RA const against RMs\n'+file_type,'RA const','RM')
        plt.plot(RA0,RMs)
        plt.savefig(save_folder1+'/RA const against RM')
        pickle.dump(fig6, open(save_folder1+'/RA const against RM.p', 'wb'))

        fig7=add_figure('RA const against RA after fit\n'+file_type,'RA const','RA')
        plt.plot(RA0,RAs)
        plt.savefig(save_folder1+'/RA const against RA after fit')
        pickle.dump(fig7, open(save_folder1+'/RA const against RA after fit.p', 'wb'))

        fig8=add_figure('RA const against CM\n'+file_type,'RA const','CM')
        plt.plot(RA0,CMs)
        plt.savefig(save_folder1+'/RA const against CMs')
        pickle.dump(fig8, open(save_folder1+'/RA const against CMs.p', 'wb'))
