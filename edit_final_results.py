from glob import glob

from show_and_edit_graph import Graph_edit,move_axes
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
from show_result import show_directory
import pickle
from plot_morphology_Yoni import plot_morph


cell_name='2017_05_08_A_4-5'
base_dir='final_data/'+cell_name+'/'
fig = plt.figure(figsize=(20, 20))
# fig.set_figheight(6)
# fig.set_figwidth(6)
shapes = (2, 4)
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2,fig=fig)
ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1,fig=fig)
ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1,fig=fig)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1,fig=fig)
ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1,fig=fig)

# fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(20,20))
# fig1 = plt.figure(figsize=(20,20))
# ax1 = fig1.subplot_mosaic("""ABC
# DEF""")
# fig1.subplots_adjust(left=0.02,right=0.98,top=0.99,bottom=0.01,hspace=0.05, wspace=0.05)
# plt.title(cell_name)

fig_neuron=Graph_edit(base_dir+'neuron_morphology_fig.p',fig=fig)

plt.sca(ax2)
move_axes(fig_neuron.ax, fig)
show_directory(ax1["A"],png_file=fig_neuron.get_figure())

# move_axes(ax[0], fig_neuron)

# ax[0].plot(fig_neuron)
fig_short_pulse=Graph_edit(base_dir+'clear_short_pulse_after_peeling.p')
# fig1.add_scalebar(units="milisecond")
# fig1.add_scalebar(units="m",location="lower left",length=5,orientation="horizontal")
# fig1.change_axis_name(title="Long Pulse")
show_directory(ax1["B"],png_file=fig_short_pulse.savefig())

try:
    file=glob(base_dir+'fit RA=*_RA_min_error.p')[0]
    file=glob(base_dir+'fit RA=*_RA_best_fit.p')[0]
    file=glob(base_dir+'fit RA=*_RA=120.p')[0]
    file=glob(base_dir+'fit RA=*_RA=150.p')[0]
except:
    print(file)
def find_RA(file_dirr):
    for decided_passive_params in ['RA_min_error','RA_best_fit','RA=120','RA=150']:
        if decided_passive_params in file:
            return decided_passive_params
decided_passive_params=find_RA(file)
fig_fit_short_pulse=Graph_edit(file)
show_directory(ax1["C"],png_file=fig_fit_short_pulse.savefig())


fig2=Graph_edit(glob('fit_transient_RDSM_full_relative_RA_min_error.png'))

fig2=Graph_edit(base_dir+'I_V_curve_fit.p')
fig2.savefig()


# move_axes(ax[1], fig2)
fig3=Graph_edit(base_dir+'clear_short_pulse_after_peeling.p')
fig2.first_edition()

# ax[1].plot(fig_neuron)
# ax[2].plot(Graph_edit(base_dir+))
# ax[0].set_title('selected segment', fontsize=24);
# ax[1].set_title('"nearby" segments', fontsize=24);
# ax[2].set_title('all segments (by seq order)', fontsize=24);

# ax[0].set_axis_off()
# ax[1].set_axis_off()
# ax[2].set_axis_off()



exit(0)
# def myPlotting(..., ax=None):
#     if ax is None:
#         # your existing figure generating code
#         ax = gca()
