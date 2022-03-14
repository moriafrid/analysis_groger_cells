from open_pickle import read_from_pickle
import numpy as np
from neuron import h,gui
import  matplotlib.pyplot as plt
from calculate_F_factor import calculate_F_factor
from add_figure import add_figure
import pickle
from extra_function import load_ASC,load_hoc,load_swc,SIGSEGV_signal_arises,create_folder_dirr
from extra_fit_func import find_injection
import pandas as pd
import sys
from glob import glob
import signal
import os
from analysis_fit_after_run import analysis_fit
# initial_folder = "data/fit/"
do_calculate_F_factor=True
if len(sys.argv) != 7:
   cell_name= '2017_03_04_A_6-7'
   file_type='z_correct.swc'
   resize_diam_by=1.0
   shrinkage_factor=1.0
   SPINE_START=20
   folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
   cell_name = sys.argv[1]
   file_type=sys.argv[2] #hoc ar ASC
   resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
   shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
   SPINE_START=int(sys.argv[5])
   folder_= sys.argv[6] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
path_short_pulse=glob(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')[0]
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]

initial_folder=folder_+save_dir+cell_name+'/fit_short_pulse/'+file_type+'_SPINE_START='+str(SPINE_START)+'/'
initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
initial_folder +="/const_param/RA"
create_folder_dirr(initial_folder)

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

def read_tau_m(cell_name,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'):
    df = pd.read_excel(save_dir+'/tau_m_cells.xlsx',index_col=0)
    return df[cell_name]['tau_m']

def change_model_pas(CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0):
   h.dt = 0.1
   h.distance(0,0.5, sec=soma)
   for sec in cell.all_sec():
       sec.Ra = RA
       sec.cm = CM  # *shrinkage_factor    #*(1.0/0.7)
       sec.g_pas = (1.0 / RM)  #*shrinkage_factor  #*(1.0/0.7)
       sec.e_pas = E_PAS
   for sec in cell.dend:
       for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
           if h.distance(seg) > SPINE_START:
               seg.cm *= F_factor
               seg.g_pas *= F_factor


def plot_res(RM, RA, CM, save_folder="data/fit/",save_name= "fit"):
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS = E_PAS)
    Vvec = h.Vector()
    Tvec = h.Vector()
    Vvec.record(soma(0.5)._ref_v)
    Tvec.record(h._ref_t)
    h.cvode.store_events(Vvec)
    h.run()
    npTvec = np.array(Tvec)
    npVec = np.array(Vvec)
    add_figure(cell_name+" fit "+save_folder.split('/')[-2]+"\nRM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),'mS','mV')
    plt.plot(T, V, color = 'black',alpha=0.3,label='data',lw=2)
    plt.plot(T[start_fit:end_fit], V[start_fit:end_fit], color = 'b',alpha=0.3,label='fit decay')
    plt.plot(T[max2fit-1200:max2fit], V[max2fit-1200:max2fit],color = 'yellow',label='fit maxV')
    plt.plot(npTvec, npVec, color = 'r', linestyle ="--",alpha=0.3,label='NEURON simulation')


    exp_V = V
    npVec = npVec
    npVec = npVec[:len(exp_V)]
    error_1 = np.sqrt(np.sum(np.power(np.mean(exp_V[:start]) - np.mean(npVec[:start]), 2)))  # error from mean rest
    error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))/(end_fit-start_fit))  #  error for the decay
    # error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))) #/(end_fit-start_fit)  #  error for the decay
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit-1200:max2fit]) - np.mean(npVec[max2fit-1200:max2fit]), 2)))  # error for maximal voltage
    error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2))/len(exp_V)) # mean square error

    print('error_total=',round(error_tot,3))
    print('error_decay=', round(error_2,3))
    print('error_mean_max_voltage=', round(error_3,3))
    print('error_from_rest=', round(error_1,3))
    plt.plot(T[0],exp_V[0],'white',label='error_decay&max='+str(error_2 + error_3))
    plt.legend(loc='best')
    plt.savefig(save_folder+'/'+save_name+".png")
    # plt.savefig(save_folder+'/'+save_name+".pdf")
    plt.close()
    return error_2 ,error_2 + error_3
def errors_Rinput(RM,RA,CM,E_PAS):
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS = E_PAS)
    Vvec = h.Vector()
    Tvec = h.Vector()
    Vvec.record(soma(0.5)._ref_v)
    Tvec.record(h._ref_t)
    h.cvode.store_events(Vvec)
    h.dt=0.1
    h.run()
    npTvec = np.array(Tvec)
    npVec = np.array(Vvec)
    exp_V = V
    npVec = npVec
    npVec = npVec[:len(exp_V)]
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit-1200:max2fit]) - np.mean(npVec[max2fit-1200:max2fit]), 2)))  # error for maximal voltage
    # print('error_mean_max_voltage=', round(error_3,3))
    return error_3

