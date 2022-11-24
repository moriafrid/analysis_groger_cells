from glob import glob
from matplotlib import pyplot as plt, image as mpimg
from pdf2image import convert_from_path
from add_figure import add_figure, adgust_subplot
from cell_properties import diam_distance_plot
from check_dynamics import check_dynamics
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
import sys


if len(sys.argv)!=2:
    save_folder='final_data/total_moo/'
    print("sys.argv not running" ,len(sys.argv))
else:
    save_folder=sys.argv[1]
save_dir=save_folder+'Figure8_check_dinamic_diam_dis/'
create_folder_dirr(save_dir)
latter=['A','B','C','D','E','F','G','H','I','J']

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

if __name__=='__main__':
    fig2 = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    fig2.subplots_adjust(left=0.05,right=0.95,top=0.95,bottom=0.05,hspace=0.001 ,wspace=0.001)
    shapes = (3, 4)
    ax0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), rowspan=1, colspan=1)
    ax7 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
    ax8 = plt.subplot2grid(shape=shapes, loc=(2, 1), rowspan=1, colspan=1)
    ax9 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)
    file_type2read= 'morphology_z_correct.swc'
    save_dir = "cells_outputs_data_short"

    for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
        adgust_subplot(eval('ax'+str(i)),cell_name,'dis','diam',latter=latter[i],xlatter=-0.01,ylatter=1)
        folder_save=save_dir+'/'+cell_name+'/data/cell_properties/'+file_type2read+'/diam_dis/'
        show_directory(eval('ax'+str(i)), title="",png_file=folder_save+'diam-dis.png')

        # diam_distance_plot(cell_name,file_type2read,ax=eval('ax'+str(i)),data_dir= "cells_initial_information",save_fig=False)
    plt.savefig(save_folder+'/diam-dis.png')
    plt.show()

    fig2 = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    fig2.subplots_adjust(left=0.1,right=0.95,top=0.9,bottom=0.1,hspace=0.5 ,wspace=0.25)
    shapes = (3, 4)
    ax0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), rowspan=1, colspan=1)
    ax7 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
    ax8 = plt.subplot2grid(shape=shapes, loc=(2, 1), rowspan=1, colspan=1)
    ax9 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)
    for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
        if i==3:
            plot_legend=True
        else:
            plot_legend=False
        adgust_subplot(eval('ax'+str(i)),cell_name,'[s]','[mV]',latter=latter[i],titlesize=18)
        check_dynamics(cell_name, save_folder,ax=eval('ax'+str(i)),save_fig=False,plot_legend=plot_legend)
    plt.savefig(save_folder+'/check_dinamic.png')
    # plt.show()


    # plt.savefig(save_folder+'/diam-dis.svg')







