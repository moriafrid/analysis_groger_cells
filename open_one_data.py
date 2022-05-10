import numpy as np
import pickle
import matplotlib.pyplot as plt
from add_figure import add_figure
import signal
from scipy.signal import find_peaks
from extra_function import SIGSEGV_signal_arises
import matplotlib
from parameters_short_pulse import *#start_decey2fit, end_decey2fit,start_full_capacity,end_full_capacity
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)

def reshape_data(data):
	minlen = min(len(r) for r in data)
	new = []
	for i in data:
		if minlen - len(i) < 0:
			new.append(np.delete(i, np.s_[minlen - len(i):]))
		else:
			new.append(i)
	return new

def correct_rest(phenomena,rest_point=[]):
	new_phenomena=[]
	rest=[]
	for i, v in enumerate(phenomena):
		v =v-np.mean(v[rest_point[0]:rest_point[1]])
		new_phenomena.append(v)
		rest.append(np.mean(v[rest_point[0]:rest_point[1]]))
	return new_phenomena,rest

def find_places(signal,prominence=0.5,two_peak=True):
	peak,parameters=find_peaks(signal,prominence=prominence,distance=100)
	if len(peak)<2 and two_peak:
		raise "find peaks didn't found enoght peaks"
	arregment_peaks=np.argsort(parameters['prominences'])
	spike_peak=peak[arregment_peaks[-1]]
	if len(peak)>1 :
		short_pulse_peak=peak[arregment_peaks[-2]]
	else:
		short_pulse_peak=None
	return spike_peak,short_pulse_peak

def find_short_pulse_edges(signal,prominence=0.5,height=0.1):
	prominence=0.5
	height=0.1
	peak0,parameters0=find_peaks(abs(signal),prominence=0.4)
	arregment_peaks0=np.argsort(parameters0['prominences'])
	short_pulse_end=peak0[arregment_peaks0[0]]

	peak,parameters=find_peaks(signal,prominence=prominence,height=height)
	while len(peak)<1:
		prominence-=0.01
		height-=0.01
		peak1,parameters1=find_peaks(signal[short_pulse_end-short_pulse_evaluate_size:short_pulse_end],prominence=prominence,height=height)

	arregment_peaks1=np.argsort(parameters['peak_heights'])
	short_pulse_start=peak1[arregment_peaks1[0]]+short_pulse_end-short_pulse_evaluate_size
	return short_pulse_start,short_pulse_end

def clear_phenomena_partial_std(phenomena,phenomena_name,part_name,base,std_max=1.5,start=None,end=None):
	phenomena_mean=np.mean(phenomena,axis=0)
	phenomena_std=np.std(phenomena,axis=0)
	filtered = []
	index2del=[]
	count=0
	for i,v in enumerate(phenomena):
		if np.all(np.abs(v-phenomena_mean)[start:end]<phenomena_std[start:end]*std_max):
			filtered.append(v)
		else:
			index2del.append(i)
			count+=1

	filtered = np.array(filtered)

	fig=add_figure('clear part from start '+str(start)+' to end '+str(end)+'with std of '+str(std_max),'point','mV')
	for v in filtered:
		plt.plot(v,alpha=0.6)
	plt.plot(phenomena_mean,'black')
	plt.fill_between(range(len(phenomena_mean))[start:end], phenomena_mean[start:end]-phenomena_std[start:end], phenomena_mean[start:end]+phenomena_std[start:end], label='std',color='grey', alpha=0.6, zorder=10)
	plt.fill_between(range(len(phenomena_mean))[start:end], phenomena_mean[start:end]-2*phenomena_std[start:end], phenomena_mean[start:end]+2*phenomena_std[start:end], label='std*2',color='grey', alpha=0.4, zorder=10)
	print(len(phenomena), filtered.shape)
	print(count,' is remove out of '+str(len(phenomena))+' from '+part_name,'by std of '+str(std_max))

	plt.suptitle(str(count)+' is remove out of '+str(len(phenomena))+' from '+part_name+'by std of '+str(std_max))
	plt.savefig(base+phenomena_name+'/noise2clear_by_std_'+part_name+'_'+phenomena_name)
	pickle.dump(fig, open(base +phenomena_name+'/noise2clear_by_std_'+part_name+'_'+phenomena_name+'.p', 'wb'))
	plt.show()
	# plt.close()
	return index2del,filtered

