from open_pickle import read_from_pickle
import numpy as np
from neuron import h,gui
import  matplotlib.pyplot as plt
from calculate_F_factor import calculate_F_factor
from add_figure import add_figure
import pickle
import signal
from glob import glob
import sys
from extra_function import load_ASC,load_hoc,SIGSEGV_signal_arises,create_folder_dirr,create_folders_list
from extra_fit_func import find_injection
from analysis_fit_after_run import analysis_fit

do_calculate_F_factor=True
spine_type="mouse_spine"
print('argv len is ',len(sys.argv),' and contain ',sys.argv,flush=True)
if len(sys.argv) != 6:
    cell_name= '2017_05_08_A_4-5'
    file_type='hoc'
    resize_diam_by=1.0
    shrinkage_factor=1.0
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
   cell_name = sys.argv[1]
   file_type=sys.argv[2] #hoc ar ASC
   resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
   shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
   folder_= sys.argv[5] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
   if not folder_.endswith("/"):
       folder_ += "/"
# add2start=5

data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
print(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')
short_pulse_file=glob(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')[0]
print(folder_+data_dir+cell_name+'/*'+file_type)
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]

save_folder=folder_+save_dir+cell_name+'/fit_short_pulse_'+file_type+'/'
# initial_folder+=spine_type
save_folder+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
save_folder+="/different_initial_conditions/"
create_folder_dirr(save_folder)
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
def plot_res(RM, RA, CM, save_name= "fit",save_folder='',print_full_graph=False):
    create_folder_dirr(save_folder)
    # creat a clamp and record it for the chosen parameter
    ## save_name need to incloud the folder path
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS = E_PAS)
    Vvec = h.Vector() #cerat vector to record on it
    Tvec = h.Vector() #cerat vector to record on it
    Vvec.record(soma(0.5)._ref_v) #where to recprd
    Tvec.record(h._ref_t) #when it record
    h.cvode.store_events(Vvec)

    h.run()
    npTvec = np.array(Tvec)
    npVec = np.array(Vvec)
    add_figure(cell_name+" fit "+save_folder.split('/')[-3]+"\nRM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),'ms','mV')
    plt.plot(npTvec[start_fit:end_fit], npVec[start_fit:end_fit], color = 'r', linestyle ="--") #plot the recorded short_pulse
    plt.plot(T[start_fit:end_fit], V[start_fit:end_fit],color = 'green')
    plt.plot(npTvec[start_fit:end_fit], npVec[start_fit:end_fit], color = 'r', linestyle ="--") #plot the recorded short_pulse

    plt.legend(['NEURON_sim','decay_to_fitting'])
    plt.savefig(save_folder+'/'+save_name+"_decay.png")
    plt.close()
    exp_V = V#[int(180.0 / h.dt):int(800.0 / h.dt)]
    npVec = npVec#[int(180.0 / h.dt):int(800.0 / h.dt)]
    npVec = npVec[:len(exp_V)]
    error_1 = np.sqrt(np.sum(np.power(np.mean(exp_V[:start]) - np.mean(npVec[:start]), 2)))  # error from mean rest
    error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))/(end_fit-start_fit))  #  error for the decay
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit-1200:max2fit]) - np.mean(npVec[max2fit-1200:max2fit]), 2)))  # error for maximal voltage
    # error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[end_fit:end_fit+1500]) - np.mean(npVec[end_fit:end_fit+1500]), 2)))  # error for maximal voltage
    error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2))/len(exp_V)) # mean square error

    print('error_total=',round(error_tot,3))
    print('error_decay=', round(error_2,3))
    print('error_mean_max_voltage=', round(error_3,3))
    print('error_from_rest=', round(error_1,3))
    if print_full_graph:
        add_figure(cell_name+": RM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),'ms','mV')
        plt.plot(T, V, color = 'k',label='data') #plot short_pulse data
        plt.plot(T[start_fit:end_fit], V[start_fit:end_fit],color = 'green',label='decay_to_fit')
        # plt.plot(T[end_fit:end_fit+1500], V[end_fit:end_fit+1500],color = 'yellow',label='maxV_to_fit')
        plt.plot(T[max2fit-1200:max2fit], V[max2fit-1200:max2fit],color = 'yellow',label='maxV_to_fit')

        plt.plot(npTvec[:len(npVec)], npVec, color = 'r', linestyle ="--",label='NEURON_sim') #plot the recorded short_pulse
        plt.suptitle('ERROR: full graph='+str(round(error_tot,3))+' decay='+str(round(error_2,3))+' maxV='+str(round(error_3,3)))
        plt.legend()
        plt.savefig(save_folder+'/'+save_name+"_full_graph.pdf")
        plt.savefig(save_folder+'/'+save_name+"_full_graph.png")
        plt.show()
        plt.close()
    return error_2 ,error_2 + error_3

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
   if (CM < 0.3 or RM < 2000 or RA <5):
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
   error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit-1200:max2fit]) - np.mean(npVec[max2fit-1200:max2fit]), 2)))  # error for maximal voltage
   return error_2 + (end_fit-start_fit)*error_3


