import numpy as np
from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from add_figure import add_figure
from extra_function import create_folders_list
import sys
import pickle
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

if len(sys.argv)!=5:
    # cells= ['2017_05_08_A_4-5(0)','2017_05_08_A_5-4(0)','2017_03_04_A_6-7(0)']
    cells= read_from_pickle('cells_name2.p')

    folder_='cells_outputs_data_short/'
else:
    cells = [sys.argv[1],sys.argv[2],sys.argv[3]]
    folder_=sys.argv[4]+'/cells_outputs_data_short/'
# cells=['2017_05_08_A_4-5']
def linear(x, m,c):
    return m*x+c
def calculate_tau_m(short_pulse_path,folder_save):
    again='y'
    short_pulse_dict=read_from_pickle(short_pulse_path)
    pulse=short_pulse_dict['mean'][0][1000:3000]
    E_PAS=short_pulse_dict['E_pas']

    # T=read_from_pickle(short_pulse_path)[1][1000:3000].rescale('ms')
    T = np.arange(0, len(pulse), 1) #* 0.1
    ln_pulse=np.log(np.array(pulse-min(pulse)))
    plt.plot(ln_pulse)
    plt.show()
    while again=="y":
        fig=add_figure(cell_name,'0.1 ms','ln(mV)')
        dot1=int(input("put the begining dot for the decay"))
        dot2=int(input("put the end dot for the decay"))
        m=(ln_pulse[dot2]-ln_pulse[dot1])/(dot2-dot1)
        tau_m=-1/m*hz*1000 #from micro farad to mili farad
        plt.plot(T,ln_pulse,label='ln('+cell_name+')')
        plt.plot([T[dot1],T[dot2]],[ln_pulse[dot1],ln_pulse[dot2]],'*','gold',label=str([dot1,dot2]))
        plt.plot(T[dot1:dot2],ln_pulse[dot1:dot2],'yellow')
        popt, pcov = curve_fit(linear, T[dot1:dot2], ln_pulse[dot1:dot2])
        plt.plot(T, linear(np.array(T), *popt), lw=1, label='tau=' + str(tau_m) + ' 1/s',
                 alpha=0.5)
        plt.legend()
        plt.savefig(folder_save+'/calculate tau_m.pdf')
        plt.savefig(folder_save+'/calculate tau_m.png')

        pickle.dump(fig, open(folder_save+'/calculate tau_m.p', 'wb'))

        plt.show()
        again=input("chose another dots? (y/n")
    d={'decay':tau_m ,'dots2calculate':[dot1, dot2]}
    pd.DataFrame(data=d)
    return {'decay': tau_m, 'dots2calculate': [dot1, dot2]}

if __name__=='__main__':
    hz=0.1
    tau_m={}
    for cell_name in cells:
        folder_data=folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse_with_parameters.p'
        folder_save=folder_+cell_name+'/fit/'
        create_folders_list([folder_save])
        tau_m[cell_name]=calculate_tau_m(folder_data,folder_save)
    #     dicty[cell_name]=calculate_tau_m(folder_data,folder_save)
    # df=pd.DataFrame.from_dict(dicty, orient='index',
    #                    columns=['tau_m','points2calculate'])
    # df.to_excel(folder_+"tau_m_cells.xlsx")
    print(tau_m)
    df1 = pd.DataFrame(tau_m)
    df1.to_excel(folder_+"tau_m_cells.xlsx")
    print(df1)
    a=1
