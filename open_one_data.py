import numpy as np
import pickle
import matplotlib.pyplot as plt
from add_figure import add_figure
import signal
from scipy.signal import find_peaks
from extra_function import SIGSEGV_signal_arises

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

def clear_phenomena_partial(phenomena,phenomena_name,part_name,base,prominanace=0.4,std_max=3.3,start=None,end=None):
	phenomena_mean=np.mean(phenomena,axis=0)
	add_figure('clear part of the graph by max','point','mV')
	for v in phenomena:
		plt.plot(v)
	plt.plot(np.arange(start, end), phenomena_mean[start:end],'black',linewidth=7)
	plt.savefig(base+phenomena_name+'/place2clear_bymax_'+part_name)
	index2del,index2delby_peak=[],[]
	add_figure('clear noises from ' + phenomena_name, 'Vec_index', 'mV')
	count = 0
	count_peaks=0
	for i, v in enumerate(phenomena):
		data_np=np.array(v[start:end])
		noise_peak,parameter=find_peaks(data_np,prominence=prominanace)

		m = data_np.mean(axis=0)
		s = data_np.std(axis=0)
		plt.plot(v,alpha=0.2)
		if  max(data_np) > m+s*std_max or min(data_np) < np.mean(m)-s*std_max :#or len(noise_peak)>0:
			plt.plot(v,'black',linewidth=1,label='clear by max')
			index2del.append(i)
			count+=1
		if len(noise_peak)>0:
			index2delby_peak.append(i)
			plt.plot(v,'blue',linewidth=1,label='clear by noise_peaks')
			count_peaks+=1

	print(count,' is remove from '+part_name,'by std from mean')
	print(count_peaks,' is remove from '+part_name,'by noisy peaks of randomal synapse activity')

	plt.suptitle( str(count)+ ' remove from graph by std from mean\n'+str(count_peaks)+ ' remove from graph by noise synapse/n')
	plt.savefig(base+phenomena_name+'/noise2clear_'+part_name+'_'+phenomena_name)
	plt.close()
	return index2del+index2delby_peak

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
def correct_rest(phenomena,rest_point=[]):
	new_phenomena=[]
	rest=[]
	for i, v in enumerate(phenomena):
		v =v-np.mean(v[rest_point[0]:rest_point[1]])
		new_phenomena.append(v)
		rest.append(np.mean(v[rest_point[0]:rest_point[1]]))
	return new_phenomena,rest
def find_places(signal,prominence=1,two_peak=True):
	peak,parameters=find_peaks(signal,prominence=prominence,distance=100)
	if len(peak)<2 and two_peak:
		raise "find peaks didn't found enoght peaks"
	arregment_peaks=np.argsort(parameters['prominences'])
	spike_peak=peak[arregment_peaks[-1]]
	short_pulse_peak=peak[arregment_peaks[-2]]
	return spike_peak,short_pulse_peak

def phenomena(t1,t2,T,base,x_units='S',Y_units='mV'):
	# this function get two channel and sperete them to the phnomenas : spike, syn, and short_plse
	# its save them in the base folder and clear short pulse from the initial noises
	spike_place,_=find_places(np.mean(t1,axis=0))
	spike_place2,short_pulse_place=find_places(np.mean(abs(t1),axis=0))
	if abs(spike_place-spike_place2)>2000:
		short_pulse_place=spike_place2
	syn_place,_= find_places(np.mean(t2,axis=0))
	V,short_pulse,spike,syn,noise1,noise2,rest4list,mean_V =[], [],[], [],[],[],[],[]
	for v in np.array(t1):
		noise1_temp=(v[short_pulse_place+3000:spike_place-1000])
		noise2_temp=(v[syn_place+3000:])
		rest1=np.mean(noise1_temp)
		rest2=np.mean(noise2_temp)
		initial_rest=np.nanmean([rest1,rest2])
		rest4list.append(initial_rest)

		V.append(v-initial_rest)
		short_pulse.append(v[short_pulse_place-4000:short_pulse_place+3000]-initial_rest)
		noise1.append(v[short_pulse_place+3000:spike_place-1000]-initial_rest)
		spike.append(v[spike_place-1000:spike_place+2000]-initial_rest)
		syn.append(v[syn_place-1000:syn_place+1500]-initial_rest)
		noise2.append(v[syn_place+1500:]-initial_rest)
		mean_V.append(np.mean(v)-initial_rest)
	T_short_pulse=T[0][short_pulse_place-4000:short_pulse_place+3000]
	T_spike=T[0][spike_place-1000:spike_place+2000]
	T_syn=T[0][syn_place-1000:syn_place+1500]

	T_V=T[0]
	add_figure('fully experiment',T[0].units,t1.units)
	for v in V:
		plt.plot(T_V,v,color='blue')
	plt.savefig(base + '/V1/V.png')
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
	REST=np.mean(rest4list)

	short_pulse_mean=np.mean(short_pulse,axis=0)
	short_pulse_time2clear1,_=find_places(short_pulse_mean,prominence=0.05)
	short_pulse_time2clear2,_=find_places(abs(short_pulse_mean),prominence=0.05)
