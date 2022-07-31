# import sys
import pickle
from glob import glob
import numpy as np
from matplotlib import pyplot as plt, gridspec
import pickle5 as pickle

from convert_friction import findFraction
from read_spine_properties import get_spine_xyz, get_n_spinese,get_sec_and_seg,get_parameter
from open_pickle import read_from_pickle
from matplotlib_scalebar.scalebar import ScaleBar
L_widgh=5
def find_xy(sec_dots,find_seg):
    dots_number=len(sec_dots[0])
    places=[int(find_seg/dots_number),int(find_seg/dots_number)]
    return sec_dots[0][places[0]],sec_dots[1][places[1]]
def plot_morphology(ax, segment_colors, names=[], width_mult_factors=None, seg_ind_to_xyz_coords_map={},synapse=[], without_axons=True):
    if width_mult_factors is None:
        width_mult_factor = 1.2
        width_mult_factors = width_mult_factor * np.ones((segment_colors.shape))
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
        # add synapses
        if seg_ind_to_xyz_coords_map[seg_ind]['sec name'] in synapse[0]:
        # for i,syn in enumerate(synapse):
            sec_dots=[seg_ind_to_xyz_coords_map[seg_ind]['x'],seg_ind_to_xyz_coords_map[seg_ind]['y']]
            syn_num=synapse[0].index(seg_ind_to_xyz_coords_map[seg_ind]['sec name'])
            syn_x,syn_y=find_xy(sec_dots,synapse[1][syn_num])
            psd_size=synapse[2][syn_num]/max(synapse[2])

            if psd_size==1:
                psd_size=1
            else:
                psd_size=round(psd_size,2)
                # psd_size=findFraction(str(psd_size))
            ax.scatter(x=syn_x, y=syn_y, s=200, c='r',zorder=2,alpha=0.6,label=''+str(syn_num)+'  '+str(psd_size)+'   '+str(round(synapse[2][syn_num],2)))
            if len(synapse[2])>1:
                ax.text(syn_x-1,syn_y-2,syn_num,color='black',**{'size':'12'})
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
            ax.scatter(seg_x_coords, seg_y_coords,s=500, color=seg_color,zorder=2)
        else:
            ax.plot(seg_x_coords, seg_y_coords, lw=seg_line_width, color=seg_color,zorder=1)
        plt.rcParams.update({'font.size': 12})

    if names != []:
        for ind in all_seg_inds:
            ax.text(np.max(seg_ind_to_xyz_coords_map[key]['x']), np.max(seg_ind_to_xyz_coords_map[key]['y']),
                    names[ind])




    ax.legend()
    # ax.set_xlim(-180, 235)
    # ax.set_ylim(-210, 1200);
    ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower center",rotation="horizontal"))
    plt.rcParams.update({'font.size': L_widgh})

    ax.set_axis_off()

def plot_morph(ax, cell_name, before_after,without_axons=True):
    morphology_filename=glob('cells_initial_information/'+cell_name+'/dict_morphology_swc'+before_after+'.pickle')
    seg_ind_to_xyz_coords_map=read_from_pickle(morphology_filename[0])

    num_segments=len(seg_ind_to_xyz_coords_map)
    segment_colors_selected = np.zeros(num_segments)
    segment_widths_selected = 5 * np.ones(segment_colors_selected.shape)
    synapses=list(get_sec_and_seg(cell_name))+[get_parameter(cell_name,'PSD')]

    # choosen_synpase=[]
    # for spine_num in np.arange(get_n_spinese(cell_name)):
    #     choosen_synpase.append(get_spine_xyz(cell_name,spine_num))
    plot_morphology(ax, segment_colors_selected, width_mult_factors=segment_widths_selected,
                    seg_ind_to_xyz_coords_map=seg_ind_to_xyz_coords_map,synapse=synapses, names=[], without_axons=without_axons)
    return ax