def fit2short_pulse(cell,short_pulse,folder="",CM=1,RM=10000,RA=100):
    opt_vals = h.Vector(3)
    opt_vals.x[RM_IX] =RM
    opt_vals.x[RA_IX] = RA
    opt_vals.x[CM_IX] = CM
    change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS=E_PAS)
    plot_res(CM=CM, RM=RM, RA=RA, save_name="before",save_folder=folder)
    for i in range(3):
        RMSD = h.fit_praxis(efun,opt_vals)   #@# take too much time if the fitting isn't found
        RM = opt_vals.x[RM_IX]
        RA = opt_vals.x[RA_IX]
        CM = opt_vals.x[CM_IX]

        print("RMSD", RMSD,", RM",  RM, ", RA",  RA, ", CM",  CM)
    if i==2:
        error_decay,precent_error=plot_res(CM=CM, RM=RM, RA=RA, save_name="_fit_after_" + str(i + 1), print_full_graph=True,save_folder=folder)
    else:
        plot_res(CM=CM, RM=RM, RA=RA, save_name="_fit_after_" + str(i + 1),save_folder=folder)

    pickle.dump({
        "RM": RM,
        "RA": RA,
        "CM": CM,
        "error":{'decay':error_decay,'decay&max':precent_error,'RMSD':RMSD}
    }, open(folder+"/fit_result.p", "wb"))
    return {"CM": CM,"RM": RM,"RA": RA,"error":{'decay':error_decay,'decay&max':precent_error,'RMSD':RMSD} }
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

    # ## delete all the axons
    # for sec in cell.axon:
    #     h.delete_section(sec=sec)
    for sec in cell.all_sec():
        sec.insert('pas') # insert passive property
        sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
    for sec in cell.all_sec():
        sec.diam = sec.diam*resize_diam_by
        sec.L*=shrinkage_factor
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
    E_PAS=short_pulse['E_pas']#np.mean(V[:start]) #or read it from the pickle
    SPINE_START = 60

    start,end=find_injection(V,E_PAS,duration=int(200/hz))
    start_fit= start-100#2000   #moria
    end_fit=end-1200#4900#3960  #moria
    max2fit=end-10
    # start+=add2start
    soma=cell.soma
    clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
    clamp.amp = I/1000 #pA
    clamp.delay = T[start]#296
    clamp.dur =T[end]-T[start]# 200 #end-start
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
    # ra_folder=save_folder +'/RA0_5:50:1+RA>1'
    # ra_folder = save_folder + "/RA0_50:100:0.5"
    # create_folders_list([ra_folder])
    # RAs = np.arange(5,50,1.)
    # solution_RA0={}
    # for ra in RAs:
    #     folder = ra_folder + "/RA0=" + str(ra)
    #     print(folder,flush=True)
    #     create_folders_list([folder])
    #     solution_RA0["RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=CM, RM=RM, RA=ra)
    #     pickle.dump(solution_RA0, open(ra_folder + "/RA0_fit_results.p", "wb"))
    # analysis_fit(ra_folder)

    ra_folder = save_folder + "/RA0_50:100:0.5"
    create_folders_list([ra_folder])
    RAs = list(np.arange(50,100,0.5))+list(np.arange(1,50,1.))
    solution_RA0={}
    for ra in RAs:
        folder = ra_folder + "/RA0=" + str(ra)
        print(folder,flush=True)

        create_folders_list([folder])
        solution_RA0["RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=CM, RM=RM, RA=ra)
        pickle.dump(solution_RA0, open(ra_folder + "/RA0_fit_results.p", "wb"))
    analysis_fit(ra_folder)

    ra_folder = save_folder + "/RA0_100:300:2"
    create_folders_list([ra_folder])
    RAs = np.arange(100,300,2.)
    solution_RA0={}
    for ra in RAs:
        folder = ra_folder + "/RA0=" + str(ra)
        print(folder,flush=True)
        create_folders_list([folder])
        solution_RA0["RA0=" + str(ra)] = fit2short_pulse(cell, short_pulse, folder=folder, CM=CM, RM=RM, RA=ra)
        pickle.dump(solution_RA0, open(ra_folder + "/RA0_fit_results.p", "wb"))
    analysis_fit(ra_folder)


    #analysis:
    # for dirr in glob(save_folder+'/RA0*'):
    #     if '+' in dirr: continue
    #     analysis_fit(dirr)

    datas=glob(save_folder+'/RA0*/RA0_fit_results.p')
    for data in datas:
        if '+' in data: datas.remove(data)
    print('datas', datas)
    data1,data2=datas

    #####change the locations
    dict1=read_from_pickle(data1)
    dict2=read_from_pickle(data2)

    if float(next(iter(dict1.keys())).split('=')[-1])<float(next(iter(dict2.keys())).split('=')[-1]):
        dict = dict1.copy()  # Copy the dict1 into the dict3 using copy() method
        for key, value in dict2.items():  # use for loop to iterate dict2 into the dict3 dictionary
            dict[key] = value
    else:
        dict = dict2.copy()  # Copy the dict1 into the dict3 using copy() method
        for key, value in dict1.items():  # use for loop to iterate dict2 into the dict3 dictionary
            dict[key] = value

    save_folder2=save_folder+'/'+data1.split('/')[-2]+'_'+data2.split('/')[-2]
    create_folders_list([save_folder2])
    RA0=[float(key.split('=')[-1]) for key in dict.keys()]
    value=[dict[key] for key in dict.keys()]
    RAs,RMs,CMs,errors=[],[],[],[]
    for key in dict.keys():
        RAs.append(dict[key]['RA'])
        RMs.append(dict[key]['RM'])
        CMs.append(dict[key]['CM'])
        errors.append(dict[key]['error']['decay&max'])
    add_figure('diffrent RA0 against error','RA0','errors')
    plt.plot(RA0,errors)
    minimums_arg=np.argsort(errors)
    # mini = np.argmin(errors)
    dict_minimums={}
    # print(loc)
    for mini in minimums_arg[:10]:
        plt.plot(RA0[mini], errors[mini], '*',label='RA0=' + str(RA0[mini]) + ' RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                     round(CMs[mini], 2)) + ' error=' + str(round(errors[mini], 3)))
        dict_minimums['RA0=' + str(RA0[mini])]=dict.get('RA0=' + str(RA0[mini]), dict.get('RA0=' + str(int(RA0[mini])), None))
        if dict_minimums['RA0=' + str(RA0[mini])] is None:
            raise TypeError("dict_minimums get None")
    pickle.dump(dict_minimums, open(save_folder2 + "/RA0_10_minimums.p", "wb"))
    plt.legend(loc='upper left')
    plt.savefig(save_folder2+'/diffrent RA0 against error.png')

    add_figure('diffrent RA against error','RA','errors')
    plt.plot(RAs,errors,'.')
    for mini in minimums_arg[:10]:
        plt.plot(RAs[mini], errors[mini], '*',label= 'RM=' + str(round(RMs[mini], 2)) + ' RA=' + str(round(RAs[mini], 2)) + ' CM=' + str(
                     round(CMs[mini], 2)) + ' error=' + str(round(errors[mini], 3)) )
    plt.legend(loc='upper left')
    plt.savefig(save_folder2+'/diffrent RA against error.png')

    add_figure('diffrent RA0 against CM','RA0','CM')
    plt.plot(RA0,CMs)
    plt.savefig(save_folder2+'/diffrent RA0 against CM.png')
    add_figure('diffrent RA0 against ֵֻֻRA after fit','RA0','RA')
    plt.plot(RA0,RAs)
    plt.savefig(save_folder2+'/diffrent RA0 against RA after fit.png')
    add_figure('diffrent RA0 against RM','RA0','RM')
    plt.plot(RA0,RMs)
    plt.savefig(save_folder2+'/diffrent RA0 against RM.png')

 #########
    # cm_folder = save_folder+"/CM0"
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

    # rm_folder = save_folder+"/RM0"
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
    print('fit_influance_by_initial_condition.py is complite to run')
