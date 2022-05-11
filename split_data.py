from neo import io
from glob import glob
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import pickle
from open_one_data import phenomena
import os
from add_figure import add_figure
import quantities as pq
from IV_curve import I_V_curve, sepereat_by_current, find_maxi
from check_dynamics import check_dynamics
from extra_function import create_folder_dirr, create_folders_list
from read_spine_properties import get_parameter
from open_pickle import read_from_pickle

from spine_classes import channel2take

def split2phenomena(cell_name,inputs_folder, outputs_folder):
	"""
	important_outputs_folder: <repository>/cells_important_outputs_data/<cell_name>
	all_outputs_folder: <repository>/cells_outputs_data_short/<cell_name>
	"""
	# base_folder = os.path.join(outputs_folder,'/data/',  'electrophysio_records/')
	# base_external_folder = os.path.join(outputs_folder, '/data/')
	# save_external_folder = base_external_folder + '/'
	base_folder = ''.join([outputs_folder,'/data/',  'electrophysio_records/'])
	base_external_folder = ''.join([outputs_folder, '/data/'])
	folder_names = ['V1', 'short_pulse', 'syn', 'spike', 'noise1', 'noise2','noise3']
	create_folder_dirr(base_external_folder)
	create_folders_list([os.path.join(base_folder, n) for n in folder_names])

	abf_files = glob(os.path.join(inputs_folder, '*.abf'))
	#transfer IV file to teh end
	place_IV=np.where(['IV' in a for a in abf_files])[0][0]
	IV_file=abf_files[place_IV]
	abf_files.pop(place_IV)
	abf_files.append(IV_file)
	try:
		place_unaligment=np.where(['stable_conc.abf' in a for a in abf_files])[0][0]
		unaligment_file=abf_files[place_unaligment]
		abf_files.pop(place_unaligment)
		abf_files.append(unaligment_file)
	except:
		print('no stable_conc.abf in this cell')


	print("Found input files {0} in {1}".format(abf_files, inputs_folder))

	for f in abf_files[:]:  # take the abf file (from 3)
		# if 'IV' not in f:continue
		print(f, flush=True)
		save_folder = os.path.join(base_folder, f[f.rfind('/') + 1:-4]) + '/'
		create_folders_list([save_folder])

		r = io.AxonIO(f)
		bl = r.read_block(lazy=False)
		hz = [np.array(segment.analogsignals[0].sampling_rate) for segment in bl.segments]
		t, T, t1, t2 = [], [], [], []
		for segment in tqdm(bl.segments):
			t_i = segment.analogsignals[0]
			channel1 = [v[0] for v in np.array(t_i)]
			t.append(t_i)
			t1.append(channel1)
			T_i = np.linspace(segment.analogsignals[0].t_start, segment.analogsignals[0].t_stop, int(len(t_i)))
			T.append(T_i)
			try:channel2 = [v[1] for v in np.array(t_i)]
			except:continue
			t2.append(channel2)


		with open(save_folder + '/full_channel.p', 'wb') as fr:
			pickle.dump([t, T], fr)
		with open(save_folder + '/first_channel.p', 'wb') as fr:
			pickle.dump([np.array(t1) * t_i.units, T], fr)
		fig1=add_figure(f[f.rfind('/') + 1:-4] + '\n first_channel', T[0].units, t[0].units)
		plt.plot(np.array(T).flatten(), np.array(t1).flatten())
		plt.savefig(save_folder + '/first_channel.png')
		plt.savefig(save_folder + '/first_channel.pdf')
		pickle.dump(fig1, open(save_folder + '/first_channel_fig.p', 'wb'))

		with open(save_folder + '/second_channel.p', 'wb') as fr:
			pickle.dump([np.array(t2) * t_i.units, T], fr)
		plt.close()
		if len(t2)>0:
			fig2=add_figure(f[f.rfind('/') + 1:-4] + '\n second_channel', T[0].units, t[0].units)
			plt.plot(np.array(T).flatten(), np.array(t2).flatten())
			plt.savefig(save_folder + '/second_channel.png')
			plt.savefig(save_folder + '/second_channel.pdf')
			pickle.dump(fig2, open(save_folder+'/second_channel_fig.p', 'wb'))

		# split to syn, short_pulse, spike ,noise
		if f.endswith(".abf") and "stable_conc_aligned" and "average" in f:  # pattern: *stable_conc_aligned_average*.abf
			pass
		elif f.endswith(".abf") and "stable_conc_aligned" in f:  # pattern: *stable_conc_aligned*.abf
			print(f, 'correct one_data')
			presnaptic_channel=eval('t'+str(int(get_parameter(cell_name,'channel2take_presynaptic')[0])))
			postsynaptic_channel=eval('t'+str(int(get_parameter(cell_name,'channel2take_postsynaptic')[0])))
			#here nedd to be choose what channel is the presynaptic channel and what is the post_synaptic channels
			REST, short_pulse, T_short_pulse = phenomena(np.array(presnaptic_channel) * t_i.units,postsynaptic_channel, T, base_folder, x_units=T[0].units, Y_units=t_i.units)
		elif f.endswith("stable_conc.abf"):
			print(f, 'correct one_data')
			base_folder_unaligment = ''.join([outputs_folder,'/data/',  'electrophysio_records/',f.split('/')[-1],'/'])
			folder_names = ['V1', 'short_pulse', 'syn', 'spike', 'noise1', 'noise2','noise3']
			create_folder_dirr(base_folder_unaligment)
			create_folders_list([os.path.join(base_folder_unaligment, n) for n in folder_names])
			presnaptic_channel=eval('t'+str(int(get_parameter(cell_name,'channel2take_presynaptic')[0])))
			postsynaptic_channel=eval('t'+str(int(get_parameter(cell_name,'channel2take_postsynaptic')[0])))
			#here nedd to be choose what channel is the presynaptic channel and what is the post_synaptic channels
			try:REST, short_pulse, T_short_pulse = phenomena(np.array(presnaptic_channel) * t_i.units,postsynaptic_channel, T, base_folder_unaligment, x_units=T[0].units,Y_units=t_i.units)
			except:
				pass
		elif f.endswith("IV.abf"):  # moria: check name?
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
			maxi = sepereat_by_current(np.array(t1) * t_i.units, T, I, save_folder_IV_curve)
			REST=read_from_pickle('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse_parameters0.p')['E_pas']
			short_pulse,T_short_pulse=read_from_pickle('cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/short_pulse/mean0_short_pulse.p')
			maxi = np.append(maxi, find_maxi(np.array(short_pulse) + REST, save_folder_IV_curve)[0])
			I.append(-50)
			with open(save_folder_IV_curve + 'max_vol_curr_inj.p', 'wb') as fr:
				pickle.dump([maxi * t_i.units, I * pq.pA], fr)
			I_V_curve(maxi, I * pq.pA, save_folder_IV_curve)
			check_dynamics(short_pulse, T_short_pulse, create_folder_dirr(base_external_folder + '/check_dynamic/'))
		else:
			print("Error. Wrong file ending for " + f)



