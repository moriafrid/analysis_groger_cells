from scipy.signal import find_peaks
import numpy as np
from parameters_short_pulse import short_pulse_evaluate_size


def get_inj(T,I,V):
    #found the begining,end and median of the injection
    I_abs = np.abs(I)
    inj_start = np.where(I_abs > I_abs.max() / 4.0)[0][0] - 1
    inj_end = np.where(I_abs > I_abs.max() / 4.0)[0][-1]
    inj = np.median(I[inj_start:inj_end])
    return inj, T[inj_start], T[inj_end]

def find_injection(V,E_PAS,prominence=1,duration=200):
    peak=[]
    while len(peak)<1:
        peak,par=find_peaks(abs(V), prominence=prominence)
        print('peak place is', peak)
        prominence-=0.3

    end=peak[np.argmax(par['prominences'])]
    start=end-duration
    idx_start = np.where(V[start:]<E_PAS)[0][0] + start
    # idx_end_decay= np.where(V[start:]<E_PAS)[0][0] + start
    return idx_start ,end
def find_short_pulse_edges(signal,prominence=0.5,height=0.1):
    peak0,parameters0=find_peaks(abs(signal),prominence=0.4)
    arregment_peaks0=np.argsort(parameters0['prominences'])
    short_pulse_end=peak0[arregment_peaks0[0]]
    prominence=0.4
    height=0.1

    peak1,parameters1=find_peaks(signal[short_pulse_end-short_pulse_evaluate_size:short_pulse_end]-np.mean(signal[short_pulse_end-short_pulse_evaluate_size:short_pulse_end]),prominence=prominence,height=height)
    while len(peak1)<1:
        prominence-=0.05
        height-=0.05
        print(prominence,height)
        peak1,parameters1=find_peaks(signal[short_pulse_end-short_pulse_evaluate_size:short_pulse_end]-np.mean(signal[short_pulse_end-short_pulse_evaluate_size:short_pulse_end]),prominence=prominence,height=height)
    peak1+=short_pulse_end-short_pulse_evaluate_size
    arregment_peaks1=np.argsort(parameters1['peak_heights'])
    short_pulse_start=peak1[arregment_peaks1[0]]
    return short_pulse_start,short_pulse_end


def initiate_simulation(self):
    clamp = h.IClamp(self.soma(0.5))  # insert clamp(constant potentientiol) at the soma's center
    clamp.amp = -0.05  ##nA
    clamp.dur = 200
    clamp.delay = 296
    ######################################################
    # load the data and see what we have
    ######################################################
    V = np.array(self.short_pulse[0])
    T = np.array(self.short_pulse[1])
    T = T - T[0]
    E_PAS = np.mean(V[:2000])
    h.tstop = (T[-1] - T[0]) * 1000
    h.v_init = E_PAS
    h.dt = 0.1
    h.steps_per_ms = h.dt
    return clamp,E_PAS, T, V
