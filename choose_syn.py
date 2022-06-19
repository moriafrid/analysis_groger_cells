# from utils import *
import pickle,os
import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
from scipy.signal import find_peaks
import matplotlib
from open_pickle import read_from_pickle
from parameters_syn import *
from add_figure import add_figure

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def close_event():
    plt.close()

dt = 0.1
fig, ax = plt.subplots(1, 1)
timer = fig.canvas.new_timer(interval=3000)
timer.add_callback(close_event)
check='again'
problematic_cells=['2017_04_03_B','2017_02_20_B','2016_08_30_A']
for cell in read_from_pickle('cells_name2.p'):#[ '2017_03_04_A_6-7(0)(0)','2017_05_08_A_5-4(0)(0)','2017_05_08_A_4-5(0)(0)']:
    if cell in '2016_05_12_A':continue
    # if cell!='2017_05_08_A_4-5':continue
    # if cell in problematic_cells:continue
    base_dir="cells_outputs_data_short/"+cell+"/data/electrophysio_records/syn/"

    print(cell)
    data=read_from_pickle(base_dir+"/syn.p")
    # if cell in read_from_pickle('cells_name2.p')[:4] or cell in read_from_pickle('cells_name2.p')[7:9]:
    #     data=read_from_pickle(base_dir+"/clear_syn.p")
    # if cell in read_from_pickle('cells_old.p'):
    #
    #     data=[]
    #     data1=read_from_pickle("cells_initial_information/"+cell+"(0)/clear_syn.p")
    #     data.append(data1[1])
    #     data.append(data1[0])


    dt = data[1][1]-data[1][0]
    npV=np.array(data[0])
    syn_mean=np.mean(npV,axis=0)
    rest=[]
    for i,v in enumerate(npV):
        spike_place,_=find_peaks(v,prominence=3)
        if len(spike_place)>0:
            base_line = v[pas_start:pas_end].mean()
            for spike_peak in spike_place:
                if spike_peak<pas_end-40 :
                    npV[i][:spike_peak+400]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
                else:
                    npV[i][spike_peak-20:]=base_line
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
        if np.max(v)>6:
            print(i)
            npV[i][:]=base_line

    timer = fig.canvas.new_timer(interval=10000)
    timer.add_callback(close_event)
    tot_base=[]
    for v in npV:
        base_line = v[pas_start:pas_end].mean()
        plt.plot(v-base_line)
        tot_base.append(base_line)

    len_E_pas=pas_end-pas_start
    plt.plot(np.mean(npV,axis=0),'black',lw=2)
    plt.plot(np.arange(pas_start,pas_end),np.mean(tot_base)*np.ones(len_E_pas),color="r",lw=1)
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
                for trace1 in npV:
                    base_line = trace1[pas_start:pas_end].mean()
                    plt.plot(trace1-base_line,alpha=0.3, color="k")
                    # plt.plot(np.array(data[1]), trace1-base_line, color="k")

                plt.plot(syn_mean,color='g')
                base_line = trace[pas_start:pas_end].mean()
                len_E_pas=pas_end-pas_start
                plt.plot(np.arange(pas_start,pas_end),base_line*np.ones(len_E_pas),color="b",lw=1)
                plt.plot(trace-base_line, color="r",lw=1)
                timer.start()

                plt.show()

                check = input('is the trace good bad or ugly? (good=enter,bad=b or again,a)')

            if check == '':
                filterd_traces_first.append(trace-base_line)
                correct_traces.append(i)

            elif check=='end':
                run_again='no'
                break
            continue
        filterd_traces_first = np.array(filterd_traces_first)


        try:(np.savetxt(base_dir+"/peeling.txt", "traces number is "+str(correct_traces)+"\n"+[data[1], np.mean(filterd_traces_first,axis=0).flatten()*data[0].units]))
        except:"txt not secsseed to save"
        with open(base_dir+"clear_syn.p", 'wb') as handle:
            pickle.dump([filterd_traces_first*data[0].units,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"mean_syn.p", 'wb') as handle:
            pickle.dump([np.mean(filterd_traces_first,axis=0)*data[0].units,data[1]], handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(base_dir+"correct_syn_traces.p", 'wb') as handle:
            pickle.dump(correct_traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
        fig=add_figure('clear_syn','ms','mV')
        for v in filterd_traces_first:
            plt.plot(data[1],v,'black',alpha=0.1,lw=0.2)

        plt.plot(data[1],np.mean(filterd_traces_first,axis=0),'black',lw=2,label='mean_syn')
        plt.savefig(base_dir+"clear_syn_after_peeling.png")
        plt.savefig(base_dir+"clear_syn_after_peeling.pdf")
        pickle.dump(fig, open(base_dir+'clear_syn_after_peeling.p', 'wb'))
        plt.close()
        plt.figure()
        plt.title(cell+' have '+str(len(filterd_traces_first))+'traces')
        timer = fig.canvas.new_timer(interval=10000)
        timer.add_callback(close_event)
        for v in filterd_traces_first:
            plt.plot(v)
        plt.savefig(base_dir+"clear_syn.png")
        plt.savefig(base_dir+"clear_syn.pdf")
        pickle.dump(fig, open(base_dir+'clear_syn_fig.p', 'wb'))
        plt.show()
        # new_dict={}
        # temp_dict=read_from_pickle(glob(base_dir+'mean0_short_pulse_with_parameters.p')[0])
        # new_dict['mean']=[np.mean(filterd_traces_first,axis=0),data[1]]+temp_dict['E_pas']
        # new_dict['E_pas']=temp_dict['E_pas']
        # new_dict['points2calsulate_E_pas']=temp_dict['points2calsulate_E_pas']
        # print(new_dict)
        # print(base_dir+'mean_syn_with_parameters.p')
        # with open(base_dir+'mean_syn_with_parameters.p', 'wb') as handle:
        #     pickle.dump(new_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        run_again=input("run again? (y/enter)")


# # from utils import *
# import pickle,os
# import numpy as np
# import matplotlib.pyplot as plt
# from add_figure import add_figure
# from scipy.signal import find_peaks
# import matplotlib
# from open_pickle import read_from_pickle
# matplotlib.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['svg.fonttype'] = 'none'
# def close_event():
#     plt.close()
#
# dt = 0.1
# fig, ax = plt.subplots(1, 1)
# timer = fig.canvas.new_timer(interval=3000)
# timer.add_callback(close_event)
# for cell in read_from_pickle('cells_name2.p'):#[ '2017_03_04_A_6-7(0)(0)','2017_05_08_A_5-4(0)(0)','2017_05_08_A_4-5(0)(0)']:
#     base_dir="cells_outputs_data_short/"+cell+"/data/electrophysio_records/syn/"
#     print(cell)
#     with open(base_dir+"/syn.p", 'rb') as handle:
#         data = pickle.load(handle)
#     dt = data[1][1]-data[1][0]
#     npV=np.array(data[0])
#
#     # syn_time2clear1=np.argmax(syn_mean)-100
#     # syn_time2clear2=np.argmax(syn_mean)+40
#     rest=[]
#     for i,v in enumerate(npV):
#         spike_place,_=find_peaks(v,prominence=3)
#         if len(spike_place)>0:
#             base_line = v[740:980].mean()
#             for spike_peak in spike_place:
#                 if spike_peak<940 :
#                     npV[i][:spike_peak+400]=base_line
#                     print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
#                 else:
#                     npV[i][spike_peak-20:]=base_line
#                     print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
#
#     syn_mean=np.mean(npV,axis=0)
#     # filterd_traces_first = data[0]
#     filterd_traces_first = []
#     correct_traces=[]
#     for i,trace in enumerate(npV):
#         # if i>2: continue
#         add_figure('trace_number '+str(i),'dots',data[0].units)
#         for trace1 in npV:
#             base_line = trace1[740:980].mean()
#             plt.plot(trace1-base_line,alpha=0.3, color="k")
#             # plt.plot(np.array(data[1]), trace1-base_line, color="k")
#
#         plt.plot(syn_mean,color='g')
#         base_line = trace[740:980].mean()
#         plt.plot(base_line*np.ones(940),color="r")
#         plt.plot(trace-base_line, color="r")
#         timer.start()
#         plt.show()
#
#         check = input('is the trace good bad or ugly? (good=enter,bad=b)')
#         pas = np.mean(trace[:940])
#         if check == '':
#             filterd_traces_first.append(trace-pas)
#             correct_traces.append(i)
#         # filterd_traces_first.append(trace)
#     filterd_traces_first = np.array(filterd_traces_first)
#     try:(np.savetxt(base_dir+"/peeling.txt", "traces number is "+str(correct_traces)+"\n"+[data[1], np.mean(filterd_traces_first,axis=0).flatten()*data[0].units]))
#     except:"txt not secsseed to save"
#     with open(base_dir+"clear_syn.p", 'wb') as handle:
#         pickle.dump([data[1],filterd_traces_first*data[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
#     with open(base_dir+"mean_syn.p", 'wb') as handle:
#         pickle.dump([data[1],np.mean(filterd_traces_first,axis=0)*data[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
#     with open(base_dir+"correct_syn_traces.p", 'wb') as handle:
#         pickle.dump(correct_traces, handle, protocol=pickle.HIGHEST_PROTOCOL)
#     from add_figure import add_figure
#     fig=add_figure('clear_syn',data[1].units,data[0].units)
#     for v in filterd_traces_first:
#         plt.plot(data[1],v,'black',alpha=0.1,lw=0.2)
#     plt.plot(data[1],np.mean(filterd_traces_first,axis=0),'black',lw=2,label='mean_syn')
#     plt.savefig(base_dir+"clear_syn.png")
#     plt.savefig(base_dir+"clear_syn.pdf")
#     pickle.dump(fig, open(base_dir+'clear_syn_fig.p', 'wb'))
#     plt.close()
# #this code is just to correct wrong loading data - need to be run fro the consule
# from open_pickle import read_from_pickle
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.signal import find_peaks
# import pickle
#
# p=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/2017_03_04_A_6-7(0)(0)/data/electrophysio_records/syn/syn.p')
# t=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/2017_03_04_A_6-7(0)(0)/data/electrophysio_records/syn/correct_syn_traces.p')
#
# base_dir="cells_outputs_data_short/2017_03_04_A_6-7(0)(0)/data/electrophysio_records/syn/"
# a=[]
# b=[]
# for i in t:
#     a.append(np.array(p[0][i]))
# npV=a
# for i,v in enumerate(npV):
#     base_line = v[740:980].mean()
#     spike_place,_=find_peaks(v,prominence=3)
#     if len(spike_place)>0:
#         for spike_peak in spike_place:
#             if spike_peak<940 :
#                 npV[i][:spike_peak+400]=base_line
#                 print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the begining')
#             else:
#                 npV[i][spike_peak-20:]=base_line
#                 print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
#     b.append(np.array(v-base_line))
# with open(base_dir+"clear_syn.p", 'wb') as handle:
#     pickle.dump({'data':[p[1], b * p[0].units]}, handle, protocol=pickle.HIGHEST_PROTOCOL)
# with open(base_dir+"mean_syn.p", 'wb') as handle:
#     pickle.dump([p[1],np.mean(b,axis=0)*p[0].units], handle, protocol=pickle.HIGHEST_PROTOCOL)
# for cell_name in [ '2017_03_04_A_6-7(0)(0)','2017_05_08_A_5-4(0)(0)','2017_05_08_A_4-5(0)(0)']:
#     n=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn.p')
#     plt.figure()
#     plt.title(cell_name)
#     for i in n[1]:
#         plt.plot(i)
# plt.show()
# plot the clear synapse syn:
# plt.close('all')
# for cell in [ '2017_03_04_A_6-7(0)(0)','2017_05_08_A_5-4(0)(0)','2017_05_08_A_4-5(0)(0)']:
#     base_dir="cells_outputs_data_short/"+cell+"/data/electrophysio_records/syn/"
#     n=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/clear_syn.p')
#
#     add_figure(cell+'clear syn',n[0].units,n[1].units)
#     for v in n[1]:
#         plt.plot(n[0],v,'black',lw=0.5,alpha=0.1)
#     plt.plot(n[0],np.mean(n[1],axis=0),'black',alpha=0.3,lw=2,label='mean_syn')
#     p=read_from_pickle('/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data_short/'+cell_name+'/data/electrophysio_records/syn/mean_syn.p')
#     plt.plot(p[0],p[1],'blue',alpha=0.3,lw=2,label='mean_syn')
#     plt.savefig(base_dir+"clear_syn.png")
#     plt.savefig(base_dir+"clear_syn.pdf")
# plt.show()