#@# add a pickle to save this places
	# index2del_short_pulse_begining,new_short_pulse1 = clear_phenomena_partial(new_short_pulse, 'short_pulse','begining', base ,start=short_pulse_time2clear1-500,end=short_pulse_time2clear1-10,correct_rest=True)
	# index2del_short_pulse_middle = clear_phenomena_partial(new_short_pulse1, 'short_pulse','middle', base ,start=short_pulse_time2clear1+300,end=short_pulse_time2clear2-10,std_max=5)
	# index2del_short_pulse_end = clear_phenomena_partial(new_short_pulse1, 'short_pulse','end', base ,start=short_pulse_time2clear2+700,end=short_pulse_time2clear2+1000)
	#
	new_short_pulse1,E_pas_short_pulse_0=correct_rest(short_pulse,[short_pulse_time2clear1-500,short_pulse_time2clear1-10]) #moria not change a lot
	index2del_short_pulse = clear_phenomena_partial(new_short_pulse1, 'short_pulse','center_end', base ,prominanace=1.4,start=short_pulse_time2clear1-500,end=short_pulse_time2clear2+1000)
	new_short_pulse2 = np.delete(new_short_pulse1, list(index2del_short_pulse), axis=0)+ REST

	# syn_mean=np.mean(short_pulse,axis=0)
	# syn_time2clear1,syn_temp=find_places(syn_mean,prominence=2,two_peak=False)
	# index2del_syn = clear_phenomena_partial(syn, 'short_pulse','center_end', base ,prominanace=3,start=syn_time2clear1+300,end=len(syn[0]))
	# new_syn = np.delete(syn, list(index2del_syn), axis=0)

	names=['short_pulse','spike']
	for i,phenomena in enumerate([new_short_pulse2,spike]):
		plt.close()
		add_figure('clear '+names[i],'index',t1.units)
		for v in phenomena:
			plt.plot(v,alpha=0.1,lw=0.5,color='grey')
		plt.plot(np.mean(phenomena,axis=0),'black',lw=3)
		plt.savefig(base+names[i]+'/clear_'+names[i])
		with open(base +names[i]+'/clear_'+names[i]+'.p', 'wb') as f:
			pickle.dump( [np.array(phenomena),eval('T_'+names[i])], f)

	with open(base + '/V1/clear_V.p', 'wb') as f:
		pickle.dump( np.array(V), f)

	for i,phenomena in enumerate([new_short_pulse2,spike]):
		add_figure('mean '+names[i],eval('T_'+names[i])[0].units,t1.units)
		mean=np.mean(phenomena,axis=0)
		plt.plot(eval('T_'+names[i]),mean)
		plt.savefig(base+names[i]+'/mean_'+names[i])
		with open(base +names[i]+'/mean_'+names[i]+'.p', 'wb') as f:
			pickle.dump( [mean*t1.units,eval('T_'+names[i])], f)
	with open(base + '/V1/mean_V.p', 'wb') as f:
		pickle.dump( [np.mean(np.array(V),axis=0)*t1.units,T[0]], f)

	E_pas_short_pulse= np.mean([new_short_pulse2[i][short_pulse_time2clear1 - 500:short_pulse_time2clear1-10] for i in range(len(new_short_pulse2))])
	E_pases=E_pas_short_pulse
	point2calculate_E_pas=[short_pulse_time2clear1 - 500,short_pulse_time2clear1-10]
	names2='short_pulse'
	mean=np.mean(new_short_pulse2,axis=0)
	with open(base +names2+'/mean_'+names2+'_with_parameters.p', 'wb') as f:
		pickle.dump({'mean':[mean * t1.units, eval('T_' + names2)],'E_pas':E_pas_short_pulse+REST,'points2calsulate_E_pas':point2calculate_E_pas }, f)
	#add to the other currents for I-V curve
	add_figure('I_V curve_together', 'points', t1.units)
	plt.plot(new_short_pulse2)
	plt.savefig(base + '/-50pA.png')
	with open(base + '/-50pA.p', 'wb') as f:
		pickle.dump({'mean': [np.mean(new_short_pulse2,axis=0) * t1.units, T_short_pulse], 'E_pas': E_pases+REST,}, f)
	return REST,np.mean(new_short_pulse2,axis=0)* t1.units,T_short_pulse

