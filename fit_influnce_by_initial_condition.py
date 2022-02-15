from open_pickle import read_from_pickle
import numpy as np
from neuron import h,gui
import os
import  matplotlib.pyplot as plt
from calculate_F_factor import calculate_F_factor
from add_figure import add_figure
import pickle
import signal
from glob import glob
import sys
from extra_function import load_ASC,load_hoc,SIGSEGV_signal_arises,create_folder_dirr,create_folders_list
from extra_fit_func import find_injection


do_calculate_F_factor=False
spine_type="mouse_spine"
print(sys.argv,flush=True)
if len(sys.argv) != 6:
    cell_name= '2017_03_04_A_6-7'
    file_type='ASC'
    resize_diam_by=1
    shrinkage_factor=1
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
   cell_name = sys.argv[1]
   file_type=sys.argv[2] #hoc ar ASC
   resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
   shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
   folder_= sys.argv[5] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
   if not folder_.endswith("/"):
       folder_ += "/"
data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
print(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')
short_pulse_file=glob(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')[0]

print(folder_+data_dir+cell_name+'/*'+file_type)
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]
initial_folder=folder_+save_dir+cell_name+'/fit_short_pulse_'+file_type+'/'
# initial_folder+=spine_type
initial_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
initial_folder+="/different_initial_conditions/"
create_folder_dirr(initial_folder)
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

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

def plot_res(RM, RA, CM, save_folder="data/fit/",save_name= "fit",print_full_graph=False):
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS = E_PAS)
    Vvec = h.Vector()
    Tvec = h.Vector()
    Vvec.record(soma(0.5)._ref_v)
    Tvec.record(h._ref_t)
    h.cvode.store_events(Vvec)
    h.run()
    npTvec = np.array(Tvec)
    npVec = np.array(Vvec)
    add_figure("fit "+save_folder.split('/')[-1]+"\nRM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),'mS','mV')
    plt.plot(npTvec[start_fit:end_fit], npVec[start_fit:end_fit], color = 'r', linestyle ="--")
    plt.plot(T[start_fit:end_fit], V[start_fit:end_fit], color = 'green')
    plt.legend(['NEURON_sim','decay_to_fitting'])
    plt.savefig(save_folder+'/'+save_name+"_decay.png")
    # plt.savefig(save_folder+'/'+save_name+"_decay.pdf")
    plt.close()
    exp_V = V
    npVec = npVec
    npVec = npVec[:len(exp_V)]
    error_1 = np.sqrt(np.sum(np.power(np.mean(exp_V[:start_fit-10]) - np.mean(npVec[:start_fit-10]), 2)))  # error from mean rest
    error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))/(end_fit-start_fit))  #  error for the decay
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[end_fit-800:end_fit]) - np.mean(npVec[end_fit-800:end_fit]), 2)))  # error for maximal voltage
    error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2))/len(exp_V)) # mean square error

    print('error_total=',round(error_tot,3))
    print('error_decay=', round(error_2,3))
    print('error_mean_max_voltage=', round(error_3,3))
    print('error_from_rest=', round(error_1,3))
    return error_2, (error_2 + error_3*10)/960

def efun(vals):
   #check the fitting
   # if the parameter incloud the fitting (not aqual to 1) check that the result is makes sense, if not return 1e6
   # if the result is make sense calculate the error between the record simulation and the initial data record
   ## *_IX is the parameter we play with them
   ## *_const is the basic parameters we return if the  result doesn't make sense
   if RM_IX != -1 :
       if vals.x[RM_IX] > 100000:
           return (1e6)
       RM = vals.x[RM_IX]
   else: RM = RM_const

   if CM_IX != -1:
       if vals.x[CM_IX] >3 :
           return (1e6)
       CM = vals.x[CM_IX]
   else:CM = CM_const

   if RA_IX != -1:
       if vals.x[RA_IX] > 300:
           return (1e6)
       RA = vals.x[RA_IX]
   else:RA = RA_const
   if (CM < 0.3 or RM < 2000 or RA <50):
       return 1e6
   # print('RA:',RA, '   CM:',CM, '   RM:',RM)

   change_model_pas(CM=CM, RA=RA, RM = RM, E_PAS = E_PAS)
   Vvec = h.Vector()
   Vvec.record(soma(0.5)._ref_v)

   h.run()
   npVec = np.array(Vvec)

   exp_V = V     #[int(180.0/h.dt):int(800.0/h.dt)]
   npVec = npVec #[int(180.0/h.dt):int(800.0/h.dt)]
   npVec = npVec[:len(exp_V)]
   error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2)))#/len(exp_V)) # mean square error


   error_1 = np.sqrt(np.sum(np.power(np.mean(exp_V[:start_fit]) - np.mean(npVec[:start_fit]), 2)))  # error from mean rest
   error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))) #/(end_fit-start_fit)  #  error for the decay
   error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[end_fit-800:end_fit]) - np.mean(npVec[end_fit-800:end_fit]), 2)))  # error for maximal voltage

   return error_2 + (end_fit-start_fit)*error_3


def fit2short_pulse(cell,short_pulse,folder="",CM=1,RM=10000,RA=100):
    opt_vals = h.Vector(3)
    opt_vals.x[RM_IX] =RM
    opt_vals.x[RA_IX] = RA
    opt_vals.x[CM_IX] = CM
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS=E_PAS)
    plot_res(CM=CM, RM=RM, RA=RA,save_folder=folder, save_name=" before")
    for i in range(3):
        RMSD = h.fit_praxis(efun,opt_vals)   #@# take too much time if the fitting isn't found
        RM = opt_vals.x[RM_IX]
        RA = opt_vals.x[RA_IX]
        CM = opt_vals.x[CM_IX]

        print("RMSD", RMSD,", RM",  RM, ", RA",  RA, ", CM",  CM)
        error2,precent_error=plot_res(CM=CM, RM=RM, RA=RA, save_folder=folder,save_name="_fit_after_" + str(i + 1))
    pickle.dump({
        "RM": RM,
        "RA": RA,
        "CM": CM,
        "error":[RMSD,error2,precent_error]
    }, open(folder+"/fit_result.p", "wb"))
    return {"CM": CM,"RM": RM,"RA": RA,"error":[error2,precent_error,RMSD]}
