import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
import pickle
import matplotlib
from open_one_data import find_short_pulse_edges
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def check_dynamics(short_pulse,x_short_pulse,save_folder):
    add_figure('short_pulse','ms','mV')
    plt.plot(x_short_pulse,short_pulse,'.')
    plt.savefig(save_folder+'/the short pulse')
    print("Done {0}".format(save_folder+'/short_pulse'))
    fig=add_figure('2 part of short_pulse on each other','s','mV')
    short_pulse_start,short_pulse_end=find_short_pulse_edges(short_pulse)

    part1=short_pulse[short_pulse_start:short_pulse_end]-short_pulse[0]
    part2=-short_pulse[short_pulse_end:]+short_pulse[short_pulse_end]
    x_part1=x_short_pulse[short_pulse_start:short_pulse_end]
    plt.plot(x_part1*1000, part1)
    plt.plot(x_part1*1000,part2[:len(x_part1)])
    plt.legend(['beginigng','flip end'])
    plt.savefig(save_folder+'/check_dynamics.png')
    plt.savefig(save_folder+'/check_dynamics.pdf')
    pickle.dump(fig, open(save_folder+'/check_dynamics.p', 'wb'))

    print("Done {0}".format(save_folder+'/short_pulse'))




