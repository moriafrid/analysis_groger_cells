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
for cell in [ '2017_03_04_A_6-7','2017_05_08_A_5-4','2017_05_08_A_4-5']:
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
            base_line = v[:1000].mean()
            for spike_peak in spike_place:
                if spike_peak<1000 :
                    npV[i][:spike_peak+400]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
                else:
                    npV[i][spike_peak-20:]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')

    syn_mean=np.mean(npV,axis=0)
    # filterd_traces_first = data[0]
    filterd_traces_first = []
    for i,trace in enumerate(npV):
        add_figure('trace_numver'+str(i),'dots',data[0].units)
        for trace1 in npV:
            base_line = trace1[:1000].mean()
            plt.plot(trace1-base_line,alpha=0.3, color="k")
            # plt.plot(np.array(data[1]), trace1-base_line, color="k")

        plt.plot(syn_mean,color='g')
        base_line = trace[:1000].mean()
        plt.plot(base_line*np.ones(1000),color="r")
        plt.plot(trace-base_line, color="r")
        timer.start()
        plt.show()

        check = input('is the trace good bad or ugly? (good=enter,bad=b)')
        pas = np.mean(trace[:1000])
        if check == '':
            filterd_traces_first.append(trace-pas)
        # filterd_traces_first.append(trace)
    filterd_traces_first = np.array(filterd_traces_first)
    np.savetxt(base_dir+"/peeling.txt", [data[1], np.mean(filterd_traces_first,axis=0).flatten()])

    with open(base_dir+"clear_syn.p", 'wb') as handle:
        pickle.dump([data[1],filterd_traces_first], handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(base_dir+"mean_syn.p", 'wb') as handle:
        pickle.dump([data[1],np.mean(filterd_traces_first,axis=0)], handle, protocol=pickle.HIGHEST_PROTOCOL)


