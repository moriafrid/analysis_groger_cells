from open_pickle import read_from_pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pdf2image import convert_from_path
from glob import glob
import re
from read_passive_parameters_csv import get_passive_parameter
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

from passive_val_function import get_passive_val
SPINE_START=20

file_types=['z_correct.swc','morphology.swc','hoc','ASC']
file_type='z_correct.swc'
# for passive_val_name in ['RA=120','RA=150','RA_min_error','RA_best_fit']:
passive_val_name='RA=120'
cell_name =read_from_pickle('cells_name.p')[0]
plot_all_Moo_results=True
compare_MOO_results=True
compare_between_types=False
compare_diffrent_passive_value=False
compare_spine_start=False
show_total_results=True
compare_between_change_in_the_morphology_passive_fits=True
place=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f"]
folder_='cells_outputs_data_short/'+cell_name
folder_='cells_outputs_data_3_initial_cells/'+cell_name

i=0
def show_dirr(png_file):
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
    imgplot = plt.imshow(img)

def show_directory(ax, title="",png_file=""):
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
plt.close('all')


#dim-dis
if __name__ == '__main__':
    if compare_between_types:
        fig1 = plt.figure(figsize=(10,10))
        axs1 = fig1.subplot_mosaic("""AB
        CD""")
        for place,file_type in zip(["A","B","C","D"],file_types):
            show_directory(axs1[place], file_type+' diam-dis',folder_+'/data/cell_properties/diam_dis/'+file_type+'/diam-dis.png')
            # show_text(folder_+'/data/cell_properties/diam_dis/'+file_type+'/cell_propertis.txt')
    if show_total_results:
        resize_by=str(1.0)
        shrinkage_by=str(1.0)
        spine_start=str(20)
        # base=glob()
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
        read_from_pickle(folder_+'/data/electrophysio_records/short_pulse_parameters0.p')
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



    if compare_diffrent_passive_value:
        fig2 = plt.figure(figsize=(10,10))
        axs2 = fig2.subplot_mosaic("""ABCDEF
        GHIJKL
        MNOPQR""")
        plt.tight_layout(pad=1.08,h_pad=0.5, w_pad=0.5)
        plt.suptitle(cell_name+" "+file_type+" properties")
        i=0
        keys=[keys.split('/')[-1] for keys in glob(folder_+'/MOO_results_*/'+file_type+'/F_shrinkage=1.0_dend*1.0/const_param/*')]
        if "test" in keys: keys.remove("test")
        for passive_val_name in keys:  # mean_best_10, min_CM
            #Rin_Rm:
            for png in glob(folder_+'/data/cell_properties/'+file_type+'_SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/Rin_Rm/*')[3:4]:
                show_directory(axs2[place[i]], 'Rin_Rm',png)
            #attenuation:
            show_directory(axs2[place[i]], 'clamp injection' ,glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/clamp_inj*.pdf')[0])
            show_directory(axs2[place[i]], 'syn injection',glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/syn_injection*.pdf')[0])
            #dendogram:
            # show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/all_with_syn.pdf')
            show_directory(axs2[place[i]], 'E_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf')
            # show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/all.pdf')
            show_directory(axs2[place[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')
            show_directory(axs[place[i]],'syn fitting relative',glob(folder_+'/MOO_results_*_relative*/'+file_type+'*SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/fit_transient_RDSM.pdf')[0])
            show_directory(axs[place[i]],'syn fitting same',glob(folder_+'/MOO_results_*_same*/'+file_type+'*SPINE_START=20/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/fit_transient_RDSM.pdf')[0])
    # if see_attenuation&dendogram:
    #     for passive_val_name in keys:  # mean_best_10, min_CM
    #         #Rin_Rm:
    #         for png in glob(folder_+'/data/cell_properties/'+file_type+'_SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/Rin_Rm/*')[3:4]:
    #             show_directory(axs2[place[i]], 'Rin_Rm',png)
    #         #attenuation:
    #         show_directory(axs2[place[i]], 'clamp injection' ,glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/clamp_inj*.pdf')[0])
    #         show_directory(axs2[place[i]], 'syn injection',glob(folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/attenuations/syn_injection*.pdf')[0])
    #         #dendogram:
    #         # show_directory(axs2[place2[i]], 'E_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/all_with_syn.pdf')
    #         show_directory(axs2[place[i]], 'E_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/E_dendogram/dend_only_with_syn.pdf')
    #         # show_directory(axs2[place2[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/all.pdf')
    #         show_directory(axs2[place[i]], 'M_dendogram',folder_+'/data/cell_properties/'+file_type+'/SPINE_START=20/dend*1.0&F_shrinkage=1.0/'+passive_val_name+'/M_dendogram/dend_only.pdf')
    #         show_directory(axs2[place[i]],'syn fit',folder_+'/MOO_results/'+file_type+'/F_shrinkage=1.0_dend*1.0/const_param/'+passive_val_name+'/fit_transient_RDSM.pdf')

    if compare_between_change_in_the_morphology_passive_fits:
        fig=plt.figure()
        # plt.title(cell_name)
        dirr_len=len(glob(folder_+'/fit_short_pulse/*_SPINE_START=*/*/const_param/RA/analysis/RA const against errors2 60.png'))
        if dirr_len<=10:
            ax = fig.subplot_mosaic("""ABC
            DEF
            GHI""")
        else:
            ax = fig.subplot_mosaic("""ABCD
            EFGH
            IJKL
            """)
        i=0
        for z,p in enumerate(glob(folder_+'/fit_short_pulse/*_SPINE_START=*/*/const_param/RA/analysis/RA const against errors2 60.png')):
            show_directory(ax[place[i]],p.split('/')[3]+'\n'+p.split('/')[4],p)

    if plot_all_Moo_results:
        same=True
        if '4-5' in cell_name:
            same=True

        if same==True:
            same_diff='same'
        else:
            same_diff='relative'
        if '6-7' in cell_name:
            same_diff=''

        fig=plt.figure()
        # plt.title(cell_name)
        i=0
        # ax = fig.subplot_mosaic("""AB
        # CD""")
        dirr=glob(folder_+'/MOO_results_'+same_diff+'*/z_correct.swc_SPINE_START=20/F_shrinkage*1.0**1.0*/const_param/*best*/fit_transient_RDSM.png')
        dirr_len=len(dirr)

        if dirr_len<10:
            ax = fig.subplot_mosaic("""ABC
            DEF
            GHI
            """)
        elif dirr_len<=13:
            ax = fig.subplot_mosaic("""ABC
            DEF
            GHI
            JKL
            """)
        elif dirr_len>14:
            ax = fig.subplot_mosaic("""ABCD
            EFGH
            IJKL
            MNOP
            """)

        # passive_vals_dict=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=int(SPINE_START),file_type=file_type)
        # ax = fig.subplot_mosaic("""ABC""")

        for z,p in enumerate(dirr):
            if p.split('/')[6]=='test': continue
            # if p.split('/')[6]=='RA_min_error': continue

            shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[4])
            shrinkage_resize=[float(num) for num in shrinkage_resize]
            if shrinkage_resize==[1.1,1.1]:continue
            if 'double_spine_area' in p.split('/')[4]:
                double_spine_area='True'
            else:
                double_spine_area='False'
            spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[3])[0])
            from read_passive_parameters_csv import get_passive_parameter
            passive_vals_dict=get_passive_parameter(cell_name,double_spine_area=double_spine_area,shrinkage_resize=shrinkage_resize,spine_start=spine_start,fit_condition=p.split('/')[5],file_type='z_correct.swc')
            RA_CM_RM=get_passive_val(passive_vals_dict[p.split('/')[6]],what_return='nice_results')
            show_directory(ax[place[i]],p.split('/')[4]+p.split('/')[6]+'\n'+RA_CM_RM,p)

        plot_to_morphology_swc_too=False
        if plot_to_morphology_swc_too:
            fig=plt.figure()
            # plt.title(cell_name)
            try:
                ax = fig.subplot_mosaic("""ABC
                DEF
                GHI
                """)
            except:
                ax = fig.subplot_mosaic("""ABCD
                EFGH
                IJKL
                """)
            i=0

            # passive_vals_dict=get_passive_parameter(cell_name,shrinkage_resize=[shrinkage_by,resize_diam_by],fit_condition=fit_condition,spine_start=int(SPINE_START),file_type=file_type)
            if '4-5' in cell_name:
                same_diff=""
            else:
                if same==True:
                    same_diff='_same'
                else:
                    same_diff='_relative'
            for z,p in enumerate(glob(folder_+'/MOO_results_*'+same_diff+'*/morphology.swc/F_shrinkage=*/const_param/*/fit_transient_RDSM.png')):
                if p.split('/')[6]=='test': continue
                # RA,CM,RM=get_passive_val(passive_vals_dict[p.split('/')[6]])
                show_directory(ax[place[i]],p.split('/')[4]+p.split('/')[6],p)



    if compare_MOO_results:
        same=False
        if '4-5' in cell_name:
            sames=[True]
        else:
            sames=[True,False]
        for same in sames:
            if same==True:
                same_diff='same'
            else:
                same_diff='relative'
            # if '6-7' in cell_name:
            #     same_diff=''

            fig=plt.figure()
            # plt.title(cell_name)
            i=0
            ax = fig.subplot_mosaic("""ABCD
            EFGH
            IJKL""")
            # ax = fig.subplot_mosaic("""ABCD
            # EFGH
            # IJKL
            # MNOP""")
            # dirr_len=len(glob(folder_+'/MOO_results'+same_diff+'*/z_correct.swc_SPINE_START=*/F_shrinkage=*/const_param/*/fit_transient_RDSM.png'))
            # if dirr_len<10:
            #     ax = fig.subplot_mosaic("""ABC
            #     DEF
            #     GHI
            #     """)
            # elif dirr_len>=13:
            #     ax = fig.subplot_mosaic("""ABCD
            #     EFGH
            #     IJKL
            #     MNOP
            #     """)


            for z,p in enumerate(glob(folder_+'/MOO_results_*_'+same_diff+'*/z_correct.swc_SPINE_START=20/F_shrinkage*/const_param/*120*/*.pdf')):
                if p.split('/')[6]=='test': continue
                # if p.split('/')[6]=='RA_min_error': continue
                # if 'double' in p.split('/')[4]: continue
                # if p.split('/')[6]!='RA_min_error':continue
                shrinkage_resize=re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[4])
                shrinkage_resize=[float(num) for num in shrinkage_resize]
                # if shrinkage_resize!=[1.0,1.0]:continue
                if 'double_spine_area' in p.split('/')[4]:
                    double_spine_area='True'
                    continue
                else:
                    double_spine_area='False'
                print(p)
                spine_start=int(re.findall(r"[-+]?\d*\.\d+|\d+", p.split('/')[3])[0])
                from read_passive_parameters_csv import get_passive_parameter
                passive_vals_dict=get_passive_parameter(cell_name,double_spine_area=double_spine_area,shrinkage_resize=shrinkage_resize,spine_start=spine_start,fit_condition=p.split('/')[5],file_type='z_correct.swc')
                RA_CM_RM=get_passive_val(passive_vals_dict[p.split('/')[6]],what_return='nice_results')
                show_directory(ax[place[i]],p.split('/')[4]+p.split('/')[6]+'\n'+RA_CM_RM,p)


        plt.show()
    if compare_spine_start:
        pass
