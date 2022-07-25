# import sys
import pickle
from glob import glob
import numpy as np
from matplotlib import pyplot as plt, gridspec
import pickle5 as pickle
from read_spine_properties import get_spine_xyz, get_n_spinese
from open_pickle import read_from_pickle
from matplotlib_scalebar.scalebar import ScaleBar

def plot_morphology(ax, segment_colors, names=[], width_mult_factors=None, seg_ind_to_xyz_coords_map={},synapse=[], without_axons=True):
    if width_mult_factors is None:
        width_mult_factor = 1.2
        width_mult_factors = width_mult_factor * np.ones((segment_colors.shape))
    oreder=0
    if segment_colors.max()!=0:
        segment_colors = segment_colors / segment_colors.max()
    colors = plt.cm.gist_earth(segment_colors)
    all_seg_inds = seg_ind_to_xyz_coords_map.keys()

    # assemble the colors for each dendritic segment
    colors_per_segment = {}
    widths_per_segment = {}
    for seg_ind in all_seg_inds:
        colors_per_segment[seg_ind] = colors[seg_ind]
        widths_per_segment[seg_ind] = width_mult_factors[seg_ind]

    # plot the cell morphology
    for key in all_seg_inds:
        if without_axons:
            if 'axon' in seg_ind_to_xyz_coords_map[key]['sec name']:
                print(seg_ind_to_xyz_coords_map[key]['sec name'])
                continue
        seg_color = colors_per_segment[key]
        # seg_line_width = width_mult_factor * np.array(seg_ind_to_xyz_coords_map[key]['d']).mean()
        seg_line_width = min(6, widths_per_segment[key] * np.array(seg_ind_to_xyz_coords_map[key]['d']).mean())
        # print(np.array(seg_ind_to_xyz_coords_map[key]['d']).mean())
        seg_x_coords = seg_ind_to_xyz_coords_map[key]['x']
        seg_y_coords = seg_ind_to_xyz_coords_map[key]['y']

        if np.isscalar(seg_ind_to_xyz_coords_map[key]['x']):
            ax.scatter(seg_x_coords, seg_y_coords,s=400, color=seg_color,zorder=oreder)
            oreder+=1
        else:
            ax.plot(seg_x_coords, seg_y_coords, lw=seg_line_width, color=seg_color)
    if names != []:
        for ind in all_seg_inds:
            ax.text(np.max(seg_ind_to_xyz_coords_map[key]['x']), np.max(seg_ind_to_xyz_coords_map[key]['y']),
                    names[ind])

    # add synapses
    for i,syn in enumerate(synapse):
        ax.scatter(x=syn[0], y=syn[1], s=200, c='r',zorder=1,alpha=0.8)
        # ax.text(syn[0]+2,syn[1]+2,str(i),color='r')
    # ax.set_xlim(-180, 235)
    # ax.set_ylim(-210, 1200);
    ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower center",rotation="horizontal"))
    ax.set_axis_off()

def plot_morph(ax, cell_name, without_axons=True):
    morphology_filename=glob('cells_initial_information/'+cell_name+'/dict_morphology_swc.pickle')
    seg_ind_to_xyz_coords_map=read_from_pickle(morphology_filename[0])

    num_segments=len(seg_ind_to_xyz_coords_map)
    segment_colors_selected = np.zeros(num_segments)
    segment_widths_selected = 6 * np.ones(segment_colors_selected.shape)
    choosen_synpase=[]
    for spine_num in np.arange(get_n_spinese(cell_name)):
        choosen_synpase.append(get_spine_xyz(cell_name,spine_num))
    plot_morphology(ax, segment_colors_selected, width_mult_factors=segment_widths_selected,
                    seg_ind_to_xyz_coords_map=seg_ind_to_xyz_coords_map,synapse=choosen_synpase, names=[], without_axons=without_axons)
    return ax

