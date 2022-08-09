from neuron import h
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from fit_best_with_const_param import change_model_pas
from extra_fit_func import short_pulse_edges
from parameters_short_pulse import decay_length
from extra_function import load_ASC,load_hoc,load_swc,SIGSEGV_signal_arises,create_folder_dirr
from calculate_F_factor import calculate_F_factor
from open_pickle import read_from_pickle
import pickle
import sys
# dirr,str(RM), str(RA), str(CM),str(resize_diam_by),str(shrinkage_by),str(passive_val_name)
if len(sys.argv) != 9:
   cell_name = "2017_03_04_A_6-7"
   RM=15450.0
   RA=78.0
   CM=1.19
   resize_diam_by = 1.0 #how much the cell sweel during the electrophisiology records
   shrinkage_by =1.0 #how much srinkage the cell get between electrophysiology record and LM
   passive_val_name='RA_best_fit_test'
   before_after='_after_shrink'
   print("plot_fit_short_pulse don't run with sys.srgv")
else:
   cell_name = sys.argv[1]
   RM=float(sys.argv[2])
   RA=float(sys.argv[3])
   CM=float(sys.argv[4])
   resize_diam_by = float(sys.argv[5]) #how much the cell sweel during the electrophisiology records
   shrinkage_by =float(sys.argv[6]) #how much srinkage the cell get between electrophysiology record and LM
   passive_val_name=sys.argv[7]
   before_after=sys.argv[8]
   print(sys.argv, 'sys.argv correct and run')

def change_model_pas(cell,CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0,F_factor=1.9,SPINE_START=20):
   h.dt = 0.1
   h.distance(0,0.5, sec=cell.soma)
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


def plot_res_short_pusle(dirr ,RM, RA, CM,resize_diam_by=1.0,shrinkage_factor=1.0,passive_val_name=''):
    data_dir="cells_initial_information/"
    cell_name=dirr.split('/')[1]
    file_type=dirr.split('/')[4][:dirr.split('/')[4].rfind('_SPINE_START')]
    # before_after=dirr.split('/')[3].replace('fit_short_pulse','')
    # cell_file='cells_initial_information/2017_03_04_A_6-7/morphology_z_correct_after_shrink.swc'
    cell_file=glob(data_dir+cell_name+'/*'+file_type[:-4]+before_after+file_type[-4:])[0]
    # if cell_name =='2017_07_06_C_4-3':
    #     cell_file=glob(data_dir+cell_name+'/*'+file_type[:-4]+'_before_shrink'+file_type[-4:])[0]

    path_short_pulse=glob(data_dir+cell_name+'/mean_short_pulse_with_parameters.p')[0]

    cell=None
    if 'ASC' in file_type:
       cell =load_ASC(cell_file)
    elif 'hoc' in file_type:
       cell =load_hoc(cell_file)
    elif 'swc' in file_type:
        cell =load_swc(cell_file)

    for sec in cell.all_sec():
        sec.insert('pas') # insert passive property
        sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
    for sec in cell.all_sec():
        sec.diam = sec.diam*resize_diam_by
        sec.L*=shrinkage_factor
    hz= 0.1

    F_factor=calculate_F_factor(cell)

    soma=cell.soma
    short_pulse=read_from_pickle(path_short_pulse)
    E_PAS = short_pulse['E_pas']
    start,end,length=short_pulse_edges(cell_name)
    decay_start= start
    decay_end=start+decay_length
    max2fit_start=start+decay_length
    V = np.array(short_pulse['mean'][0])
    T = np.array(short_pulse['mean'][1].rescale('ms'))
    T = T-T[0]
    if cell_name=='2017_04_03_B':
        max2fit_end=end-500
    else:
        max2fit_end=end-10
    I=-50
    clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
    clamp.amp = I/1000 #pA
    clamp.delay = T[start]#296
    clamp.dur =T[end]-T[start]# 200 #end-start
    change_model_pas(cell,CM=CM, RA =RA, RM = RM, E_PAS = E_PAS,F_factor=F_factor,SPINE_START=20)

    Vvec = h.Vector()
    Tvec = h.Vector()
    Vvec.record(soma(0.5)._ref_v)
    Tvec.record(h._ref_t)
    h.cvode.store_events(Vvec)
    h.dt=hz
    h.tstop = (T[-1]-T[0])
    h.v_init=E_PAS
    h.steps_per_ms = h.dt
    h.run()
    npTvec = np.array(Tvec)
    npVec = np.array(Vvec)
    exp_V = V
    npVec = npVec
    npVec = npVec[:len(exp_V)]
    error_2 = np.sqrt(np.sum(np.power(exp_V[decay_start:decay_end] - npVec[decay_start:decay_end], 2))/(decay_end-decay_start))  #  error for the decay
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit_start:max2fit_end]) - np.mean(npVec[max2fit_start:max2fit_end]), 2)))  # error for maximal voltage
    # error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2))/len(exp_V)) # mean square error
    plt.legend(loc='best')
    dict_result={'parameter':{'RA':RA,'CM':CM,'RM':RM,'E_PAS':E_PAS},'passive_val_name':passive_val_name,'experiment':{'T':T,'V':V},'model':{'T':npTvec,'V':npVec,'error':error_2+error_3},'fit_decay':{'T':T[decay_start:decay_end],'V':V[decay_start:decay_end],'error':error_2},'fit_Rin':{'T':T[max2fit_start:max2fit_end], 'V':V[max2fit_start:max2fit_end],'error':error_3}}
    save_dirr=dirr+passive_val_name+'_results.p'
    plt.plot(T, V, color = 'black',alpha=0.3,label='data',lw=2)
    plt.plot(T[decay_start:decay_end], V[decay_start:decay_end], color = 'b',alpha=0.3,label='fit decay')
    plt.plot(T[max2fit_start:max2fit_end], V[max2fit_start:max2fit_end],color = 'yellow',label='fit maxV')
    if len(npTvec)>len(npVec):
        npTvec=npTvec[:len(npVec)]
    plt.plot(npTvec, npVec, color = 'r', linestyle ="--",alpha=0.3,label='NEURON simulation')
    plt.title(cell_name)
    plt.show()
    with open(save_dirr, 'wb') as fr:
    	pickle.dump(dict_result, fr)
    return save_dirr

if __name__=='__main__':
    data_file='cells_outputs_data_short/'+cell_name+'/'
    dirr=glob(data_file+'/fit_short_pulse'+before_after+'/z_correct.swc_SPINE_START=20/dend*'+str(resize_diam_by)+'&F_shrinkage='+str(shrinkage_by)+'/const_param/RA/')[0]
    plot_res_short_pusle(dirr ,float(RM), float(RA), float(CM),resize_diam_by=resize_diam_by,shrinkage_factor=shrinkage_by,passive_val_name=passive_val_name)

    cell=None
