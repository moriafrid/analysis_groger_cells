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

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def close_event():
    plt.close()

dt = 0.1
fig, ax = plt.subplots(1, 1)
timer = fig.canvas.new_timer(interval=3000)
timer.add_callback(close_event)
for cell in read_from_pickle('cells_name2.p')[5:]:#[ '2017_03_04_A_6-7(0)(0)','2017_05_08_A_5-4(0)(0)','2017_05_08_A_4-5(0)(0)']:
    base_dir="cells_outputs_data_short/"+cell+"/data/electrophysio_records/short_pulse/"
    print(cell)
    data=read_from_pickle(base_dir+"/clear0_short_pulse.p")

    dt = data[1][1]-data[1][0]
    npV=np.array(data[0])

    short_pulse_mean=np.mean(npV,axis=0)
    start_short_pulse,end_short_pulse=find_short_pulse_edges(short_pulse_mean)


    run_again='y'
    while run_again=="y":
        timer = fig.canvas.new_timer(interval=4000)
        timer.add_callback(close_event)
        # filterd_traces_first = data[0]
        filterd_traces_first = []
        correct_traces=[]
        for i,trace in enumerate(npV):
            # if i>2 : continue
            add_figure(cell+'\ntrace_number '+str(int(i))+ ' out of '+str(len(npV)),'dots','mV')
            for trace1 in npV:
                base_line = trace1[start_short_pulse+start_calculate_E_pas:start_short_pulse+end_calculate_E_pas].mean()
                plt.plot(trace1-base_line,alpha=0.3, color="k")
                # plt.plot(np.array(data[1]), trace1-base_line, color="k")

            plt.plot(short_pulse_mean,color='g')
            base_line = trace[start_short_pulse+start_calculate_E_pas:start_short_pulse+end_calculate_E_pas].mean()
            len_E_pas=(start_short_pulse+end_calculate_E_pas)-(start_short_pulse+start_calculate_E_pas)
            plt.plot(np.arange(start_short_pulse+start_calculate_E_pas,start_short_pulse+end_calculate_E_pas),base_line*np.ones(len_E_pas),color="r")
            plt.plot(trace-base_line, color="r")
            timer.start()

            plt.show()

            check = input('is the trace good bad or ugly? (good=enter,bad=b)')
            pas = np.mean(trace[start_short_pulse+start_calculate_E_pas])
            if check == '':
                filterd_traces_first.append(trace-pas)
                correct_traces.append(i)
            # filterd_traces_first.append(trace)
        filterd_traces_first = np.array(filterd_traces_first)

        try:(np.savetxt(base_dir+"/peeling.txt", "traces number is "+str(correct_traces)+"\n"+[data[1], np.mean(filterd_traces_first,axis=0).flatten()*data[0].units]))
        except:"txt not secsseed to save"
        with open(base_dir+"clear_short_pulse.p", 'wb') as handle:
            pickle.dump([data[1],filterd_traces_first], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"mean_short_pulse.p", 'wb') as handle:
            pickle.dump([data[1],np.mean(filterd_traces_first,axis=0)], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"correct_short_pulse_traces.p", 'wb') as handle:
            pickle.dump(correct_traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
        from add_figure import add_figure
        fig=add_figure('clear_short_pulse','ms','mV')
        for v in filterd_traces_first:
            plt.plot(data[1],v,'black',alpha=0.1,lw=0.2)
        plt.plot(data[1],np.mean(filterd_traces_first,axis=0),'black',lw=2,label='mean_short_pulse')
        plt.savefig(base_dir+"clear_short_pulse_after_peeling.png")
        plt.savefig(base_dir+"clear_short_pulse_after_peeling.pdf")
        pickle.dump(fig, open(base_dir+'clear_short_pulse__after_peeling.p', 'wb'))
        plt.close()
        plt.figure()
        plt.title(cell+' have '+str(len(filterd_traces_first))+'traces')
        timer = fig.canvas.new_timer(interval=10000)
        timer.add_callback(close_event)
        for v in filterd_traces_first:
            plt.plot(v)
        plt.show()
        run_again=input("run again? (y/enter)")



    plt.close()