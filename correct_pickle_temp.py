from open_pickle import read_from_pickle
from glob import glob
import pickle
new=[]
for path in glob('cells_outputs_data_short/*/data/electrophysio_records/short_pulse/*_temp.p'):
    # print(path)
    new=[]
    temp=read_from_pickle(path)
    new.append(temp[1])
    new.append(temp[0])
    with open(path[:path.find('_temp.p')]+".p", 'wb') as handle:
        pickle.dump(new, handle, protocol=pickle.HIGHEST_PROTOCOL)
    name=path.split('/')[-1]
    # print('cells_initial_information/'+path.split('/')[1]+'/'+name[:name.find('_temp.p')])
    with open('cells_initial_information/'+path.split('/')[1]+'/'+name[:name.find('_temp.p')]+".p", 'wb') as handle:
        pickle.dump(new, handle, protocol=pickle.HIGHEST_PROTOCOL)


    if 'mean' in path.split('/')[-1]:
        'cells_outputs_data_short/2017_02_20_B/data/electrophysio_records/short_pulse/mean0_short_pulse_with_parameters.p'
        new_dict={}
        # print(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')
        temp_dict=read_from_pickle(glob(path[:path.find('mean')]+'mean0_short_pulse_with_parameters.p')[0])
        new_dict['mean']=new
        new_dict['E_pas']=temp_dict['E_pas']
        new_dict['points2calsulate_E_pas']=temp_dict['points2calsulate_E_pas']
        print(new_dict)
        print(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p')
        with open(path[:path.find('mean')]+'mean_short_pulse_with_parameters.p', 'wb') as handle:
            pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
