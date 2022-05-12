import numpy as np
from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from add_figure import add_figure
from extra_function import create_folder_dirr
import sys
import pickle
import matplotlib
from glob import glob
from open_one_data import find_short_pulse_edges
from parameters_short_pulse import *
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

if len(sys.argv)!=2:
    # cells= ['2017_05_08_A_4-5(0)','2017_05_08_A_5-4(0)','2017_03_04_A_6-7(0)']
    cells= read_from_pickle('cells_name2.p')
else:
    cells = read_from_pickle(sys.argv[1])
folder_='cells_outputs_data_short/'

# cells=['2017_07_06_C_3-4']
def linear(x, m,c):
    return m*x+c
def calculate_tau_m(cell_name):
    #show the chooseing pulses
    read_from_pickle(glob(folder_+cell_name+'/data/electrophysio_records/short_pulse/clear_short_pulse__after_peeling.p')[0])
    plt.show()
    short_pulse_path=glob(folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p')[0]
    short_pulse_par=read_from_pickle(glob(folder_+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')[0])
    folder_save=folder_+cell_name+'/fit_short_pulse/tau_m_calculation/'
    create_folder_dirr(folder_save)

    again='y'
    T,pulse=read_from_pickle(short_pulse_path)
    start_short_pulse,end_short_pulse=find_short_pulse_edges(pulse)

    pulse=pulse[start_short_pulse-10:3000]
    pulse-=min(pulse)

    T=T[start_short_pulse-5:3000]
    E_PAS=short_pulse_par['E_pas']
    # T.rescale('ms')
    # T = np.arange(0, len(pulse), 1) #* 0.1

    ln_pulse=np.log(np.array(pulse))
    plt.plot(pulse)
    plt.scatter(0,pulse[0])
    plt.scatter(np.arange(len(pulse))[np.where(pulse==0)],0)
    plt.plot(ln_pulse)
    plt.show()
    while again=="y":
        fig=add_figure(cell_name,'ms','ln(mV)')
        dot1=int(input("put the begining dot for the decay"))
        dot2=int(input("put the end dot for the decay"))
        m=(ln_pulse[dot2]-ln_pulse[dot1])/(dot2-dot1)
        tau_m=-1/m*hz*1000 #from micro farad to mili farad
        plt.plot(ln_pulse,label='ln('+cell_name+')')
        plt.plot([dot1,dot2],[ln_pulse[dot1],ln_pulse[dot2]],'*',color='red',label=str([dot1,dot2]))
        plt.plot(np.arange(dot1,dot2),ln_pulse[dot1:dot2],'yellow')
        popt, pcov = curve_fit(linear, np.arange(dot1,dot2), ln_pulse[dot1:dot2])
        plt.plot(np.arange(0,len(T)), linear(np.array(np.arange(0,len(T))), *popt), lw=1, label='tau=' + str(tau_m) + ' 1/s',alpha=0.5)
        plt.legend()
        plt.show()
        again=input("chose another dots? (y/n")

    plt.plot(T,ln_pulse,label='ln('+cell_name+')')
    plt.plot([T[dot1],T[dot2]],[ln_pulse[dot1],ln_pulse[dot2]],'*',color='red',label=str([dot1,dot2]))
    plt.plot(T[dot1:dot2],ln_pulse[dot1:dot2],'yellow')
    popt, pcov = curve_fit(linear, T[dot1:dot2], ln_pulse[dot1:dot2])
    plt.plot(T, linear(np.array(T), *popt), lw=1, label='tau=' + str(tau_m) + ' 1/s',
             alpha=0.5)
    plt.legend()
    plt.savefig(folder_save+'/calculate_tau_m.pdf')
    plt.savefig(folder_save+'/calculate_tau_m.png')
    pickle.dump(fig, open(folder_save+'/calculate_tau_m.p', 'wb'))
    plt.show()

    d={'decay':tau_m ,'dots2calculate':[dot1, dot2]}
    pd.DataFrame(data=d)
    return {'decay': tau_m, 'dots2calculate': [dot1, dot2]}

if __name__=='__main__':
    hz=0.1
    tau_m={}
    for cell_name in cells[2:]:
        tau_m[cell_name]=calculate_tau_m(cell_name)
        print(tau_m)
        df1 = pd.DataFrame(tau_m)
        df1.to_excel(folder_+"tau_m_cells.xlsx")
        print(df1)
