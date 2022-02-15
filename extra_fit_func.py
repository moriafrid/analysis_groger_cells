from scipy.signal import find_peaks
import numpy as np


def get_inj(T,I,V):
    #found the begining,end and median of the injection
    I_abs = np.abs(I)
    inj_start = np.where(I_abs > I_abs.max() / 4.0)[0][0] - 1
    inj_end = np.where(I_abs > I_abs.max() / 4.0)[0][-1]
    inj = np.median(I[inj_start:inj_end])
    return inj, T[inj_start], T[inj_end]

def find_injection(V,prominence=1,duration=200):
    peak=[]
    while len(peak)<1:
        peak,par=find_peaks(abs(V),prominence=prominence)
        print('peak place is', peak)
        prominence-=0.3
    end=peak[np.argmax(par['prominences'])]
    start=end-duration
    return start ,end

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
