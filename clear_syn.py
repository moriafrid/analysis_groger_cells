import matplotlib.pyplot as plt
import numpy as np
from open_pickle import read_from_pickle
from add_figure import add_figure
import pickle
import sys
from extra_function import create_folder_dirr,create_folders_list
from syn2clear_data import Syn2Clear
from scipy.signal import find_peaks
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['png.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

if len(sys.argv) != 5:
    cell_name= '2017_03_04_A_6-7'
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir= "cells_outputs_data_short"
    save_dir = "cells_outputs_data_short"
else:
    cell_name = sys.argv[1]
    folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir = sys.argv[3] #cells_initial_information
    save_dir =sys.argv[4] #cells_outputs_data_short
folder_data=    folder_+data_dir+'/'+cell_name+'/data/electrophysio_records/syn/syn.p'
folder_save=folder_+save_dir+'/'+cell_name+'/data/electrophysio_records/clear_syn/' #(path)
create_folder_dirr(folder_save)
path1=folder_save+'syn2clear/'
create_folders_list([path1])

V_units,t_units=read_from_pickle(folder_data)
V=np.array(V_units)
syn_mean=np.mean(V,axis=0)
syn_time2clear1=np.argmax(syn_mean)-100
syn_time2clear2=np.argmax(syn_mean)+40


rest=[]

	# syn_time2clear1,syn_temp=find_places(syn_mean,prominence=2,two_peak=False)
	# index2del_syn = clear_phenomena_partial(syn, 'short_pulse','center_end', base ,prominanace=3,start=syn_time2clear1+300,end=len(syn[0]))
	# new_syn = np.delete(syn, list(index2del_syn), axis=0)

for i,v in enumerate(V):
    spike_place1,_=find_peaks(v[:syn_time2clear1],prominence=3)
    spike_place2,_=find_peaks(v[syn_time2clear2:],prominence=3)
    rest_temp=np.mean(v[syn_time2clear1 - 100:syn_time2clear1])
    rest.append(rest_temp)
    V[i] = v - rest_temp
    # new_syn.append(v[syn_time2clear1 - 500:syn_time2clear2 + 1000])
    # spike_peaks,_=find_peaks(v,prominence=3)
    if len(spike_place1)>0:
        for spike_peak in spike_place1:
            if spike_peak+400<syn_time2clear1 - 100:
                V[i][:spike_peak+400]=None
                print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
            else:
                V[i]=None
    if len(spike_place2)>0:
        for spike_peak in spike_place2:
            V[i][spike_peak-20:]=None
            print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
REST=np.mean(rest)
# t=t_units[syn_time2clear1 - 500:syn_time2clear2 + 1000]
t=t_units
for i,bolt_trace in enumerate(V):
    plt.close()
    add_figure('trace num '+str(i)+'\nmean on 100 points',str(syn_time2clear1 - 500)+':'+str(syn_time2clear2 + 1000),'mv')
    for v in V:
        plt.plot(v,'grey', alpha=0.1,lw=0.5)
    mean_syn=np.mean(V,axis=0)
    plt.plot(mean_syn,'black',lw=2)
    plt.plot(bolt_trace,'green',alpha=0.5,lw=1)
    print(i)
    plt.savefig(path1+'trace_num'+str(i))
    plt.close()

syns_records=Syn2Clear(cell_name)
not_sure=syns_records.not_sure
cut_on_1000=syns_records.cut_on_1000
rigth=syns_records.rigth
false=syns_records.false
path2=folder_save+'syn2clear_again'
create_folders_list([path2])
new_syn1=[]
for num in rigth:
    new_syn1.append(V[num])

for i,bolt_trace in enumerate(new_syn1):
    add_figure('trace num '+str(i)+'\nmean on 100 points',str(syn_time2clear1 - 500)+':'+str(syn_time2clear2 + 1000),'mv')
    for v in new_syn1:
        plt.plot(v,alpha=0.5)
    mean_syn=np.mean(new_syn1,axis=0)
    plt.plot(mean_syn,'black',linewidth=3)
    plt.plot(bolt_trace,'b',linewidth=2)
    print(i)
    plt.savefig(path2+'/trace_num'+str(i))
    plt.close()
    a=1
# remove=[18,23,27,34,43,47] #6? 14?
remove=syns_records.remove
#for time2syn+1000 and stable antil point 1200
# remove=[11,19,24,]

new_syn2=np.delete(new_syn1,remove,axis=0)+REST
fig=add_figure('correct synapse',V_units.units,t_units.units)
for v in new_syn2:
    plt.plot(t,v, alpha=0.1,lw=0.5)
plt.plot(t,np.mean(new_syn2,axis=0),'black',lw=2)
plt.savefig(folder_save+'/clear_syn')
pickle.dump(fig, open(folder_save+'/clear_syn_fig.p', 'wb'))

with open(folder_save + '/clear_syn.p', 'wb') as f:
    pickle.dump([new_syn2*V_units.units,t] , f)
fig1=add_figure('mean correct synepses',V_units.units,t_units.units)
plt.plot(t,np.mean(new_syn2,axis=0),'black',linewidth=2)
plt.savefig(folder_save+'/mean_clear_syn')
pickle.dump(fig1, open(folder_save+'/mean_clear_syn.p', 'wb'))

with open(folder_save + '/mean_syn.p', 'wb') as f:
    pickle.dump({'mean':[(np.mean(new_syn2, axis=0)) * V_units.units,t],'E_pas':REST}, f)

a=0
