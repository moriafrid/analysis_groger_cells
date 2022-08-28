# import sys
import pickle
from glob import glob
import numpy as np
from matplotlib import pyplot as plt, gridspec
import pickle5 as pickle
from function_Figures import fontsize
from convert_friction import findFraction
from read_spine_properties import get_spine_xyz, get_n_spinese,get_sec_and_seg,get_parameter
from open_pickle import read_from_pickle
from matplotlib_scalebar.scalebar import ScaleBar
from function_Figures import text_size,legend_size
addlw=0
L_widgh=5
def find_xy(sec_dots,find_seg):
    dots_number=len(sec_dots[0])
    places=[int(find_seg*dots_number),int(find_seg*dots_number)]
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
        #     colors_per_segment[seg_ind]=colors[seg_ind]/2
            sec_dots=[seg_ind_to_xyz_coords_map[seg_ind]['x'],seg_ind_to_xyz_coords_map[seg_ind]['y']]
            syn_num=synapse[0].index(seg_ind_to_xyz_coords_map[seg_ind]['sec name'])
            syn_x,syn_y=find_xy(sec_dots,synapse[1][syn_num])
            psd_size=synapse[3][syn_num]/max(synapse[3])

            if psd_size==1:
                psd_size=1
            else:
                psd_size=round(psd_size,2)
                # psd_size=findFraction(str(psd_size))
            color=['#03d7fc','#fc8003'][int(np.where(np.array(synapse[0])==seg_ind_to_xyz_coords_map[seg_ind]['sec name'])[0])]
            label=' PSD='+str(round(synapse[3][syn_num],2))+'\u03BCm^2; '+str(round(synapse[2][syn_num],2))+' \u03BCm from the soma   '+str(psd_size*100)+'%'
            # label=str(syn_num)+'  '+str(psd_size*100)+'%         '+str(round(synapse[3][syn_num],2))+'micron^2'+'\ndis from soma='+str(round(synapse[2][syn_num],2))+' micron'
            if len(synapse[0])>1:
                ax.scatter(x=syn_x, y=syn_y, lw=10+addlw, c=color,zorder=2,alpha=1,label=str(syn_num)+label)
                # ax.text(syn_x-3,syn_y-3,syn_num,color='white',**{'size':str(text_size)})
            else:
                ax.scatter(x=syn_x, y=syn_y, lw=8+addlw, c='red',zorder=2,alpha=1,label=label)

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
            ax.scatter(seg_x_coords, seg_y_coords,lw=15, color=seg_color,zorder=2)
            ax.scatter(seg_x_coords, seg_y_coords,lw=12, color=seg_color,zorder=2)

        else:
            ax.plot(seg_x_coords, seg_y_coords, lw=seg_line_width, color=seg_color,zorder=1)
        plt.rcParams.update({'font.size': fontsize})

    if names != []:
        for ind in all_seg_inds:
            ax.text(np.max(seg_ind_to_xyz_coords_map[key]['x']), np.max(seg_ind_to_xyz_coords_map[key]['y']),
                    names[ind])

    ax.legend(loc='upper right',prop={'size':legend_size},bbox_to_anchor=(1, 0.9))
    # leg = ax.get_legend()
    # leg.legendHandles[0].set_color('red')
    # leg.legendHandles[1].set_color('yellow')

    ax.add_artist(ScaleBar(1, "um", fixed_value=50, location="lower center",rotation="horizontal"))
    # plt.rcParams.update({'font.size': L_widgh})

    ax.set_axis_off()

def plot_morph(ax, cell_name, before_after,without_axons=True):
    morphology_filename=glob('cells_initial_information/'+cell_name+'/dict_morphology_swc'+before_after+'.pickle')
    seg_ind_to_xyz_coords_map=read_from_pickle(morphology_filename[0])

    num_segments=len(seg_ind_to_xyz_coords_map)
    segment_colors_selected = np.zeros(num_segments)
    segment_widths_selected = 6 * np.ones(segment_colors_selected.shape)
    synapses=list(get_sec_and_seg(cell_name,with_distance=True))+[get_parameter(cell_name,'PSD')]
    print(synapses)
    # synapses=[get_spine_xyz(cell_name,i) for i in range(get_n_spinese(cell_name))]
    # choosen_synpase=[]
    # for spine_num in np.arange(get_n_spinese(cell_name)):
    #     choosen_synpase.append(get_spine_xyz(cell_name,spine_num))
    plot_morphology(ax, segment_colors_selected, width_mult_factors=segment_widths_selected,
                    seg_ind_to_xyz_coords_map=seg_ind_to_xyz_coords_map,synapse=synapses, names=[], without_axons=without_axons)
    return ax

if __name__=='__main__':
    cell_name = read_from_pickle('cells_name2.p')[8:10]
    print(cell_name)
    fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
    fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    shapes = (1, 2)
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    plot_morph(ax1,cell_name[0],'_after_shrink')
    plot_morph(ax2,cell_name[1],'_after_shrink')
    plt.show()
