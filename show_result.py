from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pdf2image import convert_from_path
import io
from PIL import Image
SPINE_START=20
cell_name =read_from_pickle('cells_name.p')
file_types=['z_correct.swc','morphology.swc','hoc','ASC']
file_type='z_correct.swc'
compare_between_types=True
def show_directory(png_file,title):
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
    plt.title(title)
    img = mpimg.imread(png_file)
    imgplot = plt.imshow(img)

plt.close('all')
#compare betwee diffrent cells:
for cell_name in read_from_pickle('cells_name.p'):
    plt.title(cell_name)
    #cell morphology and properties:
    
    #cells best result for passivr parameters:

    #cells result for AMPA and NMDA leakness
    plt.show()

#show entire cell

plt.title(cell_name)
#cell morphology and properties:
fig = plt.figure(figsize=(10,10))
axs = fig.subplot_mosaic("""AAA
BBC
DEE""")
# axs["A"].plot([1,2,3],[4,5,6])
# axs["B"].plot([1,2,3],[4,8,6])
# axs["C"].plot([1,2,3],[3,5,6])
#dim-dis
if compare_between_types:
    for file_type in file_types:
        axs["A"]=show_directory('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis_'+file_type+'/diam-dis.png')
        # show_text('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis_'+file_type+'/cell_propertis.txt')
else:
    file_type='z_correct.swc'
    show_directory('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis_'+file_type+'/diam-dis.png')
    # show_text('cells_outputs_data/'+cell_name+'/data/cell_properties/diam_dis_'+file_type+'/cell_propertis.txt')
#choose the rigth channel:
show_directory('cells_outputs_data/'+cell_name+'/data/electrophysio_records/2017_05_08_A_0004_IV/IV_curve_channel1&channel2.pdf','a')
show_directory('cells_outputs_data/'+cell_name+'/data/electrophysio_records/2017_05_08_A_0004_IV/I_V_curve_together.png')
#show short pulse
show_directory('cells_outputs_data/'+cell_name+'/data/electrophysio_records/short_pulse/clear_short_pulse.png')
read_from_pickle('cells_outputs_data/'+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')
#cells best result for passive parameters:
for property in ['attenuation','Rin_Rm','dendogram']:
    for passive_val in ['RA_120','RA=150','RA_min_error','RA_best_fit']:
        show_diarectory
#cells result for AMPA and NMDA leakness
show_diarectory('cells_outputs_data/'+cell_name+'/data/electrophysio_records/syn/clear_syn.png')
plt.close('all')
folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data/'
cell_name=read_from_pickle('cells_name.p')[1]
for spine_start in [10,20,60]:
    plt.figure()
    plt.title(cell_name+'z_correct.swc_SPINE_START='+str(spine_start))
    dir=(folder+cell_name+'/fit_short_pulse/z_correct.swc_SPINE_START='+str(spine_start)+'/dend*1.0&F_shrinkage=1.0/const*/RA/analysis/diffrent RA against error.png')
    img = mpimg.imread(dir)
    imgplot = plt.imshow(img)
plt.show()
