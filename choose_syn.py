# from utils import *
import pickle,os
import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
from scipy.signal import find_peaks
def close_event():
    plt.close()

dt = 0.1
fig, ax = plt.subplots(1, 1)
timer = fig.canvas.new_timer(interval=3000)
timer.add_callback(close_event)
for cell in ['2017_03_04_A_6-7']:#[ '2017_03_04_A_6-7','2017_05_08_A_5-4','2017_05_08_A_4-5']:
    base_dir="cells_outputs_data/"+cell+"/data/electrophysio_records/syn/"
    print(cell)
    with open(base_dir+"/syn.p", 'rb') as handle:
        data = pickle.load(handle)
    dt = data[1][1]-data[1][0]
    npV=np.array(data[0])

    # syn_time2clear1=np.argmax(syn_mean)-100
    # syn_time2clear2=np.argmax(syn_mean)+40
    rest=[]
    for i,v in enumerate(npV):
        spike_place,_=find_peaks(v,prominence=3)
        if len(spike_place)>0:
            base_line = v[:940].mean()
            for spike_peak in spike_place:
                if spike_peak<940 :
                    npV[i][:spike_peak+400]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
                else:
                    npV[i][spike_peak-20:]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')

    syn_mean=np.mean(npV,axis=0)
    # filterd_traces_first = data[0]
    filterd_traces_first = []
    correct_traces=[]
    for i,trace in enumerate(npV):
        # if i>2: continue
        add_figure('trace_number '+str(i),'dots',data[0].units)
        for trace1 in npV:
            base_line = trace1[:940].mean()
            plt.plot(trace1-base_line,alpha=0.3, color="k")
            # plt.plot(np.array(data[1]), trace1-base_line, color="k")

        plt.plot(syn_mean,color='g')
        base_line = trace[:940].mean()
        plt.plot(base_line*np.ones(940),color="r")
        plt.plot(trace-base_line, color="r")
        timer.start()
        plt.show()

        check = input('is the trace good bad or ugly? (good=enter,bad=b)')
        pas = np.mean(trace[:940])
        if check == '':
            filterd_traces_first.append(trace-pas)
            correct_traces.append(i)
        # filterd_traces_first.append(trace)
    filterd_traces_first = np.array(filterd_traces_first)
    try:(np.savetxt(base_dir+"/peeling.txt", "traces number is "+str(correct_traces)+"\n"+[data[1], np.mean(filterd_traces_first,axis=0).flatten()*data[0].units]))
    except:"txt not secsseed to save"
    with open(base_dir+"clear_syn.p", 'wb') as handle:
        pickle.dump([data[1],filterd_traces_first*data[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(base_dir+"mean_syn.p", 'wb') as handle:
        pickle.dump([data[1],np.mean(filterd_traces_first,axis=0)*data[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(base_dir+"correct_syn_traces.p", 'wb') as handle:
        pickle.dump(correct_traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
from open_pickle import read_from_pickle
import numpy as np
from scipy.signal import find_peaks
import pickle
import matplotlib.pyplot as plt
p=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/2017_03_04_A_6-7/data/electrophysio_records/syn/syn.p')
t=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/2017_03_04_A_6-7/data/electrophysio_records/syn/correct_syn_traces.p')

base_dir="cells_outputs_data/2017_03_04_A_6-7/data/electrophysio_records/syn/"
a=[]
b=[]
for i in t:
    a.append(np.array(p[0][i]))
npV=a
for i,v in enumerate(npV):
    base_line = v[740:980].mean()
    spike_place,_=find_peaks(v,prominence=3)
    if len(spike_place)>0:
        for spike_peak in spike_place:
            if spike_peak<940 :
                npV[i][:spike_peak+400]=base_line
                print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
            else:
                npV[i][spike_peak-20:]=base_line
                print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
    b.append(np.array(v-base_line))
with open(base_dir+"clear_syn.p", 'wb') as handle:
    pickle.dump([p[1],b*p[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(base_dir+"mean_syn.p", 'wb') as handle:
    pickle.dump([p[1],np.mean(b,axis=0)*p[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
for cell_name in [ '2017_03_04_A_6-7','2017_05_08_A_5-4','2017_05_08_A_4-5']:
    n=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'+cell_name+'/data/electrophysio_records/syn/clear_syn.p')
    plt.figure()
    plt.title(cell_name)
    for i in n[1]:
        plt.plot(i)
plt.show()
