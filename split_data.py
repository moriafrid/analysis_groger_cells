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


def create_folders(folders_list):
    for curr in folders_list:
        try:
            os.makedirs(curr)
        except FileExistsError:
            pass


# try:	os.mkdir(folder_ + 'data')
# except FileExistsError:	pass
# try:os.mkdir(base+'traces_img')
# except FileExistsError:pass
# for phen in ['V1', 'short_pulse', 'syn', 'spike', 'noise']:
# 	try:os.mkdir(base + phen)
# 	except FileExistsError:pass


def split2phenomena(inputs_folder, important_outputs_folder, all_outputs_folder):
	"""
	important_outputs_folder: <repository>/cells_important_outputs_data/<cell_name>
	all_outputs_folder: <repository>/cells_outputs_data/<cell_name>
	"""
	base_folder = os.path.join(important_outputs_folder, 'data', 'electrophysio_records/')
	base_external_folder = os.path.join(important_outputs_folder, 'data/')
	save_external_folder = base_external_folder + '/'
	folder_names = ['V1', 'short_pulse', 'syn', 'spike', 'noise1', 'noise2']
	create_folders([os.path.join(base_folder, n) for n in folder_names])

	abf_files = glob(os.path.join(inputs_folder, '*.abf'))
	print("Found input files {0} in {1}".format(abf_files, inputs_folder))
	for f in abf_files[:]:  # take the abf file (from 3)
		print(f, flush=True)
		save_folder = os.path.join(base_folder, f[f.rfind('/') + 1:-4]) + '/'
		create_folders([save_folder])

		r = io.AxonIO(f)
		bl = r.read_block(lazy=False)
		hz = [np.array(segment.analogsignals[0].sampling_rate) for segment in bl.segments]
		t, T, t1, t2 = [], [], [], []
		second_channel = True
		for segment in tqdm(bl.segments):
			t_i = segment.analogsignals[0]
			channel1 = [v[0] for v in np.array(t_i)]
			t.append(t_i)
			t1.append(channel1)

			if second_channel:
				channel2 = [v[1] for v in np.array(t_i)]
				t2.append(channel2)
			T_i = np.linspace(segment.analogsignals[0].t_start, segment.analogsignals[0].t_stop, int(len(t_i)))
			T.append(T_i)

		with open(save_folder + '/full_channel.p', 'wb') as fr:
			pickle.dump([t, T], fr)
		with open(save_folder + '/first_channel.p', 'wb') as fr:
			pickle.dump([np.array(t1) * t_i.units, T], fr)
		add_figure(f[f.rfind('/') + 1:-4] + '\n first_channel', T[0].units, t[0].units)
		plt.plot(np.array(T).flatten(), np.array(t1).flatten())
		plt.savefig(save_folder + '/first_channel.png')
		plt.savefig(save_folder + '/first_channel.pdf')

		if second_channel:
			with open(save_folder + '/second_channel.p', 'wb') as fr:
				pickle.dump([np.array(t2) * t_i.units, T], fr)
			plt.close()
			add_figure(f[f.rfind('/') + 1:-4] + '\n second_channel', T[0].units, t[0].units)
			plt.plot(np.array(T).flatten(), np.array(t2).flatten())
			plt.savefig(save_folder + '/second_channel.png')
			plt.savefig(save_folder + '/second_channel.pdf')

		# split to syn, short_pulse, spike ,noise
		if f.endswith(".abf") and "stable_conc_aligned" and "average" in f:  # pattern: *stable_conc_aligned_average*.abf
			pass
		elif f.endswith(".abf") and "stable_conc_aligned" in f:  # pattern: *stable_conc_aligned*.abf
			print(f, 'correct one_data')
			REST, short_pulse, T_short_pulse = phenomena(np.array(t1) * t_i.units, T, base_folder, x_units=T[0].units,
														 Y_units=t_i.units)
		elif f.endswith(".abf"):  # moria: check name?
			# cell_name = '2017_05_08_A_0006'
			save_folder_IV_curve = save_folder  # moria
			I = [-200, -160, -120, -80, -40, -0, 40, 80, 120, 160]
			# print(f,'correct IV_curve')
			maxi = sepereat_by_current(np.array(t1) * t_i.units, T, I, save_folder_IV_curve)
			maxi = np.append(maxi, find_maxi(np.array(short_pulse) - REST, save_folder_IV_curve))
			I.append(-50)
			with open(save_folder_IV_curve + 'max_vol_curr_inj.p', 'wb') as fr:
				pickle.dump([maxi * short_pulse.units, I * pq.pA], fr)
			I_V_curve(maxi, I * pq.pA, save_folder_IV_curve)
			create_folders([save_external_folder + '/check_dynamic/'])
			check_dynamics(short_pulse, T_short_pulse, save_external_folder + '/check_dynamic/')
		else:
			print("Error. Wrong file ending for " + f)


