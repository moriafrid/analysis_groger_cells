import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from tqdm import tqdm
from add_figure import add_figure
from glob import glob
import pickle
from calculate_F_factor import calculate_F_factor
from extra_function import load_ASC,load_hoc,SIGSEGV_signal_arises,create_folder_dirr
import sys

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
if len(sys.argv) != 7:
    cell_name= '2017_05_08_A_4-5'
    file_type='hoc'
    resize_diam_by=1.0
    shrinkage_factor=1.0
    RA_min=1
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
    cell_name = sys.argv[1]
    file_type=sys.argv[2] #hoc ar ASC
    resize_diam_by = float(sys.argv[3]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[4]) #how much srinkage the cell get between electrophysiology record and LM
    RA_min=int(sys.argv[5])
    folder_= sys.argv[6] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
print(sys.argv,len(sys.argv),flush=True)
# path_single_traces=glob('data/traces_img/2017_05_08_A_0006/*pA.p')
# path=path_single_traces[0]
# I=int(path[path.rfind('/')+1:path.rfind('pA')])

data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
path_short_pulse=glob(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p')[0]
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type)[0]
save_folder=folder_+save_dir+cell_name+'/fit_short_pulse_'+file_type+'/'
I=-50
# save_folder+=str(I)+'pA/'
save_folder+='dend*'+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))+'/basic_fit/Ra_min='+str(RA_min)
create_folder_dirr(save_folder)

do_calculate_F_factor=True

SPINE_START = 60
shrinkage_factor=1#1.0/0.7
resize_diam_by=1
spine_type="mouse_spine"

CM=1#2/2
RM=14000#5684*2#*2
RA=150

print('the injection current is',I,flush=True)

def change_model_pas(CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0):
    #input the neuron property    h.dt = 0.1
    h.distance(0,0.5, sec=soma) # it isn't good beacause it change the synapse distance to the soma
    #h.distance(0, sec=soma)
    for sec in cell.all_sec(): ##check if we need to insert Ra,cm,g_pas,e_pas to the dendrit or just to the soma
        sec.Ra = RA
        sec.cm = CM#*(1.0/0.7)
        sec.g_pas = (1.0 / RM)#*(1.0/0.7)
        sec.e_pas = E_PAS
    for sec in cell.dend:
        for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
            # how many segment have diffrent space larger then SPINE_START that decided
            if h.distance(seg) > SPINE_START:
                seg.cm *= F_factor
                seg.g_pas *= F_factor



## e_pas is the equilibrium potential of the passive current
def plot_res(RM, RA, CM, save_name= "fit",print_full_graph=False):

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
    add_figure(cell_name+" fit "+'RA_min='+str(RA_min)+"\nRM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),'mS','mV')
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
    error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2))/len(exp_V)) # mean square error

    print('error_total=',round(error_tot,3))
    print('error_decay=', round(error_2,3))
    print('error_mean_max_voltage=', round(error_3,3))
    print('error_from_rest=', round(error_1,3))
    if print_full_graph:
        add_figure(cell_name+": RM="+str(round(RM,1))+",RA="+str(round(RA,1))+",CM="+str(round(CM,2)),short_pulse[0].units,short_pulse[1].units)
        plt.plot(T, V, color = 'k',label='data') #plot short_pulse data
        plt.plot(T[start_fit:end_fit], V[start_fit:end_fit],color = 'green',label='decay_to_fit')
        # plt.plot(T[end_fit:end_fit+1500], V[end_fit:end_fit+1500],color = 'yellow',label='maxV_to_fit')
        plt.plot(T[max2fit-1200:max2fit], V[max2fit-1200:max2fit],color = 'yellow',label='maxV_to_fit')
        plt.plot(npTvec[:len(npVec)], npVec, color = 'r', linestyle ="--",label='NEURON_sim') #plot the recorded short_pulse
        plt.suptitle('ERROR: full graph='+str(round(error_tot,3))+' decay='+str(round(error_2,3))+' maxV='+str(round(error_3,3)))
        plt.legend()
        plt.savefig(save_folder+'/'+save_name+"_full_graph.pdf")
        plt.savefig(save_folder+'/'+save_name+"_full_graph.png")
        plt.close()
    return save_folder

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
    if (CM < 0.3 or RM < 2000 or RA <RA_min):
        return 1e6
    # print('RA:',RA, '   CM:',CM, '   RM:',RM)

    change_model_pas(CM=CM, RA=RA, RM = RM, E_PAS = E_PAS)
    Vvec = h.Vector()
    Vvec.record(soma(0.5)._ref_v)

    h.run()
    npVec = np.array(Vvec)

    exp_V = V#[int(180.0/h.dt):int(800.0/h.dt)]
    npVec = npVec#[int(180.0/h.dt):int(800.0/h.dt)]
    npVec = npVec[:len(exp_V)]
    error_tot = np.sqrt(np.sum(np.power(exp_V - npVec, 2)))#/len(exp_V)) # mean square error


    error_1 = np.sqrt(np.sum(np.power(np.mean(exp_V[:start_fit]) - np.mean(npVec[:start_fit]), 2)))  # error from mean rest
    error_2 = np.sqrt(np.sum(np.power(exp_V[start_fit:end_fit] - npVec[start_fit:end_fit], 2))) #/(end_fit-start_fit)  #  error for the decay
    error_3 = np.sqrt(np.sum(np.power(np.mean(exp_V[max2fit-1200:max2fit]) - np.mean(npVec[max2fit-1200:max2fit]), 2)))  # error for maximal voltage
    return error_2 + (end_fit-start_fit)*error_3