def clear_phenomena_partial_peaks(phenomena,phenomena_name,part_name,base,prominanace=0.4,start=None,end=None):
	phenomena_mean=np.mean(phenomena,axis=0)
	index2del,index2delby_peak=[],[]
	fig=add_figure('clear noises from ' + phenomena_name +' by peaks with prominance of '+str(prominanace), 'Vec_index', 'mV')
	without_peaks=[]
	count_peaks=0
	for i, v in enumerate(phenomena):
		erae2clear=np.array(v[start:end])
		noise_peak,parameter=find_peaks(erae2clear,prominence=prominanace)
		plt.plot(v,alpha=0.2)
		if len(noise_peak)>0:
			index2delby_peak.append(i)
			plt.plot(v,'blue',linewidth=1,label='clear by noise_peaks')
			count_peaks+=1
		else:
			without_peaks.append(v)
			plt.plot(v,linewidth=1)

	print(count_peaks,' is remove from '+part_name,'by noisy peaks of randomal synapse activity')
	plt.plot(range(len(phenomena_mean))[start:end],phenomena_mean[start:end],'black',lw=2,zorder=10)

	plt.suptitle(str(count_peaks)+ ' out of '+str(len(phenomena))+ ' remove from graph by noise synapses')
	plt.savefig(base+phenomena_name+'/noise2clear_by_peaks'+part_name+'_'+phenomena_name)
	pickle.dump(fig, open(base +phenomena_name+'/noise2clear_by_peaks'+part_name+'_'+phenomena_name+'.p', 'wb'))

	plt.show()
	# plt.close()
	return index2delby_peak,without_peaks

def clear_phenomena(phenomena,phenomena_name,base,std_mean=3,std_max=6,bymax=False, bymean=True):
	index2del= []
	mean_V = np.mean(np.array(phenomena), axis=0)
	count1, count2 = 0, 0
	add_figure('clear noises from '+phenomena_name,'Vec_index','mV')
	for i, v in enumerate(phenomena):
		data_np=np.array(v)
		m = data_np.mean(axis=0)
		s = data_np.std(axis=0)
		plt.plot(v,alpha=0.2)
		if bymean:
			if np.mean(mean_V)>m+std_mean*s or np.mean(mean_V)<m-s*std_mean:
				plt.plot(v,'blue',alpha=0.3,linewidth=1,label='clear by mean')
				index2del.append(i)
				count1+=1

		if bymax:
			if  max(v) > np.mean(m)+s*std_max or min(v) < np.mean(m)-s*std_max:
				#phenomena.pop(i)
				plt.plot(v,'black',linewidth=1,label='clear by max')
				index2del.append(i)
				count2+=1
	if bymean and bymax:
		plt.suptitle(str(count1)+' remove by std_mean (blue) and '+str(count2)+ ' by std_max (black)')
	elif bymean and not bymax:
		plt.suptitle(str(count1)+' remove by std_mean - blue')
	elif bymax and not bymean:
		plt.suptitle( str(count2)+ ' remove by std_max - black')

	plt.savefig(base+phenomena_name+'/noise2clear_'+phenomena_name)
	plt.close()
	return index2del


