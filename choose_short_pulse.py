# from utils import *
import pickle,os
import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
from scipy.signal import find_peaks
import matplotlib
from open_pickle import read_from_pickle
from parameters_short_pulse import *
from open_one_data import find_short_pulse_edges
from extra_fit_func import short_pulse_edges
from glob import glob


matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def close_event():
    plt.close()

dt = 0.1
fig, ax = plt.subplots(1, 1)
timer = fig.canvas.new_timer(interval=3000)
timer.add_callback(close_event)
check='again'
#['2016_04_16_A','2017_03_04_A_6-7','2017_07_06_C_3-4']# cells with problems so I change the diarection to run on all the pulses wrong postsynaptic measerments
# run on full trace: #['2017_05_08_A_4-5,'2017_07_06_C_4-3','2017_02_20_B','2016_05_12_A, '2016_04_16_A','2017_03_04_A_6-7']
#maybe run again ['2017_04_03_B
# problem with check pro-post channels '2016_05_12_A' (split it) (and in sespicies '2017_07_06_C_4-3' (not split it))
from matplotlib import cm
cmap = 'viridis'
rgb = cm.get_cmap(cmap)
for cell in ['2017_07_06_C_4-3','2016_08_30_A']:#read_from_pickle('cells_name2.p')[:]:#['2016_05_12_A','2016_04_16_A']:#
    base_dir="cells_outputs_data_short/"+cell+"/data/electrophysio_records/short_pulse/"
    if cell in ['2017_05_08_A_4-5','2017_07_06_C_4-3','2017_02_20_B', '2016_04_16_A','2017_03_04_A_6-7','2017_04_03_B','2017_07_06_C_3-4']:
        data=read_from_pickle(base_dir+"/short_pulse.p")
    else:
        data=read_from_pickle(base_dir+"/clear0_short_pulse.p")
    if cell in ['2016_08_30_A','2017_07_06_C_4-3']:#remove the last pulse befor e they start to divargnce:
        mv=data[0].units

        before_divrgense,number_before_divrgense=[],[]

        for i,v in enumerate(data[0]):
            # start_short_pulse,end_short_pulse,length=short_pulse_edges(cell)
            # if np.mean(v[start_short_pulse:end_short_pulse])>np.mean(np.mean(data[0],axis=0)[start_short_pulse:end_short_pulse]):
            #     before_divrgense.append(v)
            #     number_before_divrgense.append(i)
            if i<len(data[0])/2:
                before_divrgense.append(v)

        data[0]=before_divrgense*mv

    # if cell in ['2017_04_03_B']:#['2017_02_20_B']:
    #     data=read_from_pickle(base_dir+"/clear_short_pulse.p")
    # else:
    #     data=read_from_pickle(base_dir+"/clear0_short_pulse.p")
    #     continue
    # data=read_from_pickle(base_dir+"/clear0_short_pulse.p")
    print(cell)

    # data=read_from_pickle(base_dir+"/short_pulse.p")

    dt = data[1][1]-data[1][0]
    npV=np.array(data[0])

    short_pulse_mean=np.mean(npV,axis=0)

    # start_short_pulse,end_short_pulse=find_short_pulse_edges(short_pulse_mean)
    start_short_pulse,end_short_pulse,length=short_pulse_edges(cell)

    timer = fig.canvas.new_timer(interval=10000)
    timer.add_callback(close_event)
    factor=int(len(rgb.colors)/len(npV)/2)
    if factor==0:
        factor=1
    for i,v in enumerate(npV):
        if i>len(rgb.colors):continue
        plt.plot(v,color=rgb.colors[i*factor],alpha=0.2)
    plt.title(cell+' have '+str(len(npV))+' traces')
    plt.show()
    timer = fig.canvas.new_timer(interval=2000)
    timer.add_callback(close_event)
    run_again='y'
    check='again'

    while run_again=="y":

        # filterd_traces_first = data[0]
        filterd_traces_first = []
        correct_traces=[]

        for i,trace in enumerate(npV):
            # if i >2 : continue
            timer = fig.canvas.new_timer(interval=2000)
            timer.add_callback(close_event)
            check='again'

            while check=='again' or check=='a':

                add_figure(cell+'\ntrace_number '+str(int(i))+ ' out of '+str(len(npV)),'dots','mV')
                for i,trace1 in enumerate(npV):
                    base_line = trace1[start_short_pulse+start_calculate_E_pas:start_short_pulse+end_calculate_E_pas].mean()
                    plt.plot(trace1-base_line,alpha=0.3, color=rgb.colors[i*factor])
                    # plt.plot(np.array(data[1]), trace1-base_line, color="k")

                plt.plot(short_pulse_mean,color='g')
                base_line = trace[start_short_pulse+start_calculate_E_pas:start_short_pulse+end_calculate_E_pas].mean()
                len_E_pas=(start_short_pulse+end_calculate_E_pas)-(start_short_pulse+start_calculate_E_pas)
                plt.plot(np.arange(start_short_pulse+start_calculate_E_pas,start_short_pulse+end_calculate_E_pas),base_line*np.ones(len_E_pas),color="r")
                plt.plot(trace-base_line, color="r")
                timer.start()

                plt.show()

                check = input('is the trace good bad or ugly? (good=enter,bad=b or again,a)')
                pas = np.mean(trace[start_short_pulse+start_calculate_E_pas:start_short_pulse+end_calculate_E_pas])

            if check == '':
                filterd_traces_first.append(trace-pas)
                correct_traces.append(i)

            elif check=='end':
                run_again='no'
                break
            continue
        filterd_traces_first = np.array(filterd_traces_first)


        try:(np.savetxt(base_dir+"/peeling.txt", "traces number is "+str(correct_traces)+"\n"+[data[1], np.mean(filterd_traces_first,axis=0).flatten()*data[0].units]))
        except:"txt not secsseed to save"
        with open(base_dir+"clear_short_pulse.p", 'wb') as handle:
            pickle.dump([filterd_traces_first*mv,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"mean_short_pulse.p", 'wb') as handle:
            pickle.dump([np.mean(filterd_traces_first,axis=0)*mv,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"correct_short_pulse_traces.p", 'wb') as handle:
            pickle.dump(correct_traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
        from add_figure import add_figure
        fig=add_figure('clear_short_pulse','ms','mV')
        for v in filterd_traces_first:
            plt.plot(data[1],v,'black',alpha=0.1,lw=0.2)

        plt.plot(data[1],np.mean(filterd_traces_first,axis=0),'black',lw=2,label='mean_short_pulse')
        plt.savefig(base_dir+"clear_short_pulse_after_peeling.png")
        plt.savefig(base_dir+"clear_short_pulse_after_peeling.pdf")
        pickle.dump(fig, open(base_dir+'clear_short_pulse_after_peeling.p', 'wb'))
        plt.close()
        plt.figure()
        plt.title(cell+' have '+str(len(filterd_traces_first))+'traces')
        timer = fig.canvas.new_timer(interval=10000)
        timer.add_callback(close_event)
        for v in filterd_traces_first:
            plt.plot(v)
        plt.show()
        new_dict={}
        temp_dict=read_from_pickle(glob(base_dir+'mean0_short_pulse_with_parameters.p')[0])
        try:
            new_dict['mean']=[np.mean(filterd_traces_first,axis=0)*mv+temp_dict['E_pas']*mv,data[1]]
        except:
            new_dict['mean']=[np.mean(filterd_traces_first,axis=0)*mv+temp_dict['E_pas'],data[1]]

        new_dict['E_pas']=temp_dict['E_pas']
        new_dict['points2calsulate_E_pas']=temp_dict['points2calsulate_E_pas']
        print(new_dict)
        print(base_dir+'mean_short_pulse_with_parameters.p')
        with open(base_dir+'mean_short_pulse_with_parameters.p', 'wb') as handle:
            pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        run_again=input("run again? (y/enter)")

unmV=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[1].units
uns=read_from_pickle(glob('cells_outputs_data_old_runs/2017_05_08_A_5-4/data/electrophysio_records/syn/mean_syn.p')[0])[0].units
for path in glob('cells_outputs_data_short/*/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p'):
    cell=path.split('/')[1]
    data=read_from_pickle(path)
    data1={}
    data1['mean']=[data['mean'][0]*unmV,data['mean'][1]*uns]
    data1['E_pas']=data['E_pas']
    data1['points2calsulate_E_pas']=data['points2calsulate_E_pas']

    with open(base_dir+'mean_short_pulse_with_parameters.p', 'wb') as handle:
        pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)
