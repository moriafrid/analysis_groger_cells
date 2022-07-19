from show_and_edit_graph import Graph_edit,move_axes
import matplotlib.pyplot as plt
from open_pickle import read_from_pickle
# def myPlotting(..., ax=None):
#     if ax is None:
#         # your existing figure generating code
#         ax = gca()

cell_name='2017_05_08_A_4-5'
base_dir='final_data/'+cell_name+'/'

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(20,20))
# fig.subplots_adjust(left=0.05,right=0.95,top=0.99,bottom=0.01,hspace=0.1, wspace=0.1)
# plt.title(cell_name)
fig_neuron=read_from_pickle(base_dir+'neuron_morphology_fig.p')
move_axes(ax[0], fig_neuron)

# ax[0].plot(fig_neuron)
fig1=Graph_edit(base_dir+'clear_short_pulse_after_peeling.p')
# fig1.first_edition()
# fig1.change_axis_name(title='clear long pulse')
fig1.savefig()

fig2=Graph_edit(base_dir+'I_V_curve_fit.p')
fig2.first_edition()
move_axes(ax[1], fig2)
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
