import numpy as np
import matplotlib.pyplot as plt
from add_figure import add_figure

def check_dynamics(short_pulse,x_short_pulse,save_folder):
    add_figure('short_pulse',x_short_pulse.units,short_pulse.units)
    plt.plot(x_short_pulse,short_pulse,'.')
    plt.savefig(save_folder+'/short_pulse')
    print("Done {0}".format(save_folder+'/short_pulse'))
    add_figure('2 part of short_pulse on each other',x_short_pulse.units/1000,short_pulse.units)
    min_index=np.argmin(short_pulse)
    max_index=np.argmax(short_pulse)
    part1=short_pulse[max_index:min_index]-short_pulse[max_index]
    part2=-short_pulse[min_index:]+short_pulse[min_index]
    x_part1=x_short_pulse[max_index:min_index]-x_short_pulse[max_index]
    x_part2=x_short_pulse[min_index:]-x_short_pulse[min_index]
    plt.plot(x_part1*1000, part1)
    plt.plot(x_part2[:len(x_part1)]*1000,part2[:len(x_part1)])
    plt.legend(['beginigng','flip end'])
    plt.savefig(save_folder+'/check_dynamics')
    print("Done {0}".format(save_folder+'/short_pulse'))




