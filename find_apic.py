import signal
from neuron import h, gui
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from add_figure import add_figure
from glob import glob
import os

def run_find_apic(apics,last_apic):
    for child in last_apic.children():
        apics.append(child)
        run_find_apic(apics,child)
def find_apic(cell,does_axon_inside_cell):
    print("unsure that there isn't cell.axon that send to find_apic.py or del_axon=False")
    last_dend_diam=0
    for dend in cell.soma[0].children():
        if does_axon_inside_cell:
            if dend in cell.axon: continue
        if dend.diam>last_dend_diam:
            start_apic=dend
            last_dend_diam=dend.diam
    apics=[start_apic]
    run_find_apic(apics,start_apic)
    return apics
