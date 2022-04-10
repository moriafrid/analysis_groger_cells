import matplotlib.pyplot as plt
import numpy as np
from open_pickle import read_from_pickle
from add_figure import add_figure
import sys
from extra_function import create_folder_dirr,create_folders_list
from scipy.signal import find_peaks
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['png.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

class Syn2Clear:
    def __init__(self,cell_name):
        if cell_name == "2017_05_08_A_4-5":
            self.not_sure=[12,20,26,28,47,48,49,70,71,74,78,81,85,88]
            self.cut_on_1000=[8,19,21,34,35,38,40,47,48,77,81,90]
            self.rigth=[0,1,2,3,4,5,6,9,10,14,18,21,22,23,24,25,26,27,33,35,36,37,41,43,44,45,47,48,50,51,53,55,56,58,59,62,65,66,67,72,73,74,75,76,78,79,82,86] #for time2syn+1000 and stable antil point 1200
            self.false=[7,11,13,15,16,17,29,39,42,46,49,52,54,57,60,61,63,64,68,69,71,80,83,84,85,87,88,89,91]#for time2syn+1000 and stable antil point 1200
            self.remove=[11,19,24,]
        if cell_name == "2017_05_08_A_5-4":
            self.not_sure=[12,13,14,19,34,71,88,92,155,162,178,181,199]
            self.cut_on_1500=[12,13,14,34,71,90,98,134,151,155,162,169,181,208,220,235,240,247]
            self.rigth=[1,2,3,4,5,6,7,8,9,10,11,15,16,18,20,22,24,25,26,28,29,30,31,33,34,35,37,38,39,40,41,42,43,44,45
                ,46,47,48,50,51,52,54,55,56,57,58,60,62,63,65,66,67,69,72,73,74,77,79,82,83,84,85,86,88,89,93,101,103,107,
                109,110,113,114,115,116,117,119,120,122,123,124,125,127,130,133,137,138,139,143,145,146,148,149,150,152,153,
                        154,156,160,162,163,164,165,167,168,170,171,172,173,174,175,177,178,180,181,182,183,185,187,188,190,191,192
                        ,196,197,198,199,200,202,203,205,206,207,209,210,211,212,213,214,215,216,218,219,221,222,228,230,231,233,234,
                        236,237,241,242,243,244,245,246]
            #for time2syn+500 and stable antil point 1200
            self.false=[0,17,21,23,27,32,36,43,49,53,59,61,64,68,70,75,76,78,80,81,87,90,91,94,95,96,97,99,100,102,104,105,106,108,
                        111,112,118,121,126,128,129,131,132,135,136,140,141,142,144,147,155,157,159,159,161,166,169,176,178,179,184
                ,186,188,193,194,195,201,204,217,223,224,226,227,232,238,239]#for time2syn+1000 and stable antil point 1200
            self.remove=[]
        if cell_name == "2017_03_04_A_6-7":
            self.not_sure=[]
            self.cut_on_1000=[]
            self.rigth=[] #for time2syn+1000 and stable antil point 1200
            self.false=[]#for time2syn+1000 and stable antil point 1200
            self.remove=[]

if __name__ == '__main__':
    if len(sys.argv) != 5:
        cell_name= '2017_05_08_A_5-4'
        folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
        data_dir= "cells_outputs_data_short"
        save_dir = "cells_outputs_data_short"
    else:
        cell_name = sys.argv[1]
        folder_= sys.argv[2] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
        data_dir = sys.argv[3] #cells_initial_information
        save_dir =sys.argv[4] #cells_outputs_data_short
    folder_data=    folder_+data_dir+'/'+cell_name+'/data/electrophysio_records/syn/syn.p'

    V_units,t_units=read_from_pickle(folder_data)
    V=np.array(V_units)
    syn_mean=np.mean(V,axis=0)
    syn_time2clear1=np.argmax(syn_mean)-100
    syn_time2clear2=np.argmax(syn_mean)+200
    rest=[]
    for i,v in enumerate(V):
        spike_place1,_=find_peaks(v[:syn_time2clear1],prominence=3)
        spike_place2,_=find_peaks(v[syn_time2clear2:],prominence=3)
        rest_temp=np.mean(v[syn_time2clear1 - 100:syn_time2clear1])
        rest.append(rest_temp)
        V[i] = v - rest_temp
        # new_syn.append(v[syn_time2clear1 - 500:syn_time2clear2 + 1000])
        # spike_peaks,_=find_peaks(v,prominence=3)
        if len(spike_place1)>0:
            for spike_peak in spike_place1:
                if spike_peak+400<syn_time2clear1 - 100:
                    V[i][:spike_peak+400]=None
                    print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
                else:
                    V[i]=None
        if len(spike_place2)>0:
            for spike_peak in spike_place2:
                V[i][spike_peak-20:]=None
                print('spike in trace '+str(i)+' is remove from place '+ str(spike_peak)+ ' to the end')
    REST=np.mean(rest)
    # t=t_units[syn_time2clear1 - 500:syn_time2clear2 + 1000]
    t=t_units
    correct,fulse,not_shure,after_1500=[],[],[],[]
    for i,bolt_trace in enumerate(V):
        plt.close()
        add_figure('trace num '+str(i)+'\nmean on 100 points',str(syn_time2clear1 - 500)+':'+str(syn_time2clear2 + 1000),'mv')
        for v in V:
            plt.plot(v,'grey', alpha=0.1,lw=0.5)
        mean_syn=np.mean(V,axis=0)
        plt.plot(mean_syn,'black',lw=2)
        plt.plot(bolt_trace,'green',alpha=0.5,lw=1)
        print(i)
        plt.show()
        what=input('do you think this trace is correct?')
        while what not in ['c','f','d','v']:
            what=input('do you think this trace is correct?')

        if what=='c':
            correct.append(i)
        elif what=='f':
            fulse.append(i)
        elif what=='d':
            not_shure.append(i)
        elif what=='v':
            after_1500.append(i)

        plt.close()
