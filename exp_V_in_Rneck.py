import os
from find_MOO_file import MOO_file, check_if_continue, model2run
from open_MOO_after_fit import OPEN_RES
import numpy as np
from neuron import h
import matplotlib.pyplot as plt
from glob import glob
from read_spine_properties import get_sec_and_seg, get_building_spine, get_n_spinese, get_parameter, calculate_Rneck
from tqdm import tqdm
import pickle
import matplotlib
from open_pickle import read_from_pickle
from extraClasses import neuron_start_time
import sys
from find_MOO_file import MOO_file
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
print(sys.argv)
if len(sys.argv) != 2:
    specipic_cell='*'
    run_reorgenize=False
    print("sys.argv isn't run")
else:
    print("the sys.argv len is correct",flush=True)
    specipic_cell = sys.argv[1]
    if specipic_cell=='None':
        specipic_cell='*'
        run_reorgenize=False
    else:
        run_reorgenize=True

folder_= ''
save_name='/Voltage in neck'
folders=[]

folders=[*set(folders)]
def get_segment_length_lamda(seg):
    """
	return the segment  e_length
	:param seg_len:
	:param RM:
	:param RA:
	:return:
	"""
    sec = seg.sec
    seg_len = sec.L/sec.nseg #micro meter
    d = seg.diam #micro meter
    R_total = 1.0 / seg.g_pas #Rm[cm^2*oum] sce.Ra[cm*oum]
    lamda = np.sqrt((R_total / sec.Ra) * (d / 10000.0) / 4.0) #micro meter
    return (float(seg_len) / 10000.0) / lamda

def cumpute_distances(base_sec,base_seg=None):
    sec_length=0
    if not base_sec is None:
        for seg in base_sec:
            if seg<base_seg:
                sec_length += get_segment_length_lamda(seg)

    for sec in h.SectionRef(sec=base_sec).child:
        for seg in sec:
            sec_length += get_segment_length_lamda(seg)
        cumpute_distances(sec)
    return sec_length

