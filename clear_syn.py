import matplotlib.pyplot as plt
import numpy as np
from open_pickle import read_from_pickle
import os
from add_figure import add_figure
import pickle
import sys
from extra_function import create_folder_dirr
from spinse_class import Syn2Clear

if len(sys.argv) != 5:
    cell_name= '2017_05_08_A_4-5'
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir= "cells_outputs_data"
    save_dir ="cells_outputs_data"
else:
    cell_name = sys.argv[1]
    folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
    data_dir = sys.argv[3] #cells_initial_information
    save_dir =sys.argv[4] #cells_outputs_data
folder_save=folder_+save_dir+'/'+cell_name+'/data/clear_syn/' #(path)
create_folder_dirr(folder_save)
path1=folder_save+'syn2clear'
try:os.mkdir(path1)
except FileExistsError:pass
V_units,t_units=read_from_pickle(folder_+data_dir+'/'+cell_name+'/data/electrophysio_records/syn/syn.p')
V=np.array(V_units)
temp_syn=np.mean(V,axis=0)
syn_time2clear1=np.argmax(temp_syn)-100
syn_time2clear2=np.argmax(temp_syn)+200
rest,new_syn=[],[]
for v in V:
    rest.append(np.mean(v[syn_time2clear1 - 100:syn_time2clear1]))
    v = v - np.mean(v[syn_time2clear1 - 100:syn_time2clear1])
    new_syn.append(v[syn_time2clear1 - 500:syn_time2clear2 + 1000])
REST=np.mean(rest)
t=t_units[syn_time2clear1 - 500:syn_time2clear2 + 1000]
for i,bolt_trace in enumerate(new_syn):
    add_figure('trace num '+str(i)+'\nmean on 100 points',str(syn_time2clear1 - 500)+':'+str(syn_time2clear2 + 1000),'mv')
    for v in new_syn:
        plt.plot(v,'grey', alpha=0.05,lw=0.5)
    mean_syn=np.mean(new_syn,axis=0)
    plt.plot(mean_syn,'black',lw=2)
    plt.plot(bolt_trace,'green',alpha=0.5,lw=1)
    print(i)
    plt.savefig(path1+'/trace_num'+str(i))
    plt.close()

syns_records=Syn2Clear(cell_name)
not_sure=syns_records.not_sure
cut_on_1000=syns_records.cut_on_1000
rigth=syns_records.rigth
false=syns_records.false
path2=folder_save+'syn2clear_again'

try:os.mkdir(path2)
except FileExistsError:pass
new_syn1=[]
for num in rigth:
    new_syn1.append(new_syn[num])

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
add_figure('correct synapse',V_units.units,t_units.units)
for v in new_syn2:
    plt.plot(t,v, alpha=0.1,lw=0.5)
plt.plot(t,np.mean(new_syn2,axis=0),'black',lw=2)
plt.savefig(folder_save+'/clear_syn')
with open(folder_save + '/clear_syn.p', 'wb') as f:
    pickle.dump([new_syn2*V_units.units,t] , f)
add_figure('mean correct synepses',V_units.units,t_units.units)
plt.plot(t,np.mean(new_syn2,axis=0),'black',linewidth=2)
plt.savefig(folder_save+'/mean_clear_syn')
with open(folder_save + '/mean_syn.p', 'wb') as f:
    pickle.dump({'mean':[(np.mean(new_syn2, axis=0)) * V_units.units,t],'E_pas':REST}, f)

a=0
