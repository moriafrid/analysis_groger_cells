from plot_morphology_Yoni import plot_morph
from create_folder import create_folder_dirr
from read_spine_properties import get_n_spinese
from function_Figures import *
import sys
from glob import glob
if len(sys.argv)!=2:
    folder2run='final_data/total_moo'
    print("sys.argv not running" ,len(sys.argv))
else:
    folder2run=sys.argv[1]
print(folder2run)
if folder2run=='':
    run_all=True
else:
    run_all=False
if __name__=='__main__':
    before_after='_after_shrink'
    # save_dir=folder2run+'/Figure2/'
    # print(cell_name)



    fig = plt.figure(figsize=(12, 15))  # , sharex="row", sharey="row"
    fig.subplots_adjust(left=0.15,right=0.90,top=0.95,bottom=0.02,hspace=0.2, wspace=0.01)
    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (5, 3)

    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax1_0.text(-0.2, 1.05, 'A', transform=ax1_0.transAxes, size=22,weight="bold")
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax4_0 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax1_1.text(-0.2, 1.05, 'B', transform=ax1_1.transAxes, size=22,weight="bold")
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
    ax1_2.text(-0.2, 1.05, 'C', transform=ax1_2.transAxes, size=22,weight="bold")
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
    ax3_2 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)

    ax1_3 = plt.subplot2grid(shape=shapes, loc=(3, 0), rowspan=1, colspan=1)
    ax1_3.text(-0.2, 1.05, 'D', transform=ax1_3.transAxes, size=22,weight="bold")
    ax2_3 = plt.subplot2grid(shape=shapes, loc=(3, 1), colspan=1, rowspan=1)
    ax3_3 = plt.subplot2grid(shape=shapes, loc=(3, 2), colspan=1, rowspan=1)


    ax1_4 = plt.subplot2grid(shape=shapes, loc=(4, 0), rowspan=1, colspan=1)
    ax1_4.text(-0.2, 1.05, 'E', transform=ax1_4.transAxes, size=22,weight="bold")
    ax2_4 = plt.subplot2grid(shape=shapes, loc=(4, 1), colspan=1, rowspan=1)
    ax3_4 = plt.subplot2grid(shape=shapes, loc=(4, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
    i=0
    for cell_name in read_from_pickle('cells_with_2_syn.p'):
        if '2016_05_12_A'==cell_name:continue
        
        eval('ax2_'+str(i)).title.set_text(cell_name)

        if cell_name in read_from_pickle('cells_sec_from_picture.p'):
            from_picture=True
        else:
            from_picture=False        
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
            elif 'syn_from_picture' in folder2run:
               from_picture=True
        create_folder_dirr(save_dir)

        base_dir=folder2run+'/'+cell_name+'/'
        decided_passive_params=get_MOO_result_parameters(cell_name,'passive_parameter')[0]#find_RA(base_dir)
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture,bbox_to_anchor=(0,1),compressed_informtion=True,legend_size=10,change_diam=2)
        print(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')
        plot_syn_model2(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(0.8 ,0.23),legend_size=11,compress_legend=True)
        # plot_syn_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage Spine&Soma_pickles*_relative_'+decided_passive_params+'.p')[0])
        plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(0.9,0.2),legend_size=9)
        i+=1
    plt.savefig(save_dir+'0.svg')
    plt.savefig(save_dir+'0.pdf')
    plt.savefig(save_dir+'0.png')
    # plt.show()

    fig = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    fig.subplots_adjust(left=0.05,right=0.95,top=0.95,bottom=0.05,hspace=0.2, wspace=0.1)

    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (2, 4)
    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax1_0.text(-0.1, 1, 'A', transform=ax1_0.transAxes, size=22,weight="bold")

    # ax1_1 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax2_1 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
    # ax1_1.text(-0.1, 1, 'B', transform=ax1_1.transAxes, size=22,weight="bold")

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(0, 2), rowspan=1, colspan=1)
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
    ax1_1.text(-0.1, 1, 'B', transform=ax1_1.transAxes, size=22,weight="bold")

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    ax1_2.text(-0.1, 1, 'C', transform=ax1_2.transAxes, size=22,weight="bold")

    i=0
    for cell_name in read_from_pickle('cells_name2.p'):
        if cell_name in read_from_pickle('cells_with_2_syn.p'):continue
        if cell_name=='2017_05_08_A_4-5':continue
        print(i)
        eval('ax1_'+str(i)).title.set_text(cell_name)

        if cell_name in read_from_pickle('cells_sec_from_picture.p'):
            from_picture=True
        else:
            from_picture=False
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
        base_dir=folder2run+'/'+cell_name+'/'
        # if '4-3' in cell_name: continue
        print(cell_name)
        decided_passive_params=get_MOO_result_parameters(cell_name,'passive_parameter')[0]#find_RA(base_dir)
        if i<2:
            bbox_to_anchor=(1.3,1)
            xlabel=-0.1
            ylabel=-0.02
        else:
            bbox_to_anchor=(1.2,1)
            xlabel=-0.1
            ylabel=1
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture,bbox_to_anchor=bbox_to_anchor,compressed_informtion=True)
        print(decided_passive_params)
        print(base_dir)
        print(glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p'))
        plot_syn_model(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p')[0],show_legend=False,xlabel=-0.1,ylabel=-0.02)
        i+=1

    plt.savefig(save_dir+'3.svg')
    plt.savefig(save_dir+'3.pdf')
    plt.savefig(save_dir+'3.png')
    # plt.show()


    fig = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
    fig.subplots_adjust(left=0.1,right=0.90,top=0.9,bottom=0.1,hspace=0.05, wspace=0.05)
    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (3, 3)

    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax1_0.text(-0.2, 1.05, 'A', transform=ax1_0.transAxes, size=22,weight="bold")
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax4_0 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax1_1.text(-0.2, 1.05, 'B', transform=ax1_1.transAxes, size=22,weight="bold")
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
    ax1_2.text(-0.2, 1.05, 'C', transform=ax1_2.transAxes, size=22,weight="bold")
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
    ax3_2 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)

    for i,cell_name in enumerate(read_from_pickle('cells_with_2_syn.p')[:3]):
        eval('ax2_'+str(i)).title.set_text(cell_name)

        if cell_name in read_from_pickle('cells_sec_from_picture.p'):
            from_picture=True
        else:
            from_picture=False        
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
            elif 'syn_from_picture' in folder2run:
               from_picture=True
        create_folder_dirr(save_dir)

        base_dir=folder2run+'/'+cell_name+'/'
        decided_passive_params=get_MOO_result_parameters(cell_name,'passive_parameter')[0]#find_RA(base_dir)
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture,bbox_to_anchor=(1.0,1.1))
        print(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')
        plot_syn_model2(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(1.15,0.1))
        # plot_syn_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage Spine&Soma_pickles*_relative_'+decided_passive_params+'.p')[0])
        plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(1.1,0.15))
    plt.savefig(save_dir+'1.svg')
    plt.savefig(save_dir+'1.pdf')
    plt.savefig(save_dir+'1.png')

    fig = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
    fig.subplots_adjust(left=0.1,right=0.90,top=0.9,bottom=0.1,hspace=0.05, wspace=0.05)

    # fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
    # fig.set_figwidth(6)
    shapes = (3, 3)
    ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax1_0.text(-0.2, 1.05, 'A', transform=ax1_0.transAxes, size=22,weight="bold")
    ax2_0 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    # ax4_0 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)

    ax1_1 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax1_1.text(-0.2, 1.05, 'B', transform=ax1_1.transAxes, size=22,weight="bold")
    ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    # ax4_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

    ax1_2 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
    ax1_2.text(-0.2, 1.05, 'C', transform=ax1_2.transAxes, size=22,weight="bold")
    ax2_2 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
    ax3_2 = plt.subplot2grid(shape=shapes, loc=(2, 2), colspan=1, rowspan=1)
    # ax4_2 = plt.subplot2grid(shape=shapes, loc=(2, 3), colspan=1, rowspan=1)

    for i,cell_name in enumerate(read_from_pickle('cells_with_2_syn.p')[3:6]):
        eval('ax2_'+str(i)).title.set_text(cell_name)

        if cell_name in read_from_pickle('cells_sec_from_picture.p'):
            from_picture=True
        else:
            from_picture=False        
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
            elif 'syn_from_picture' in folder2run:
               from_picture=True
        base_dir=folder2run+'/'+cell_name+'/'
        decided_passive_params=get_MOO_result_parameters(cell_name,'passive_parameter')[0]#find_RA(base_dir)
        plot_morph(eval('ax1_'+str(i)), cell_name, before_after,without_axons=True,from_picture=from_picture,bbox_to_anchor=(1.0,1.1))
        plot_syn_model2(eval('ax2_'+str(i)),glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(1.15,0.1))
        # plot_syn_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage Spine&Soma_pickles*_relative_'+decided_passive_params+'.p')[0])
        print(glob(base_dir+'Voltage in neck_pickles*'+decided_passive_params+'.p')[0])
        plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*'+decided_passive_params+'.p')[0],start_point=970,bbox_to_anchor=(1.1,0.15))
        #plot_neck_voltage(eval('ax3_'+str(i)),glob(base_dir+'Voltage in neck_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(1.1,0.15))

    plt.savefig(save_dir+'2.svg')
    plt.savefig(save_dir+'2.pdf')
    plt.savefig(save_dir+'2.png')
    # plt.show()



