from plot_morphology_Yoni import plot_morph
from create_folder import create_folder_dirr
from read_spine_properties import get_n_spinese
from function_Figures import *
import sys
if sys.argv!=2:
    folder2run='final_data/correct_seg_syn_from_picture'
    folder2run=''
else:
    folder2run=sys.argv[1]
if folder2run=='':
    run_all=True
else:
    run_all=False
if __name__=='__main__':
    before_after='_after_shrink'
    # save_dir=folder2run+'/Figure2/'
    # print(cell_name)
    fig = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (3, 3)
    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax4_0 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
    ax3_2 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)
    # ax4_2 = plt.subplot2grid(shape=shapes, loc=(2, 3), colspan=1, rowspan=1)

    # plt.subplots_adjust(hspace=0.3, wspace=0.3)
    for i,cell_name in enumerate(read_from_pickle('cells_with_2_syn.p')[:3]):
        if run_all:
            if cell_name in read_from_pickle('cells_sec_from_picture.p'): #cell that taken from picture
                folder2run='final_data/correct_seg_syn_from_picture'
                from_picture=True
            else:#cell that coming from xyz searching
                folder2run='final_data/correct_seg_find_syn_xyz'
                from_picture=False
            save_dir='final_data/Figure2/' #orgenize the cell to taken from evereywhre I want
        else:
            save_dir=folder2run+'/Figure2/'
            if 'syn_xyz' in folder2run:
               from_picture=False
            else:
               from_picture=True
        create_folder_dirr(save_dir)

        base_dir=folder2run+'/'+cell_name+'/'
        decided_passive_params=find_RA(base_dir)
        if cell_name in ['2017_03_04_A_6-7','2017_05_08_A_5-4']: decided_passive_params='RA_best_fit'
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture)

        plot_syn_model2(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0])
        # plot_syn_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage Spine&Soma_pickles*_relative_'+decided_passive_params+'.p')[0])
        plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*_relative_'+decided_passive_params+'.p')[0])
        # plt.show()
    plt.savefig(save_dir+'1.svg')
    plt.savefig(save_dir+'1.pdf')
    plt.savefig(save_dir+'1.png')
    # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar

    fig = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (3, 3)
    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax4_0 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
    ax3_2 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)
    # ax4_2 = plt.subplot2grid(shape=shapes, loc=(2, 3), colspan=1, rowspan=1)

    for i,cell_name in enumerate(read_from_pickle('cells_with_2_syn.p')[3:6]):
        if run_all:
            if cell_name in read_from_pickle('cells_sec_from_picture.p'): #cell that taken from picture
                folder2run='final_data/correct_seg_syn_from_picture'
                from_picture=True
            else:#cell that coming from xyz searching
                folder2run='final_data/correct_seg_find_syn_xyz'
                from_picture=False
            save_dir='final_data/Figure2/' #orgenize the cell to taken from evereywhre I want
        else:
            save_dir=folder2run+'/Figure2/'
            if 'syn_xyz' in folder2run:
               from_picture=False
            else:
               from_picture=True
        base_dir=folder2run+'/'+cell_name+'/'
        decided_passive_params=find_RA(base_dir)
        # if cell_name in ['2017_03_04_A_6-7','2017_05_08_A_5-4']: decided_passive_params='RA_best_fit'

        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture)
        plot_syn_model2(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0])
        # plot_syn_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage Spine&Soma_pickles*_relative_'+decided_passive_params+'.p')[0])
        plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*_relative_'+decided_passive_params+'.p')[0])

    plt.savefig(save_dir+'2.svg')
    plt.savefig(save_dir+'2.pdf')
    plt.savefig(save_dir+'2.png')


    fig = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (2, 4)
    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax1_1 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
    ax1_2 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax1_3 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    ax2_3 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
    i=0
    for cell_name in read_from_pickle('cells_name2.p'):
        if cell_name in read_from_pickle('cells_with_2_syn.p'):continue
        if run_all:
            if cell_name in read_from_pickle('cells_sec_from_picture.p'): #cell that taken from picture
                folder2run='final_data/correct_seg_syn_from_picture'
                from_picture=True
            else:#cell that coming from xyz searching
                folder2run='final_data/correct_seg_find_syn_xyz'
                from_picture=False
            save_dir='final_data/Figure2/' #orgenize the cell to taken from evereywhre I want
        else:
            save_dir=folder2run+'/Figure2/'
            if 'syn_xyz' in folder2run:
               from_picture=False
            else:
               from_picture=True
        base_dir=folder2run+'/'+cell_name+'/'
        # if '4-3' in cell_name: continue
        print(cell_name)
        decided_passive_params=find_RA(base_dir)
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture)
        plot_syn_model(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p')[0])
        i+=1

    plt.savefig(save_dir+'3.svg')
    plt.savefig(save_dir+'3.pdf')
    plt.savefig(save_dir+'3.png')
    # plt.show()
