import numpy as np
from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os
from add_figure import add_figure

def linear(x, m,c):
    return m*x+c
def calculate_tau_m(short_pulse_path,folder_save):
    again='y'
    pulse=read_from_pickle(short_pulse_path)[0][1000:3000]
    # T=read_from_pickle(short_pulse_path)[1][1000:3000].rescale('ms')
    T = np.arange(0, len(pulse), 1) * 0.1
    ln_pulse=np.log(np.array(pulse-min(pulse)))
    plt.plot(ln_pulse)
    plt.show()
    while again=="y":
        dot1=int(input("put the begining dot for the decay"))
        dot2=int(input("put the end dot for the decay"))
        m=(ln_pulse[dot2]-ln_pulse[dot1])/(dot2-dot1)
        tau_m=-1/m*hz*1000 #from micro farad to mili farad
        plt.plot(T,ln_pulse)
        # plt.plot(T[dot1:dot2],m*T[dot1:dot2]+(ln_pulse[dot1]-m*T[dot1]),'g')
        plt.plot([T[dot1],T[dot2]],[ln_pulse[dot1],ln_pulse[dot2]],'*','gold',label=tau_m)
        plt.plot(T[dot1:dot2],ln_pulse[dot1:dot2],'yellow')
        popt, pcov = curve_fit(linear, T[dot1:dot2], ln_pulse[dot1:dot2])
        plt.plot(T, linear(np.array(T), *popt), lw=1, label='tau=' + str(-1.0 / round(popt[0], 3)) + ' 1/s',
                 alpha=0.5)
        plt.scatter([T[dot1],T[dot2]], [ln_pulse[dot1],ln_pulse[dot2]], s=80, alpha=0.1)
        # print(1.0 / (abs(log_v[point[1]] - log_v[point[0]]) / abs(T[point[1]] - T[point[0]])))
        plt.legend()
        plt.show()
        again=input("chose another dots? (y/n")
    plt.savefig(folder_save+'/calculate tau_m')
    d={'decay':tau_m ,'dots2calculate':[dot1, dot2]}
    pd.DataFrame(data=d)
    return {'decay': tau_m, 'dots2calculate': [dot1, dot2]}

if __name__=='__main__':
    hz=0.1
    tau_m={}
    from extra_function import create_folders_list
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
    for cell_name in ['2017_05_08_A_4-5','2017_05_08_A_5-4','2017_03_04_A_6-7']:
        folder_data=folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p'
        folder_save=folder_+cell_name+'/fit/'
        create_folders_list([folder_save])
        tau_m[cell_name]=calculate_tau_m(folder_data,folder_save)

    print(tau_m)
    df1 = pd.DataFrame(tau_m)
    df1.to_excel(folder_+"tau_m_cells.xlsx")
    a=1
