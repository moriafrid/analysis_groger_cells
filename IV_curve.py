from matplotlib import pyplot as plt
import numpy as np
from add_figure import add_figure
import pickle
from scipy.optimize import curve_fit
import quantities as pq
from scipy.signal import find_peaks
from parameters_short_pulse import *



def linear(x, m):
    return m*x

def sepereat_by_current(t,T,I,save_folder):
    fig=add_figure('I_V curve_together', 'points', t.units)
    for v in np.array(t):
        plt.plot(v)
    plt.savefig(save_folder + '/I_V_curve_together')
    pickle.dump(fig, open(save_folder + '/I_V_curve_together.p', 'wb'))
    plt.close()
    maxi=[]
    for i,v in enumerate(np.array(t)):
        fig1=add_figure('Trace with current' + str(I[i]),'points',t.units)
        plt.plot(v,alpha=0.5,label='full trace')
        plt.plot(np.arange(len(v))[12000:20400], v[12000:20400])
        max_temp=np.mean(v[12000:20400])
        plt.plot([12000,20400],[max_temp,max_temp],label='max='+str(max_temp))
        plt.plot([12000,20400],[v[12000],v[20400]],'*')

        rest=np.mean(t[I.index(0)][0:10000])
        plt.plot(np.arange(len(v))[0:10000], v[0:10000])
        rest_temp = np.mean(v[0:10000])
        plt.plot([0,10000], [rest_temp, rest_temp],label='rest='+str(rest_temp))
        plt.legend()
        plt.savefig(save_folder +'/'+str(I[i])+'pA.png')
        plt.savefig(save_folder +'/'+str(I[i])+'pA.pdf')
        pickle.dump(fig1, open(save_folder +'/'+str(I[i])+'pA_fig.p', 'wb'))

        with open(save_folder+'/'+str(I[i])+'pA.p', 'wb') as file:
            pickle.dump([v*t.units,T[i]], file)
        plt.close()
        maxi.append(max_temp)
        rest=np.mean(t[I.index(0)][12000:20400])
    rest1=np.mean(t[I.index(0)])
    rest2=np.mean(t[I.index(0)][12000:20400])
    return (maxi-np.array(rest2))

def I_V_curve(maxi,I,save_file):
    fig=add_figure('I-V Curve\nfit to V=I*Rinput','Current I[pA]','Voltage V[mV]')
    plt.plot(I,maxi,'.',label='max volt to diffrent current inject')
    popt, pcov = curve_fit(linear, np.array(I), np.array(maxi))
    plt.plot(I, linear(np.array(I), *popt),label='fit=I*'+str(round(popt[0]*1e-12/1e-3*1e12,3))+'pohm')
    plt.plot(I[-1],maxi[-1],'*',label=str(I[-1])+'pA')
    I_50=[0,I[-1]]
    maxi_50=[0,maxi[-1]]
    popt1, pcov1 = curve_fit(linear, np.array(I_50), np.array(maxi_50))
    plt.plot(I, linear(np.array(I), *popt1),label='fit=I*'+str(round(popt1[0]*1e-12/1e-3*1e12,3))+'pohm')
    plt.legend()
    plt.savefig(save_file + '/I_V_curve_fit')
    pickle.dump(fig, open(save_file + '/I_V_curve_fit.p', 'wb'))
    plt.close()
    print('The input resistance from I_V cureve is ',round(popt[0]*1e-12/1e-3*1e12,3),'pOhm')
    print('The input resistance from I=-50pA is ', round(popt1[0] * 1e-12 / 1e-3 * 1e12, 3), 'pOhm')
    return popt1[0]*10e-12/10e-3*pq.ohm


def find_maxi(V,save_folder):
    # width=500
    cell_name=save_folder.split('/')[1]
    # peak,dict_peaks=find_peaks(abs(V),width=width)
    # if len(peak)<1:
    #     width-=200
    #     peak,dict_peaks=find_peaks(abs(V),width=width)
    # arregment_peaks=np.argsort(dict_peaks['widths'])
	# short_pulse_start=peak[arregment_peaks[0]]
    from extra_fit_func import short_pulse_edges
    start,end,length=short_pulse_edges(cell_name)
    # left_ips=int(dict_peaks["right_ips"][arregment_peaks[0]])+start_full_capacity
    # right_ips=int(dict_peaks["right_ips"][arregment_peaks[0]])+end_full_capacity
    left_ips=end-int(length/2)
    right_ips=end+end_full_capacity
    fig=add_figure('check if the maxi correct','ms','mV')
    plt.plot(V,label='full trace')
    plt.plot([left_ips,right_ips],[V[left_ips],V[right_ips]],'*')
    plt.plot(np.arange(left_ips,right_ips),V[left_ips:right_ips],label='max to calculate')
    plt.plot(np.arange(left_ips,right_ips),np.mean(V[left_ips:right_ips])*np.ones(right_ips-left_ips),label='max')
    plt.legend()
    plt.savefig(save_folder + '/-50pA.png')
    plt.savefig(save_folder + '/-50pA.pdf')
    pickle.dump(fig, open(save_folder + '/-50pA.p', 'wb'))
    plt.close()
    return np.mean(V[left_ips:right_ips]),[left_ips,right_ips]


