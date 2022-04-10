import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure
import pickle
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['png.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
def check_dynamics(short_pulse,x_short_pulse,save_folder):
    add_figure('short_pulse',x_short_pulse.units,short_pulse.units)
    plt.plot(x_short_pulse,short_pulse,'.')
    plt.savefig(save_folder+'/the short pulse')
    print("Done {0}".format(save_folder+'/short_pulse'))
    fig=add_figure('2 part of short_pulse on each other',x_short_pulse.units/1000,short_pulse.units)
    min_index=np.argmin(short_pulse)
    max_index=np.argmax(short_pulse)
    part1=short_pulse[max_index:min_index]-short_pulse[max_index]
    part2=-short_pulse[min_index:]+short_pulse[min_index]
    x_part1=x_short_pulse[max_index:min_index]-x_short_pulse[max_index]
    x_part2=x_short_pulse[min_index:]-x_short_pulse[min_index]
    plt.plot(x_part1*1000, part1)
    plt.plot(x_part2[:len(x_part1)]*1000,part2[:len(x_part1)])
    plt.legend(['beginigng','flip end'])
    plt.savefig(save_folder+'/check_dynamics.png')
    plt.savefig(save_folder+'/check_dynamics.pdf')
    pickle.dump(fig, open(save_folder+'/check_dynamics.p', 'wb'))

    print("Done {0}".format(save_folder+'/short_pulse'))