for curr_i, model_place in tqdm(enumerate(model2run())):
    if 'syn_xyz' in model_place:
        sec_from_picture=False
    else:
        sec_from_picture=True
    type=model_place.split('/')[-1]
    cell_name=model_place.split('/')[1]
    # if not '05_12_A' in model_place:continue
    # if get_n_spinese(cell_name)==2:continue
    if type=='test': continue
    try:loader = OPEN_RES(res_pos=model_place+'/', curr_i=curr_i)
    except:
        print(model_place + '/hall_of_fame.p is not exsist' )
        continue
    psd_sizes=get_parameter(cell_name,'PSD')

    if 'relative' in model_place:
        argmax=np.argmax(psd_sizes)
        reletive_strengths=psd_sizes/psd_sizes[argmax]
    else:
        # if get_n_spinese(cell_name)>1:continue
        reletive_strengths=np.ones(get_n_spinese(cell_name))
    RDSM_objective_file = folder_+'cells_initial_information/'+cell_name+"/mean_syn.p"
    V_data,T_data=read_from_pickle(RDSM_objective_file)
    T_with_units=T_data-T_data[0]
    T_with_units=T_with_units*1000
    T_base = np.array(T_with_units)
    V_base = np.array(V_data)
    # T_with_units=T_data.rescale('ms')
    # spike_timeing=T_base[np.argmax(np.array(V_base))-65]
    spike_timeing=T_base[read_from_pickle('syn_onset.p')[cell_name]]
    total_duration=T_base[-1] + neuron_start_time
    # V_base=V_base+E_PAS
    model=None
    model=loader.get_model()

    h=loader.sim.neuron.h
    netstim = h.NetStim()  # the location of the NetStim does not matter
    netstim.number = 1
    netstim.start = spike_timeing + neuron_start_time
    netstim.noise = 0
    h.tstop = total_duration
    special_sec=''
    if cell_name =='2017_04_03_B':
        for n in np.arange(1,7):
            if '_'+str(n)+'_' in model_place.split('/')[-2]:
                special_sec='_'+str(n)


    secs,segs=get_sec_and_seg(cell_name,from_picture=sec_from_picture,special_sec=special_sec)
    num=0
    V_spine=[]
    V_base_neck=[]
    spines=[]
    syn_objs=[]
    imps_base=[]
    imps_spine_head=[]
    seg_for_record_base=[]
    seg_for_record_head=[]
    g_spine_NMDA,g_spine_AMPA=[],[]
    # imp_soma=h.Impedance(sec=model.soma[0])
    imp_soma=h.Impedance()
    seg_for_record=model.soma[0](0.5)
    imp_soma.loc(seg_for_record,sec=seg_for_record.sec)
    distance,lambdas=[],[]
    for sec,seg in zip(secs,segs):
        dict_spine_param=get_building_spine(cell_name,num)
        spine, syn_obj = loader.create_synapse(loader.get_sec(sec), seg,reletive_strengths[num], number=num,netstim=netstim)
        spines.append(spine)
        syn_objs.append(syn_obj)
        V_spine.append(h.Vector())
        V_spine[num].record(spine[1](1)._ref_v) #thh spine head
        V_base_neck.append(h.Vector())
        V_base_neck[num].record(loader.get_sec(sec)(seg)._ref_v) #the neck base

        seg_for_record_base.append(loader.get_sec(sec)(seg))
        imps_base.append(h.Impedance())
        # imps_base.append(h.Impedance(sec=loader.get_sec(sec)))
        # imps_base[num].loc(0) #spine base = on dend segment
        imps_base[num].loc(seg_for_record_base[num],sec=seg_for_record_base[num].sec) #spine base = on dend segment

        seg_for_record_head.append(spine[1](1))
        imps_spine_head.append(h.Impedance())

        g_spine_NMDA.append(h.Vector())
        g_spine_NMDA[num].record(syn_obj[1][0]._ref_g_NMDA)
        g_spine_AMPA.append(h.Vector())
        g_spine_AMPA[num].record(syn_obj[0][0]._ref_g)
        # imps_spine_head.append(h.Impedance(sec=spine[1]))
        # imps_spine_head[num].loc(1) #spine_head
        imps_spine_head[num].loc(seg_for_record_head[num],sec=seg_for_record_head[num].sec) #spine_head
        lambdas.append(cumpute_distances(loader.get_sec(sec),seg))
        distance.append(h.distance(model.soma[0](0.5),loader.get_sec(sec)(seg)))
        num+=1

    time = h.Vector()
    time.record(h._ref_t)
    V_soma = h.Vector()
    V_soma.record(model.soma[0](0.5)._ref_v)
    h.dt = 0.1
    h.steps_per_ms = 1.0/h.dt

    h.run()

    # Rin_soma=imp_soma.input(0)
    imp_soma.compute(0)
    Rin_soma=imp_soma.input(0.5,sec=model.soma[0])

    Rin_base,Rtrans_base=[],[]
    for num, imp in enumerate(imps_base):
        imp.compute(0)
        Rin_base.append(imp.input(seg_for_record_base[num],sec=seg_for_record_base[num].sec))
        Rtrans_base.append(imp.transfer(model.soma[0](0.5),sec=model.soma[0]))
        # Rtrans_base.append(imp.transfer(model.soma[0](0.5)))

    Rin_head,Rtrans_head=[],[]
    for num,imp in enumerate(imps_spine_head):
        imp.compute(0)
        Rin_head.append(imp.input(seg_for_record_head[num],sec=seg_for_record_head[num].sec))
        Rtrans_head.append(imp.transfer(model.soma[0](0.5),sec=model.soma[0]))
    passive_propert_title='Rm='+str(round(1.0/model.soma[0].g_pas,2)) +' Ra='+str(round(model.soma[0].Ra,2))+' Cm='+str(round(model.soma[0].cm,2))
    cut_from_start_time=int(neuron_start_time/0.1)

    V_soma=np.array(V_soma)[cut_from_start_time:]
    time=np.array(time)[cut_from_start_time:]-time[cut_from_start_time]
    names=["A","B"]

    fig = plt.figure(figsize=(10,10))

    if get_n_spinese(cell_name) == 2:
       axs = fig.subplot_mosaic("""AB""")
    else:
       axs = fig.subplot_mosaic("""A""")

    fig.suptitle('Voltage in Spine base\n '+" ".join([model_place.split('/')[1],model_place.split('/')[-1] ,'\n',model_place.split('/')[4],model_place.split('/')[2]])+'\n'+passive_propert_title)
    dicty={}
    dicty['time']=time
    parameters_dict={'reletive_strengths':reletive_strengths,'PSD':psd_sizes,'RA':loader.get_param('Ra'),'RM':1.0/loader.get_param('g_pas'),'CM':loader.get_param('cm'),'E_PAS':loader.get_param('e_pas'),'Rneck':calculate_Rneck(cell_name,Ra=loader.get_param('Ra'))}
    dicty['parameters']=parameters_dict
    for j in range(len(V_spine)):
        V_spine[j]=np.array(V_spine[j])[cut_from_start_time:]
        V_base_neck[j]=np.array(V_base_neck[j])[cut_from_start_time:]
        axs[names[j]].set_title('spine'+str(j)+" "+secs[j]+" "+str(segs[j]))
        # axs[names[j]].plot(time, V_soma,'green',label='V_soma higth:'+str(round(np.amax(V_soma)-np.amin(V_soma),2))+'mV')
        axs[names[j]].plot(time, V_spine[j],'orange',label='V_spine'+str(j)+ ' higth:'+str(round(np.amax(V_spine[j])-np.amin(V_spine[j]),2))+'mV')
        axs[names[j]].plot(time, V_base_neck[j],'green',label='V_base_neck'+str(j)+ ' higth:'+str(round(np.amax(V_base_neck[j])-np.amin(V_base_neck[j]),2))+'mV')
        axs[names[j]].set_xlabel('time [ms]')
        axs[names[j]].set_ylabel('voltage [mv]')
        axs[names[j]].legend()
        axs[names[j]].plot(np.array(T_base), np.array(V_base)+loader.get_param('e_pas'), color='black',label='EP record',alpha=0.2,lw=5)
        dicty['voltage_'+str(j)]={'V_head':V_spine[j],'V_base_neck':V_base_neck[j]}

    pickle.dump(dicty, open(model_place+save_name+'_pickles.p', 'wb'))
    parameters_dict['distance']=distance
    parameters_dict['lambda']=lambdas
    parameters_dict['W_AMPA']=loader.get_param('weight_AMPA')
    parameters_dict['W_NMDA']=loader.get_param('weight_NMDA')
    parameters_dict['g_NMDA_spine']=[max(np.array(v)*1000) for v in g_spine_NMDA]
    parameters_dict['tau1_AMPA']=loader.get_param('exp2syn_tau1')
    parameters_dict['tau2_AMPA']=loader.get_param('exp2syn_tau2')
    parameters_dict['tau1_NMDA']=loader.get_param('NMDA_tau_r_NMDA')
    parameters_dict['tau2_NMDA']=loader.get_param('NMDA_tau_d_NMDA')
    V_high_base_neck=np.amax(V_base_neck,axis=1)-loader.get_param('e_pas')
    V_high_spine_head=np.amax(V_spine,axis=1)-loader.get_param('e_pas')

    pickle.dump({'soma':{'Rin':Rin_soma},'neck_base':{'Rin':Rin_base,'Rtrans':Rtrans_base,'V_high':V_high_base_neck},
                 'spine_head':{'Rin':Rin_head,'Rtrans':Rtrans_head,'V_high':V_high_spine_head},'parameters':parameters_dict}, open(model_place+'/Rins_pickles.p', 'wb'))

    plt.savefig(model_place+save_name+'.png')
    plt.savefig(model_place+save_name+'.pdf')
    pickle.dump(fig, open(model_place+save_name+'.p', 'wb'))
    # plt.show()
    plt.close()

    loader.destroy()
    model.destroy()
os.system("python csv_for_MOO_results_final.py")

if specipic_cell=='*':
    specipic_cell="None"
if run_reorgenize:
    os.system('python reorgenize_results.py None _after_shrink total_moo')




