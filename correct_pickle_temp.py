import numpy as np
from matplotlib import pyplot as plt

from open_pickle import read_from_pickle
from glob import glob
import pickle
import os
from add_figure import add_figure
new=[]
unmV=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[1].units
uns=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[0].units

####i need correct the mean_short_pulse_with_paramaters.p
cell_name='2016_04_16_A'
base_dir='cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse/'
path1=glob(base_dir+'/mean_short_pulse_with_parameters_temp.p')[0]
path2=glob(base_dir+'/clear_short_pulse_temp.p')[0]
data=read_from_pickle(path2)
after_del=np.delete(data[0],[22],axis=0)
filterd_traces_first=[v-np.mean(v[1390:1998])for v in after_del]

# os.rename(path1,path1[:-2]+'_temp.p')
path3=glob('cells_outputs_data_old_runs/*/data/electrophysio_records/short_pulse/short_pulse.p')
with open(base_dir+"clear_short_pulse.p", 'wb') as handle:
    pickle.dump([filterd_traces_first*unmV,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(base_dir+"mean_short_pulse.p", 'wb') as handle:
    pickle.dump([np.mean(filterd_traces_first,axis=0)*unmV,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)

fig=add_figure('clear_short_pulse','ms','mV')
for v in filterd_traces_first:
    plt.plot(data[1],v,'black',alpha=0.1,lw=0.2)

plt.plot(data[1],np.mean(filterd_traces_first,axis=0),'black',lw=2,label='mean_short_pulse')
plt.savefig(base_dir+"clear_short_pulse_after_peeling.png")
plt.savefig(base_dir+"clear_short_pulse_after_peeling.pdf")
pickle.dump(fig, open(base_dir+'clear_short_pulse__after_peeling.p', 'wb'))
plt.close()
plt.figure()
plt.title(cell_name+' have '+str(len(filterd_traces_first))+'traces')

temp=read_from_pickle(path1)
data1={}
meany=[np.mean(filterd_traces_first,axis=0)+temp['E_pas']]
data1['mean']=[meany[0]*unmV,data[1]]
data1['E_pas']=temp['E_pas']
data1['points2calsulate_E_pas']=temp['points2calsulate_E_pas']

with open(base_dir+'mean_short_pulse_with_parameters.p', 'wb') as handle:
    pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)
# for path in path2:
#     cell_name=path.split('/')[1]
#     if cell_name!='2016_05_12_A':continue
#     path3=glob('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn0.p')[0]
#     time=read_from_pickle(path3)[1]
#     data=read_from_pickle(path3)
#     data1=[]
#     data1.append(data[0]*unmV)
#     data1.append(data[1])
#     # data1={}
#     # data1['mean']=[data['mean'][0][:len(time)]*unmV,time]
#     # data1['E_pas']=data['E_pas']
#     # data1['points2calsulate_E_pas']=data['points2calsulate_E_pas']
#     # print(len(data1['mean'][0]),len(data1['mean'][1]))
#     print(data1)
#     with open('cells_initial_information/'+cell_name+'/clear_syn0.p', 'wb') as handle:
#         pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #
    # # print(path)
    # dicty=read_from_pickle(path)
    # # new_mean=dicty['mean'][0]+dicty['E_pas']
    # # new_dicty=dicty.copy()
    # # new_dicty['mean'][0]=new_mean
    # # print(new_dicty)
    # print(dicty['mean'][0])
    # with open(path[:path.find('_temp.p')]+".p", 'wb') as handle:
    #     pickle.dump(dicty, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #
    #
    # if 'mean' in path.split('/')[-1]:
    #     'cells_outputs_data_short/2017_02_20_B/data/electrophysio_records/short_pulse/mean0_short_pulse_with_parameters.p'
    #     new_dict={}
    #     # print(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')
    #     temp_dict=read_from_pickle(glob(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')[0])
    #     new_dict['mean']=new
    #     new_dict['E_pas']=temp_dict['E_pas']
    #     new_dict['points2calsulate_E_pas']=temp_dict['points2calsulate_E_pas']
    #     print(new_dict)
    #     print(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p')
    #     with open(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p', 'wb') as handle:
    #         pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
