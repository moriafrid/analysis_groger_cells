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