#########################################
# build the model
######################################################

# fname =glob(folder_+cell_name+ "/05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Bluecell_spinec91.ASC"
# cell=instantiate_swc('/ems/elsc-labs/segev-i/moria.fridman/project/data_analysis_git/data_analysis/try1.swc')
cell=None
if file_type=='ASC':
    cell =load_ASC(cell_file)
elif file_type=='hoc':
    cell =load_hoc(cell_file)

print (cell)
sp = h.PlotShape()
sp.show(0)  # show diameters
## delete all the axons
# for sec in cell.axon:
#    h.delete_section(sec=sec)

soma= cell.soma

#insert pas to all other section
for sec in tqdm(h.allsec()):
    sec.insert('pas') # insert passive property
    sec.nseg = int(sec.L/10)+1  #decide that the number of segment will be 21 with the same distances
for sec in cell.all_sec():
    sec.diam = sec.diam*resize_diam_by
    sec.L*=shrinkage_factor

if do_calculate_F_factor:
    F_factor=calculate_F_factor(cell,'mouse_spine')
else:
    F_factor = 1.9
print('F_factor=',F_factor)

short_pulse_dict = read_from_pickle(path_short_pulse)
short_pulse=short_pulse_dict['mean']
V = np.array(short_pulse[0])
short_pulse[1]=short_pulse[1].rescale('ms')
T = np.array(short_pulse[1])
T = T-T[0]
T=T
# clamp = h.IClamp(cell.dend[82](0.996)) # insert clamp(constant potentientiol) at the soma's center
clamp = h.IClamp(soma(0.5)) # insert clamp(constant potentientiol) at the soma's center
clamp.amp = I/1000#-0.05 ## supopsed to be 0.05nA
from extra_fit_func import find_injection
hz=0.1 #moria
E_PAS=short_pulse_dict['E_pas'] #np.mean(V[:start]) #or read it from the pickle
start,end=find_injection(V, E_PAS,duration=int(200/hz))
start_fit= start-100#2000   #moria
end_fit=end-1500#4900#3960  #moria
max2fit=end-10
clamp.delay = T[start]#296
clamp.dur =T[end]-T[start]# 200 #end-start

# if path in path_single_traces:
#     start_inj=10500
#     end_inj= 20400
#     hz=0.1
#     clamp.dur = (end_inj-start_inj)*hz
#     clamp.delay = start_inj*hz
# else:
#     clamp.dur = 200
#     clamp.delay = 296
######################################################
# load the data and see what we have
######################################################

# if path in path_single_traces:
#     E_PAS = np.mean(V[:9000])
#     end_fit=len(T)
# else:
#     E_PAS = np.mean(V[2945-500:2945])
#     # E_PAS = np.mean(V[:2000])

h.tstop = (T[-1]-T[0])
h.v_init=E_PAS
h.dt = hz#0.1
h.steps_per_ms = h.dt

CM_IX = 2
RM_IX=0
RA_IX = 1

RM_const = 60000.0
RA_const = 150
CM_const = 1.0

print("free params:")

h.attr_praxis(1e-9,1000,0)
opt_vals = h.Vector(3)#3
opt_vals.x[RM_IX] =RM
opt_vals.x[RA_IX] = RA
opt_vals.x[CM_IX] = CM
change_model_pas(CM=CM, RA=RA, RM=RM, E_PAS=E_PAS)

imp = h.Impedance(sec=soma)
imp.loc(soma(0.5))
imp.compute(0)
imp.input(0)

plot_res(CM=CM, RM=RM, RA=RA, save_name="before")
# plot_res(CM=CM, RM=RM, RA=RA, save_name="before")

#plot_res(CM=0.97, RM=11853.6, RA=99.6, save_name="test")

print('the initial impadence is', imp.input(0))

# allway run the fitting 3 time to avoid stack in local minima
for i in range(3):
    RMSD = h.fit_praxis(efun,opt_vals)   #@# take too much time if the fitting isn't found
    print('RMSD:',RMSD)
    RM = opt_vals.x[RM_IX]
    RA = opt_vals.x[RA_IX]
    CM = opt_vals.x[CM_IX]

    print("RMSD", RMSD,", RM",  RM, ", RA",  RA, ", CM",  CM)
    if i==2:
        plot_res(CM=CM, RM=RM, RA=RA, save_name="_fit_after_" + str(i + 1), print_full_graph=True)
    else:
        save_folder=plot_res(CM=CM, RM=RM, RA=RA, save_name="_fit_after_" + str(i + 1))

    # imp.compute(0)
    # print('the impadence is',imp.input(0))
pickle.dump({
        "RM": RM,
        "RA": RA,
        "CM": CM,
        "error" :RMSD
    }, open(save_folder+'/' + "final_result_dend*"+str(resize_diam_by)+".p", "wb"))
#

# from analysis_fit_after_run import analysis_fit
# anlysis_fit(save_folder)




