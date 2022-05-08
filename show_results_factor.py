import re
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from pdf2image import convert_from_path

from passive_val_function import get_passive_val
from read_passive_parameters_csv import get_passive_parameter


class DataForFig:
    def __init__(self):
        self.fig_path = ""
        self.fig_title = ""
        self.parameter_str = ""


def show_directory(ax, title,png_file):
    global i
    if png_file.split('.')[-1]=='pdf':  # if only have pdf (no png) => create png and read it later
        if len(glob(png_file.replace(".pdf", ".png")))>0:
            png_file = png_file.replace(".pdf", ".png")
        else:
            images = convert_from_path(png_file)
            if len(images) == 1:
                images[0].save(png_file.replace(".pdf", ".png"))
            else:  # save per page
                print("Error. too many images")
                return
                # for page_no, image in enumerate(images):
                #     image.save(png_file.replace(".pdf", "_p{0}.png".format(page_no)))
            png_file = png_file.replace(".pdf", ".png")
    # read png
    img = mpimg.imread(png_file)
    if ax is None:
        plt.title(title)
        imgplot = plt.imshow(img)
    else:
        ax.set_title(title)
        ax.axis('off')
        ax.imshow(img)
    i+=1


def read_data(cell_name="*", same_diff="relative",passive_val_name='120',SPINE_START='20',morphology_path='z_correct.swc'):
    if num_spine==1:
        same_diff='same'
    files_list = glob('cells_outputs_data_short/'+cell_name+'/MOO_results_*'+same_diff+'*/'+morphology_path+'_SPINE_START='+SPINE_START+'/F_shrinkage*/const_param/*'+passive_val_name+'*/*.pdf')
    n_row, n_col = 3, 4  # todo change me to auto calc
    result = np.full((n_row, n_col), DataForFig())
    for z, p in enumerate(files_list):
        if p.split('/')[6] == 'test':
            continue
        # if p.split('/')[6]=='RA_min_error': continue
        # if 'double' in p.split('/')[4]: continue
        # if p.split('/')[6]!='RA_min_error':continue
        shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[4])
        shrinkage_resize=[float(num) for num in shrinkage_resize]
        if 'double_spine_area' in p.split('/')[4]:
            double_spine_area='True'
            continue
        else:
            double_spine_area='False'
        print(p)
        spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[3])[0])
        passive_vals_dict=get_passive_parameter(cell_name,double_spine_area=double_spine_area,shrinkage_resize=shrinkage_resize,spine_start=spine_start,fit_condition=p.split('/')[5],file_type='z_correct.swc')
        RA_CM_RM=get_passive_val(passive_vals_dict[p.split('/')[6]],what_return='nice_results')
        title=p.split('/')[4]+p.split('/')[6]+'\n'+RA_CM_RM
        new_data = DataForFig()  # todo change me
        result[0, 1] = new_data

    return result

def read_total_cell(cell_name,resize_by='1.0',shrinkage_by='1.0',spine_start='20'):
    #cell morphology and properties:
    fig = plt.figure(figsize=(10,10))
    plt.suptitle(cell_name+ " "+passive_val_name)
    axs = fig.subplot_mosaic("""ABCD
    EFGH
    IJKL
    MNOP""")
    plt.tight_layout()
    file_type='z_correct.swc'
    try:
        show_directory(axs[place[i]], 'diam-dis',folder_+'/data/cell_properties/'+file_type+'/diam_dis/diam-dis.pdf')
    except:
        show_directory(axs[place[i]], 'diam-dis',folder_+'/data/cell_properties/diam_dis/'+file_type+'/diam-dis.png')
    # show_text(folder_+'/data/cell_properties/diam_dis/'+file_type+'/cell_propertis.txt')
    #choose the rigth channel:
    show_directory(axs[place[i]],'morphology with syn 2D',folder_+'/synapses.pdf')
    show_directory(axs[place[i]], 'choosing the correct channels(1&2)',glob(folder_+'/data/electrophysio_records/*/IV_curve_channel1&channel2.pdf')[0])
    show_directory(axs[place[i]], 'I_V curve',glob(folder_+'/data/electrophysio_records/*/I_V_curve_together.png')[0])
    #show short pulse
    show_directory(axs[place[i]], 'short_pulse clean',folder_+'/data/electrophysio_records/short_pulse/clear_short_pulse.png')
    show_directory(axs[place[i]], 'check dynamic',folder_+'/data/check_dynamic/check_dynamics.png')
    read_from_pickle(folder_+'/data/electrophysio_records/short_pulse_parameters.p')
    #cells best result for passive parameters:
    #### show pussive_val_results
    show_directory(axs[place[i]], 'passive best fit '+passive_val_name,folder_+'/fit_short_pulse/morphology.swc_SPINE_START=20/dend*1.0&F_shrinkage=1.0/const_param/RA/fit '+passive_val_name+'.png')

    for png in glob(folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/Rin_Rm/*')[3:4]:
        show_directory(axs[place[i]], 'Rin_Rm',png)
    ##### attenuation:
    show_directory(axs[place[i]], 'clamp injection' ,glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/clamp_inj*.pdf')[0])
    show_directory(axs[place[i]], 'syn_injection',glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/syn_injection*.pdf')[0])
    #### dendogram:
    # show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/all_with_syn.pdf')
    show_directory(axs[place[i]], 'E_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf')
    # show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/all.pdf')
    show_directory(axs[place[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')

    #cells result for AMPA and NMDA leakness
    show_directory(axs[place[i]], 'syn clean',folder_+'/data/electrophysio_records/syn/clear_syn.png')
    show_directory(axs[place[i]],'syn fitting relative',glob(folder_+'/MOO_results_relative*/'+file_type+'*SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/fit_transient_RDSM.pdf')[0])
    show_directory(axs[place[i]],'syn fitting same',glob(folder_+'/MOO_results_same*/'+file_type+'*SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/fit_transient_RDSM.pdf')[0])

    # show_text(folder_+'/MOO_results/'+file_type+'/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/data.txt')



if __name__ == '__main__':
    cell_name="*5-4"
    same=False

    if '4-5' in cell_name:
        sames=[True]
    else:
        sames=[True,False]
    for same in sames:

        data = read_data(cell_name, same_diff='same')
        print(data)

        fig=plt.figure()
        # plt.title(cell_name)
        i=0
        # todo run on shape of result
        ax = fig.subplot_mosaic("""ABCD
        EFGH
        IJKL""")

        # todo run on shape of result
        # for z, p in enumerate(glob('cells_outputs_data_short/'+cell_name+'/MOO_results_'+same_diff+'*/z_correct.swc_SPINE_START=20/F_shrinkage*/const_param/*120*/*.pdf')):
        #     show_directory(ax[place[i]],title,p)


