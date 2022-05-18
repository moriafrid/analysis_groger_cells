from glob import glob
import pickle
import matplotlib.pyplot as plt
import numpy as np
from read_spine_properties import get_parameter
from IV_curve import I_V_curve, sepereat_by_current, find_maxi
from check_dynamics import check_dynamics
import quantities as pq
from open_pickle import read_from_pickle
from extra_function import create_folder_dirr

inputs_folder='cells_initial_information/'

abf_files=glob(inputs_folder+'*/*IV.abf')

for f in abf_files[:]:
	if '(0)' in f: continue
	print(f, flush=True)
	cell_name=f.split('/')[1]
	print(cell_name)
	save_folder='cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/'+f.split('/')[-1][:-4]
	base_external_folder='cells_outputs_data_short/'+cell_name + '/data/'

	t1,T=read_from_pickle(save_folder + '/first_channel.p')
	t2,T=read_from_pickle(save_folder + '/second_channel.p')

	from open_pickle import read_from_pickle
	fig, axs = plt.subplots(2)
	fig.suptitle('decide on the right channels')
	axs[0].plot(np.array(T).flatten(), np.array(t1).flatten())
	axs[0].set_title('channels1')
	if len(t2)>0:
		axs[1].plot(np.array(T).flatten(), np.array(t2).flatten())
		axs[1].set_title('channels2')
		plt.savefig(save_folder + '/IV_curve_channel1&channel2.pdf')
	t1=eval('t'+str(int(get_parameter(cell_name,'channel2take_IV')[0])))
	# plt.show()
	save_folder_IV_curve = save_folder  # moria
	I = [-200, -160, -120, -80, -40, -0, 40, 80, 120, 160]
	# print(f,'correct IV_curve')
	maxi = sepereat_by_current(np.array(t1) * t1.units, T, I, save_folder_IV_curve)
	REST=read_from_pickle('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')['E_pas']
	short_pulse,T_short_pulse=read_from_pickle('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p')
	maxi = np.append(maxi, find_maxi(np.array(short_pulse), save_folder_IV_curve)[0])
	I.append(-50)
	with open(save_folder_IV_curve + 'max_vol_curr_inj.p', 'wb') as fr:
		pickle.dump([maxi * t1.units, I * pq.pA], fr)
	I_V_curve(maxi, I * pq.pA, save_folder_IV_curve)
	check_dynamics(short_pulse, T_short_pulse, create_folder_dirr(base_external_folder+'check_dynamic/'))