if __name__=='__main__':
    I = -50 #pA
    hz=0.1
    cell=None
    if file_type=='ASC':
       cell =load_ASC(cell_file)
    elif file_type=='hoc':
       cell =load_hoc(cell_file)

    sp = h.PlotShape()
    sp.show(0)  # show diameters
    for sec in h.allsec():
        sec.diam = sec.diam*resize_diam_by
        sec.L*=shrinkage_factor
    # ## delete all the axons
    # for sec in cell.axon:
    #     h.delete_section(sec=sec)
    for sec in h.allsec():
        sec.insert('pas') # insert passive property
        sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances

    if do_calculate_F_factor:
       F_factor=calculate_F_factor(cell,'mouse_spine')
    else:
       F_factor = 1.9

    ######################################################
    # load the data and see what we have
    ######################################################
    short_pulse=read_from_pickle(short_pulse_file)

    V = np.array(short_pulse['mean'][0])
    T = np.array(short_pulse['mean'][1].rescale('ms'))
    T = T-T[0]
    SPINE_START = 60

    start,end=find_injection(V,duration=int(200/hz))
    soma=cell.soma
    clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
    clamp.amp = I/1000 #pA
    clamp.delay = T[start]#296
    clamp.dur =T[end]-T[start]# 200 #end-start
    E_PAS=np.mean(V[:start])#short_pulse['E_pas']#np.mean(V[:start]) #or read it from the pickle
    start_fit= start#2000   #moria
    end_fit=end-100#4900#3960  #moria
    E_PAS = short_pulse['E_pas']
    h.tstop = (T[-1]-T[0])
    h.v_init=E_PAS
    h.dt = hz
    h.steps_per_ms = h.dt
    CM_IX = 2
    RM_IX=0
    RA_IX = 1

    RM_const = 60000.0
    RA_const = 100.0
    CM_const = 1.0
    print("free params:")
    h.attr_praxis(1e-9,1000,0)

    CM = 1  # 2/2
    RM = 5684*2  # *2
    RA = 100

    ra_folder = initial_folder + "/RA0_50:100:0.5"
    create_folders_list([ra_folder])
    RAs = np.arange(50,100,0.5)
    solution_RA0={}
    for ra in RAs:
        folder = ra_folder + "/RA0=" + str(ra)
        create_folders_list([folder])
        solution_RA0["RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=CM, RM=RM, RA=ra)
        pickle.dump(solution_RA0, open(ra_folder + "/RA0_fit_results.p", "wb"))

    ra_folder = initial_folder + "/RA0_100:300:2"
    create_folders_list([ra_folder])
    RAs = np.arange(100,300,2.)
    solution_RA0={}
    for ra in RAs:
        folder = ra_folder + "/RA0=" + str(ra)
        create_folders_list([folder])
        solution_RA0["RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=CM, RM=RM, RA=ra)
        pickle.dump(solution_RA0, open(ra_folder + "/RA0_fit_results.p", "wb"))
    # cm_folder = initial_folder+"/CM0"
    # try:os.mkdir(cm_folder)
    # except FileExistsError:pass
    # CMs=[0.5,0.8,1,1.2,1.4,1.8,2,2.5,3]
    # solution_CM0={}
    # for cm in tqdm(CMs):
    #     folder = cm_folder+"/CM0="+str(cm)
    #     try:os.mkdir(folder)
    #     except FileExistsError:pass
    #     solution_CM0["CM0="+str(cm)]=fit2short_pulse(cell,short_pulse,folder=folder,CM=cm,RM=RM,RA=RA)
    # pickle.dump(solution_CM0 , open(cm_folder+"/CM0_fit_results.p", "wb"))

    # rm_folder = initial_folder+"/RM0"
    # try:os.mkdir(rm_folder)
    # except FileExistsError:pass
    # RMs=[5000,10000,15000,20000,25000,30000,50000,80000]
    # solution_RM0={}
    # for rm in RMs:
    #     folder = rm_folder+"/RM0="+str(rm)
    #     try:os.mkdir(folder)
    #     except FileExistsError:pass
    #     solution_RM0["RM0="+str(rm)]=fit2short_pulse(cell,short_pulse,folder=folder,CM=CM,RM=rm,RA=RA)
    # pickle.dump(solution_RM0 , open(rm_folder+"/RM0_fit_results.p", "wb"))





    # CM_RA_RM_folder = initial_folder + "/CM0_RM0_RA0"
    # try:os.mkdir(CM_RA_RM_folder)
    # except FileExistsError:pass
    # solution={}
    # for cm in CMs:
    #     for rm in RMs:
    #         for ra in RAs:
    #             folder = CM_RA_RM_folder + "/CM0="+str(cm)+" RM0="+str(rm)+" RA0=" + str(ra)
    #             try:os.mkdir(folder)
    #             except FileExistsError:pass
    #             solution["CM0="+str(cm)+" RM0="+str(rm)+" RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=cm, RM=rm, RA=ra)
    # pickle.dump(solution, open(CM_RA_RM_folder + "/CM_RM_RA_fit_results.p", "wb"))
