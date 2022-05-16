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
folder_data='cells_initial_information/'
# cells=['2017_07_06_C_3-4']
def linear(x, m,c):
    return m*x+c
def calculate_tau_m(cell_name):
    global folder_save
    #show the chooseing pulses
    read_from_pickle(glob(folder_+cell_name+'/data/electrophysio_records/short_pulse/clear_short_pulse__after_peeling.p')[0])
    plt.show()
    short_pulse_path=glob(folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p')[0]
    short_pulse_par=read_from_pickle(glob(folder_+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')[0])
    folder_save=folder_+cell_name+'/fit_short_pulse/tau_m_calculation/'
    create_folder_dirr(folder_save)

    again='y'
    again2='y'

    pulse,T=read_from_pickle(short_pulse_path)
    start_short_pulse,end_short_pulse=find_short_pulse_edges(pulse)
    #if i want i ca add one dot in the middle and still i wnt to understand what timegive ne the best fir results
    # need to run the function again (less lan(Vexp(t0)) to find tau1
    pulse=pulse[start_short_pulse+2:3000]
    pulse-=min(pulse)

    T=T[start_short_pulse+2:3000]
    E_PAS=short_pulse_par['E_pas']
    # T.rescale('ms')
    # T = np.arange(0, len(pulse), 1) #* 0.1
    np_pulse=np.array(pulse)
    ln_pulse=np.log(np_pulse)
    plt.plot(pulse)
    plt.scatter(0,pulse[0])
    plt.scatter(np.arange(len(pulse))[np.where(pulse==0)],0)
    plt.plot(ln_pulse)
    plt.show()
    while again=="y":
        fig=add_figure(cell_name,'ms','ln(mV)')
        dot1=int(input("put the begining dot for the decay"))
        dot2=int(input("put the end dot for the decay"))
        m_temp=(ln_pulse[dot2]-ln_pulse[dot1])/(dot2-dot1)
        tau_m_temp=-1/m_temp*hz*1000 #from micro farad to mili farad
        ax = fig.subplot_mosaic("""AB""")
        ax['A'].plot(pulse)
        ax['A'].plot(ln_pulse,label='ln('+cell_name+')')
        ax['A'].plot([dot1,dot2],[ln_pulse[dot1],ln_pulse[dot2]],'*',color='red',label=str([dot1,dot2]))
        ax['A'].plot(np.arange(dot1,dot2),ln_pulse[dot1:dot2],'yellow')

        popt0, pcov0 = curve_fit(linear, np.arange(dot1,dot2), ln_pulse[dot1:dot2])
        m,c=popt0
        taum=-1/m*hz*1000

        ax['A'].plot(np.arange(0,len(T)), linear(np.array(np.arange(0,len(T))), *popt0), lw=1, label='tau_m=' + str(taum) + ' 1/s',alpha=0.5)

        ax['B'].plot(pulse,label='pulse')
        ax['B'].plot(np.exp(+m*np.arange(0,len(pulse))+c),label='tau_m')
        ax['A'].legend()
        ax['B'].legend()
        plt.savefig(folder_save+'/calculate_tau_m.pdf')
        plt.savefig(folder_save+'/calculate_tau_m.png')
        pickle.dump(fig, open(folder_save+'/calculate_tau_m.p', 'wb'))
        plt.show()
        again=input("chose another dots? (y/n")


    pulse_1=np_pulse-np.exp(+m*np.arange(0,len(pulse))+c)
    ln_pulse1=np.log(pulse_1)
    first_nan=np.where(np.isnan(ln_pulse1)==True)[0][0]

    m1,c1,[dot3,dot4]=calculate_tau1(np_pulse,m,c,cell_name)
    tau_1=-1/m1*hz*1000 #from micro farad to mili farad

    plt.plot(pulse,label='pulse')
    plt.plot(np.exp(+m*np.arange(0,len(pulse))+c),label='tau_m=' + str(taum) + ' 1/s')
    plt.plot(np.exp(+m*np.arange(0,len(pulse))+c)+np.exp(+m1*np.arange(0,len(pulse))+c1),label='tau_1=' + str(tau_1) + ' 1/s')

    # plt.plot(T,ln_pulse,label='ln('+cell_name+')')
    # plt.plot([T[dot1],T[dot2]],[ln_pulse[dot1],ln_pulse[dot2]],'*',color='red',label=str([dot1,dot2]))
    # plt.plot(T[dot1:dot2],ln_pulse[dot1:dot2],'yellow')
    # popt0, pcov0 = curve_fit(linear, T[dot1:dot2], ln_pulse[dot1:dot2])
    # plt.plot(T, linear(np.array(T), *popt0), lw=1, label='tau_m=' + str(tau_m) + ' 1/s',alpha=0.5)
    #
    # plt.plot([T[dot3],T[dot4]],[ln_pulse[dot3],ln_pulse[dot4]],'*',color='red',label=str([dot1,dot2]))
    # plt.plot(T[dot3:dot4],ln_pulse[dot3:dot4],'yellow')
    # popt1, pcov1 = curve_fit(linear, T[dot3:dot4], ln_pulse[dot3:dot4])
    # plt.plot(T, linear(np.array(T), *popt1), lw=1, label='tau_1=' + str(tau_1) + ' 1/s',alpha=0.5)
    plt.legend()
    plt.savefig(folder_save+'/calculate_taus.pdf')
    plt.savefig(folder_save+'/calculate_taus.png')
    pickle.dump(fig, open(folder_save+'/calculate_taus.p', 'wb'))
    plt.show()

    # d={'decay': taum, 'dots2calculate_tau_m': [dot1, dot2],'tau1:':tau_1,'dots2calculate_tau1': [dot3, dot4]}
    # df=pd.DataFrame(data=d)
    # df.to_csv('cells_initial_information/'+cell_name+"/taues.csv")

    dict_for_records = {}

    # add metadata
    dict_for_records['decay'] = taum
    dict_for_records['dot1_tau_m'] =dot1
    dict_for_records['dot2_tau_m']=dot2
    dict_for_records['tau1'] = tau_1
    dict_for_records['dots3_tau1'] =dot3
    dict_for_records['dots4_tau1'] =dot4
    # df=pd.DataFrame(data=dict_for_records)
    # df.to_csv('cells_initial_information/'+cell_name+"/taues.csv")

    dicty={'decay': taum, 'dot1_tau_m': dot1, 'dot2_tau_m':dot2,'tau1':tau_1,'dots3_tau1': dot3,'dots4_tau1': dot4}
    dict_for_records.update(dicty)
    output_df = pd.DataFrame.from_records([dicty])
    output_df.to_csv(folder_data+cell_name+"/taues.csv", index=False)
    return dict_for_records
    # return {'decay': taum, 'dots2calculate_tau_m': [dot1, dot2],'tau1':tau_1,'dots2calculate_tau1': [dot3, dot4]}
    # return {'decay': taum, 'dots2calculate_tau_m': [dot1, dot2]}
def calculate_tau1(pulse,m,c,cell_name=''):
    pulse_1=pulse-np.exp(+m*np.arange(0,len(pulse))+c)
    ln_pulse=np.log(pulse_1)
    first_nan=np.where(np.isnan(ln_pulse)==True)[0][0]
    print('the correct places '+str(first_nan))
    fig=add_figure('from where calculate tau1','dots','mv')
    plt.plot(pulse_1)
    plt.plot(ln_pulse)
    plt.plot(ln_pulse[:first_nan])
    plt.plot(ln_pulse[:first_nan],'.')

    plt.savefig(folder_save+'/place2cal_tau1.pdf')
    plt.savefig(folder_save+'/place2cal_tau1.png')
    pickle.dump(fig, open(folder_save+'/place2cal_tau1.p', 'wb'))
    plt.show()

    ln_pulse=ln_pulse[:first_nan]
    again2='y'
    while again2=="y":

        fig=add_figure(cell_name,'ms','ln(mV)')
        dot3=int(input("put the begining dot for the decay"))
        dot4=int(input("put the end dot for the decay"))
        ax = fig.subplot_mosaic("""AB""")
        ax['A'].plot(pulse_1[:first_nan],label='pulse antil '+str(first_nan))
        ax['A'].plot(ln_pulse,label='ln_pulse')
        ax['A'].plot([dot3,dot4],[ln_pulse[dot3],ln_pulse[dot4]],'*',color='red',label=str([dot3,dot4]))
        ax['A'].plot(np.arange(dot3,dot4),ln_pulse[dot3:dot4],'yellow',label='area2calculate')
        m1_temp=(ln_pulse[dot4]-ln_pulse[dot3])/(dot4-dot3)
        tau_1_temp=-1/m1_temp*hz*1000 #from micro farad to mili farad

        popt1, pcov1 = curve_fit(linear, np.arange(dot3,dot4), ln_pulse[dot3:dot4])
        m1,c1=popt1
        tau1=-1/m1*hz*1000
        ax['A'].plot(np.arange(0,len(ln_pulse)), linear(np.array(np.arange(0,len(ln_pulse))), *popt1), lw=1, label='tau1=' + str(tau1) + ' 1/s',alpha=0.5)
        ax['B'].plot(pulse,label='pulse')
        ax['B'].plot(np.exp(+m*np.arange(0,len(pulse))+c),label='taum')

        ax['B'].plot(np.exp(+m*np.arange(0,len(pulse))+c)+np.exp(+m1*np.arange(0,len(pulse))+c1),label='tau1')

        ax['A'].legend()
        ax['B'].legend()
        plt.savefig(folder_save+'/calculate_tau1.pdf')
        plt.savefig(folder_save+'/calculate_tau1.png')
        pickle.dump(fig, open(folder_save+'/calculate_tau1.p', 'wb'))
        plt.show()
        again2=input("chose another dots? (y/n")



    return m1,c1,[dot3,dot4]






if __name__=='__main__':
    hz=0.1
    tau_m={}
    all_data=[]

    for cell_name in ['2017_04_03_B']:#cells[10:]:
        print(cell_name)
        dicty=calculate_tau_m(cell_name)
        # tau_m[cell_name]
        dict_for_records = {}
        dict_for_records['cells_name']=cell_name
        dict_for_records.update(dicty)
        all_data.append(dict_for_records)
        output_df = pd.DataFrame.from_records(all_data)
        output_df.to_excel(folder_+"tau_m_cells2.xlsx", index=False)
        output_df.to_csv(folder_data+"tau_cells2.csv", index=False)

        # print(tau_m)
        # df1 = pd.DataFrame(dicty,index=0)
        # df1.to_excel(folder_+"tau_m_cells.xlsx")
        # print(df1)