def phenomena(t1,t2,T,base,x_units='S',Y_units='mV'):
	# this function get two channel and sperete them to the phnomenas : spike, syn, and short_plse
	# its save them in the base folder and clear short pulse from the initial noises
	spike_place,_=find_places(np.mean(t1,axis=0),two_peak=False)
	spike_place2,short_pulse_place=find_places(np.mean(abs(t1),axis=0))
	if abs(spike_place-spike_place2)>2000:
		short_pulse_place=spike_place2

	short_pulse_start,short_pulse_end=find_short_pulse_edges(np.mean(t1,axis=0)[short_pulse_place-5000:short_pulse_place+3000])
	short_pulse_start+=short_pulse_place-5000
	short_pulse_end+=short_pulse_place-5000


	syn_place,_= find_places(np.mean(t2,axis=0),two_peak=False)

	V,short_pulse,spike,syn,noise1,noise2,noise3,rest4list,mean_V =[], [], [],[], [],[],[],[],[]
	syn0,short_pulse0,spike0=[],[],[]
	for v in np.array(t1):
		if short_pulse_end>spike_place:
			noise1_temp=(v[spike_place+1000:short_pulse_end-2000])
		else:
			noise1_temp=(v[short_pulse_end+3000:spike_place-1000])
		first_phen=min(syn_place,short_pulse_place,spike_place)
		noise2_temp=(v[first_phen-1500:])
		last_phen=max(syn_place,short_pulse_place,spike_place)
		noise3_temp=(v[last_phen+3000:])
		rest1=np.mean(noise1_temp)
		rest2=np.mean(noise2_temp)
		rest3=np.mean(noise3_temp)

		initial_rest=np.nanmean([rest1,rest2,rest3])
		rest4list.append(initial_rest)

		V.append(v-initial_rest)
		short_pulse.append(v[short_pulse_start-2000:short_pulse_end+3000]-initial_rest)
		if short_pulse_start>spike_place:
			noise1.append(v[spike_place+1000:short_pulse_start-2000]-initial_rest)
		else:
			noise1.append(v[short_pulse_end+3000:spike_place-1000]-initial_rest)
		spike.append(v[spike_place-1000:spike_place+1000]-initial_rest)
		syn.append(v[syn_place-1000:syn_place+1500]-initial_rest)
		first_phen=min(syn_place,short_pulse_place,spike_place)
		noise2.append(v[first_phen-1500:]-initial_rest)
		last_phen=max(syn_place,short_pulse_place,spike_place)
		noise3.append(v[last_phen+1500:]-initial_rest)
		mean_V.append(np.mean(v)-initial_rest)

		short_pulse0.append(v[short_pulse_start-2000:short_pulse_end+3000])
		spike0.append(v[spike_place-1000:spike_place+1000])
		syn0.append(v[syn_place-1000:syn_place+1500])


	T_short_pulse=T[0][short_pulse_start-2000:short_pulse_end+3000]
	T_spike=T[0][spike_place-1000:spike_place+1000]
	T_syn=T[0][syn_place-1000:syn_place+1500]
	T_V=T[0]
	for y_phen,x,name in zip([syn0,short_pulse0,spike0],[T_syn,T_short_pulse,T_spike],['syn/initial_syn','short_pulse/initial_short_pulse','spike/initial_spike']):
		fig=add_figure('initial data','ms','mV')
		for y in y_phen:
			plt.plot(x,y)
		pickle.dump(fig, open(base + name+'.p', 'wb'))

		plt.savefig(base + name+'.pdf')
		plt.close()
	for y_phen,x,name in zip([syn,short_pulse,spike],[T_syn,T_short_pulse,T_spike],['syn/syn','short_pulse/short_pulse','spike/spike']):
		fig=add_figure('data aftre rest correction','ms','mV')
		for y in y_phen:
			plt.plot(x,y)
		plt.savefig(base + name+'-rest.pdf')
		pickle.dump(fig, open(base + name+'-rest.p', 'wb'))

		plt.close()
	with open(base + '/V1/V.p', 'wb') as f:
		pickle.dump( [V,T], f)
	with open(base+'/syn/syn.p', 'wb') as f:
		pickle.dump( [np.array(syn)*t1.units,T_syn], f)
	with open(base+'/short_pulse/short_pulse.p', 'wb') as f:
		pickle.dump([np.array(short_pulse)*t1.units,T_short_pulse], f)
	with open(base + '/spike/spike.p', 'wb') as f:
		pickle.dump([np.array(spike)*t1.units,T_spike], f)
	with open(base + '/noise1/noise1.p', 'wb') as f:
		pickle.dump(np.array(noise1), f)
	with open(base + '/noise2/noise2.p', 'wb') as f:
		pickle.dump(np.array(noise2), f)
	with open(base + '/noise3/noise3.p', 'wb') as f:
		pickle.dump(np.array(noise3), f)
	REST=np.mean(rest4list)
	short_pulse_mean=np.mean(short_pulse,axis=0)
	plt.show()

	new_short_pulse0,E_pas_short_pulse_0=correct_rest(short_pulse,[short_pulse_start+start_calculate_E_pas,short_pulse_start+end_calculate_E_pas]) #moria not change a lot
	std_max=1.3
	index2del_short_pulse2,new_short_pulse1 = clear_phenomena_partial_std(new_short_pulse0, 'short_pulse','decay', base ,std_max=std_max,start=short_pulse_start+start_decey2fit,end=short_pulse_start+end_decey2fit)

	while len(new_short_pulse1)<35 :#or index2del_short_pulse/len(new_short_pulse1)<0.4 or :
		std_max+=0.1
		index2del_short_pulse2,new_short_pulse1 = clear_phenomena_partial_std(new_short_pulse0, 'short_pulse','decay', base ,std_max=std_max,start=short_pulse_start+start_decey2fit,end=short_pulse_start+end_decey2fit)

	prominanace=0.4
	index2del_short_pulse1,new_short_pulse2 = clear_phenomena_partial_peaks(new_short_pulse1, 'short_pulse','center', base ,prominanace=prominanace,start=short_pulse_end+start_full_capacity,end=short_pulse_end+end_full_capacity)

	while len(new_short_pulse2)<28:#or index2del_short_pulse/len(new_short_pulse1)<0.3 or :
		prominanace+=0.05
		index2del_short_pulse1,new_short_pulse2 = clear_phenomena_partial_peaks(new_short_pulse1, 'short_pulse','center', base ,prominanace=prominanace,start=short_pulse_end+start_full_capacity,end=short_pulse_end+end_full_capacity)

	prominanace=0.5
	index2del_short_pulse2,new_short_pulse3 = clear_phenomena_partial_peaks(new_short_pulse2, 'short_pulse','center_end', base ,prominanace=prominanace,start=short_pulse_end+end_full_capacity,end=short_pulse_end-end_not_very_clear)
	while len(new_short_pulse2)<25:#or index2del_short_pulse/len(new_short_pulse1)<0.2 or :
		prominanace+=0.05
		index2del_short_pulse1,new_short_pulse2 = clear_phenomena_partial_peaks(new_short_pulse1, 'short_pulse','center_end', base ,prominanace=prominanace,start=short_pulse_end+end_full_capacity,end=short_pulse_end-end_not_very_clear)


	# new_short_pulse2 = np.delete(new_short_pulse1, list(index2del_short_pulse), axis=0)+ REST

	names=['short_pulse','spike']
	for i,phenomena in enumerate([new_short_pulse2,spike]):
		plt.close()
		fig=add_figure('clear '+names[i],'index',t1.units)
		for v in phenomena:
			plt.plot(v,alpha=0.1,lw=0.5,color='grey')
		plt.plot(np.mean(phenomena,axis=0),'black',lw=3)
		plt.savefig(base+names[i]+'/clear0_'+names[i])
		pickle.dump(fig, open(base+names[i]+'/clear0_'+names[i]+'_fig.p', 'wb'))

		with open(base +names[i]+'/clear0_'+names[i]+'.p', 'wb') as f:
			pickle.dump( [np.array(phenomena),eval('T_'+names[i])], f)

	with open(base + '/V1/clear_V.p', 'wb') as f:
		pickle.dump( np.array(V), f)

	for i,phenomena in enumerate([new_short_pulse2,spike]):
		fig=add_figure('mean '+names[i],eval('T_'+names[i])[0].units,t1.units)
		mean=np.mean(phenomena,axis=0)
		plt.plot(eval('T_'+names[i]),mean)
		plt.savefig(base+names[i]+'/mean0_'+names[i])
		pickle.dump(fig, open(base+names[i]+'/mean0_'+names[i]+'.p', 'wb'))

		with open(base +names[i]+'/mean0_'+names[i]+'.p', 'wb') as f:
			pickle.dump( [mean*t1.units,eval('T_'+names[i])], f)
	with open(base + '/V1/mean_V.p', 'wb') as f:
		pickle.dump( [np.mean(np.array(V),axis=0)*t1.units,T[0]], f)

	E_pas_short_pulse= np.mean([new_short_pulse2[i][short_pulse_start +start_calculate_E_pas:short_pulse_start+end_calculate_E_pas] for i in range(len(new_short_pulse2))])
	E_pases=E_pas_short_pulse
	point2calculate_E_pas=[short_pulse_start +start_calculate_E_pas,short_pulse_start+end_calculate_E_pas]
	names2='short_pulse'
	mean=np.mean(new_short_pulse2,axis=0)
	with open(base +names2+'/mean0_'+names2+'_with_parameters.p', 'wb') as f:
			pickle.dump({'mean':[mean * t1.units, eval('T_' + names2)],'E_pas':REST,'points2calsulate_E_pas':point2calculate_E_pas }, f)
		# pickle.dump({'mean':[mean * t1.units, eval('T_' + names2)],'E_pas':E_pas_short_pulse+REST,'points2calsulate_E_pas':point2calculate_E_pas }, f)
	with open(base +'/short_pulse_parameters0.p', 'wb') as f:
			pickle.dump({'units':{'y':t1.units,'x': T[0].units},'E_pas':REST,'points2calsulate_E_pas':point2calculate_E_pas }, f)

	#add to the other currents for I-V curve
	fig=add_figure('I_V curve_together', 'points', t1.units)
	plt.plot(new_short_pulse2)
	plt.savefig(base + '/-50pA.png')
	plt.savefig(base + '/-50pA.pdf')
	pickle.dump(fig, open(base + '/-50pAt.p', 'wb'))

	with open(base + '/-50pA.p', 'wb') as f:
		pickle.dump({'mean': [np.mean(new_short_pulse2,axis=0) * t1.units, T_short_pulse], 'E_pas': REST,}, f)
	return REST,np.mean(new_short_pulse2,axis=0)* t1.units,T_short_pulse

