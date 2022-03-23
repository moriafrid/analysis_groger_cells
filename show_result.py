from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pdf2image import convert_from_path
from glob import glob

SPINE_START=20
cell_name =read_from_pickle('cells_name.p')[0]
file_types=['z_correct.swc','morphology.swc','hoc','ASC']
file_type='z_correct.swc'
compare_between_types=False
compare_diffrent_passive_value=False
compare_spine_start=False
place2=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f"]

def show_directory(ax, title,png_file):
    if png_file.split('.')[-1]=='pdf':  # if only have pdf (no png) => create png and read it later
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

plt.close('all')
# for passive_val_name in ['RA=120','RA=150','RA_min_error','RA_best_fit']:
passive_val_name='RA=120'
plt.title(cell_name+ " "+passive_val_name)
#cell morphology and properties:
fig = plt.figure(figsize=(10,10))
axs = fig.subplot_mosaic("""ABC
DEF
GHI
JKL""")
plt.tight_layout()
# axs["A"].plot([1,2,3],[4,5,6])
# axs["B"].plot([1,2,3],[4,8,6])
# axs["C"].plot([1,2,3],[3,5,6])
#dim-dis
folder_='cells_outputs_data/'+cell_name
if compare_between_types:
    fig1 = plt.figure(figsize=(10,10))
    axs1 = fig1.subplot_mosaic("""AB
    CD""")
    for place,file_type in zip(["A","B","C","D"],file_types):
        show_directory(axs1[place], file_type+' diam-dis',folder_+'/data/cell_properties/diam_dis/'+file_type+'/diam-dis.png')
        # show_text('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis/'+file_type+'/cell_propertis.txt')

file_type='z_correct.swc'
show_directory(axs["A"], 'diam-dis',folder_+'/data/cell_properties/diam_dis/'+file_type+'/diam-dis.png')
# show_text('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis/'+file_type+'/cell_propertis.txt')
#choose the rigth channel:
show_directory(axs["B"],'morphology with syn 2D',folder_+'/synapses.pdf')
show_directory(axs["C"], 'choosing the correct channels(1&2)','cells_outputs_data/'+cell_name+'/data/electrophysio_records/2017_05_08_A_0004_IV/IV_curve_channel1&channel2.pdf')
show_directory(axs["D"], 'I_V curve',folder_+'/data/electrophysio_records/2017_05_08_A_0004_IV/I_V_curve_together.png')
#show short pulse
show_directory(axs["E"], 'short_pulse clean',folder_+'/data/electrophysio_records/short_pulse/clear_short_pulse.png')
show_directory(axs["F"], 'check dynamic',folder_+'/data/check_dynamic/check_dynamics.png')
read_from_pickle(folder_+'/data/electrophysio_records/short_pulse_parameters.p')
#cells best result for passive parameters:
#### show pussive_val_results
show_directory(axs["G"], 'passive best fit '+passive_val_name,folder_+'/fit_short_pulse/morphology.swc_SPINE_START=20/dend*1.0&F_shrinkage=1.0/const_param/RA/fit '+passive_val_name+'.png')

for png in glob(folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/Rin_Rm/*')[3:4]:
    show_directory(axs["G"], 'Rin_Rm',png)
##### attenuation:
show_directory(axs["H"], 'clamp injection' ,folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/clamp_inj_freq_100_for_1000ms_dend*1.0.pdf')
show_directory(axs["I"], 'syn_injection',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/syn_injection_weight=0.002_dend*1.0.pdf')
#### dendogram:
# show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/all_with_syn.pdf')
show_directory(axs["J"], 'E_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf')
# show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/all.pdf')
show_directory(axs["K"], 'M_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')

#cells result for AMPA and NMDA leakness
show_directory(axs["L"], 'syn clean','cells_outputs_data/'+cell_name+'/data/electrophysio_records/syn/clear_syn.png')
plt.show()


if compare_diffrent_passive_value:
    fig2 = plt.figure(figsize=(10,10))
    axs2 = fig2.subplot_mosaic("""ABCDE
    FGHIJ
    KLMNO
    PQRST""")
    plt.tight_layout(pad=1.08,h_pad=0.5, w_pad=0.5)
    plt.suptitle(cell_name+"properties")
    i=0
    for passive_val_name in ['RA=120','RA=150','RA_min_error','RA_best_fit']:  # mean_best_10, min_CM
        #Rin_Rm:
        from glob import glob
        for png in glob(folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/Rin_Rm/*')[3:4]:
            show_directory(axs2[place2[i]], 'Rin_Rm',png)
        i+=1
        #attenuation:
        show_directory(axs2[place2[i]], 'clamp injection' ,folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/clamp_inj_freq_100_for_1000ms_dend*1.0.pdf')
        i+=1
        show_directory(axs2[place2[i]], 'syn_injection',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/syn_injection_weight=0.002_dend*1.0.pdf')
        i+=1
        #dendogram:
        # show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/all_with_syn.pdf')
        # i+=1
        show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf')
        i+=1
        # show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/all.pdf')
        # i+=1
        show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/ASC/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')
        i+=1
        print(i)
if compare_spine_start:
    pass