if __name__=='__main__':
    I = -50
    short_pulse=read_from_pickle(path_short_pulse)
    cell=None
    if file_type=='ASC':
       cell =load_ASC(cell_file)
    elif file_type=='hoc':
       cell =load_hoc(cell_file)
    elif 'swc' in file_type:
        cell =load_swc(cell_file)
    sp = h.PlotShape()
    sp.show(0)  # show diameters

    # ## delete all the axons
    # for sec in cell.axon:
    #     h.delete_section(sec=sec)
    for sec in cell.all_sec():
        sec.insert('pas') # insert passive property
        sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances

    for sec in cell.all_sec():
        sec.diam = sec.diam*resize_diam_by
        sec.L*=shrinkage_factor
    SPINE_START = 60
    hz= 0.1

    if do_calculate_F_factor:
        F_factor=calculate_F_factor(cell,'mouse_spine')
    else:
        F_factor = 1.9
    soma=cell.soma

    ######################################################
    # load the data and see what we have
    ######################################################
    V = np.array(short_pulse['mean'][0])
    T = np.array(short_pulse['mean'][1].rescale('ms'))
    T = T-T[0]
    E_PAS = short_pulse['E_pas']
    start,end=find_injection(V, E_PAS,duration=int(200/hz))
    start_fit= start-100
    end_fit=end-1200
    max2fit=end-10
    clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
    clamp.amp = I/1000 #pA
    clamp.delay = T[start]#296
    clamp.dur =T[end]-T[start]# 200 #end-start

    h.dt=hz
    h.tstop = (T[-1]-T[0])
    h.v_init=E_PAS
    h.steps_per_ms = h.dt
    imp = h.Impedance(sec=soma)
    imp.loc(soma(0.5))
    RA=list(np.arange(1,150,1))+list(np.arange(150, 302, 2))
    if read_tau_m(cell_name)==[]:
        os.system('calculate_tau_m.py')
        print('tau_m for cell',cell_name, ' needs to be calculate')
    tau_m=read_tau_m(cell_name)#25716 in cell4-5#ms*10^3=micro
    d=soma.diam
    ra_error=[]
    params_dict=[]
    precent_erors=[]
    ra_error_next=[]
    for ra in RA:
        RM=6000
        CM=tau_m/RM
        imp.compute(0)
        Rin = imp.input(0)
        error_last=errors_Rinput(RM, ra, CM,E_PAS)
        error_next=error_last
        while error_next<=error_last:
            RM+=20
            CM=tau_m/RM
            change_model_pas(CM=CM, RA = ra, RM = RM, E_PAS = E_PAS)
            imp.compute(0)
            Rin=imp.input(0)
            # print('Rin='+str(round(rin,3)))
            # RM=(Rin*pi)**2/4*d**3*ra
            error_last=error_next
            error_next=errors_Rinput(RM, ra, CM,E_PAS)
        print(RM)
        RM-=35
        CM = tau_m / RM
        change_model_pas(CM=CM, RA=ra, RM=RM, E_PAS=E_PAS)
        imp.compute(0)
        Rin = imp.input(0)
        error_last = errors_Rinput(RM, ra, CM, E_PAS)
        error_next = errors_Rinput(RM, ra, CM, E_PAS)
        while error_next<=error_last:
            RM+=1
            CM=tau_m/RM
            change_model_pas(CM=CM, RA = ra, RM = RM, E_PAS = E_PAS)
            imp.compute(0)
            Rin=imp.input(0)
            # print('Rin='+str(round(rin,3)))
            # RM=(Rin*pi)**2/4*d**3*ra
            error_last=error_next
            error_next=errors_Rinput(RM, ra, CM,E_PAS)
        print('Rinput for Ra='+str(ra)+' is '+str(round(Rin,2)))
        ra_error2,precent_eror=plot_res(RM, ra, CM, save_folder=initial_folder, save_name="fit RA=" + str(round(ra, 2)))
        ra_error.append(ra_error2)
        precent_erors.append(precent_eror)
        ra_error_next.append(error_next)
        params_dict.append({'RM': RM, 'RA': ra, 'CM': CM})
        pickle.dump({'RA':RA,'error':{'decay':ra_error,'decay&max':precent_erors},'params':params_dict}, open(initial_folder + '/Ra_const_errors.p', "wb"))
    add_figure('RA_errors','RA','errors')
    plt.plot(RA,ra_error)
    plt.savefig(initial_folder + '/Ra_const_errors1.png')
    add_figure('RA_errors','RA','ra_next_eror')
    plt.plot(RA,ra_error_next)
    plt.savefig(initial_folder + '/Ra_const_errors2.png')
    print('fit_best_with_const_param.py is complite to run')


    # analysis_fit(initial_folder)
    initial_locs=glob(folder_+save_dir+cell_name+'/fit_short_pulse_'+file_type+'/')
    for loc in initial_locs:
        data=glob(initial_folder+'/Ra_const_errors.p')[0]
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
        add_figure('RA const against errors\n'+loc.split('/')[-1],'RA const','error')
        plt.plot(RA0,errors)
        minimums_arg=np.argsort(errors)
        dict_minimums2={}
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
            dict_minimums2['RA_const=' + str(RA0[mini])]={'params': {'RM': RMs[mini], 'RA': RAs[mini], 'CM': CMs[mini]},'error':{key2:error_all[key2][mini] for key2 in error_all.keys()} }
        pickle.dump(dict_minimums2, open(save_folder1 + "/RA_const_10_minimums.p", "wb"))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors')
        plt.savefig(save_folder1+'/RA const against errors.pdf')

        end_plot=60
        add_figure('RA const against errors\n'+loc.split('/')[-1],'RA const','error')
        plt.plot(RA0[:end_plot],errors[:end_plot])
        for mini in minimums_arg[:10]:
            plt.plot(RA0[mini], errors[mini], '*',label=' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                         round(CMs[mini], 2)) + ' error=' +  str(round(errors[mini], 3)))
        plt.legend(loc='upper left')
        plt.savefig(save_folder1+'/RA const against errors until point '+str(end_plot))

        add_figure('RA const against RMs\n'+loc.split('/')[-1],'RA const','RM')
        plt.plot(RA0,RMs)
        plt.savefig(save_folder1+'/RA const against RM')
        add_figure('RA const against RA after fit\n'+loc.split('/')[-1],'RA const','RA')
        plt.plot(RA0,RAs)
        plt.savefig(save_folder1+'/RA const against RA after fit')
        add_figure('RA const against CM\n'+loc.split('/')[-1],'RA const','CM')
        plt.plot(RA0,CMs)
        plt.savefig(save_folder1+'/RA const against CMs')


