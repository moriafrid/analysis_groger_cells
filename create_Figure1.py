from plot_morphology_Yoni import plot_morph
from create_folder import create_folder_dirr
from read_spine_properties import get_n_spinese
from function_Figures import *
from matplotlib import pyplot as plt
import string
import sys
from open_pickle import read_from_pickle
if len(sys.argv)!=2:
    folder2run='final_data/total_moo'
    print("sys.argv not running" ,len(sys.argv),sys.argv)
else:
    folder2run=sys.argv[1]
print(folder2run)
if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p')[:]:
        # if cell_name!='2017_04_03_B':continue
        before_after='_after_shrink'
        #'final_data_after_shrink_with_mistak#
        base_dir=folder2run+'/'+cell_name+'/'
        save_dir=folder2run+'/Figure1/'
        create_folder_dirr(save_dir)
        print(cell_name)
        fig = plt.figure(figsize=(20, 10))  # , sharex="row", sharey="row"
        fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
        fig.subplots_adjust(left=0.01,right=0.99,top=0.94,bottom=0.05,hspace=0.01, wspace=0.05)
        # fig.set_figwidth(6)
        shapes = (2, 4)
        ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
        ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

        # plt.subplots_adjust(hspace=0.3, wspace=0.3)

        decided_passive_params=get_MOO_result_parameters(cell_name,'passive_parameter')[0]#find_RA(base_dir)
        # if cell_name in ['2017_03_04_A_6-7','2017_05_08_A_5-4']: decided_passive_params='RA_best_fit'
        if cell_name in read_from_pickle('cells_sec_from_picture.p'):
            from_picture=True
        else:
            from_picture=False
        plot_morph(ax1, cell_name, before_after,without_axons=True,from_picture=from_picture)

        if get_n_spinese(cell_name)>1:
            ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2)
            ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
            plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
            plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_pickles.p')[0])
            plot_syn_model2(ax4,glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0])
            plot_neck_voltage(ax5,glob(base_dir+'Voltage in neck_pickles*'+decided_passive_params+'.p')[0],start_point=970)
        else:
            ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2) # , sharex=ax2
            ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1, sharey=ax4) # , sharex=ax4
            plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
            plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_pickles.p')[0])
            plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')
            plot_syn_model(ax5,glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p')[0])

        # axs = axs.flat
        latter=['A','B','C','D','E']
        for n, ax in enumerate([ax1,ax2,ax3,ax4,ax5]):
        #string.ascii_uppercase[n]
            ax.text(-0.1, 0.9, string.ascii_uppercase[n], transform=ax.transAxes, size=25)

        plt.savefig(save_dir+cell_name+'.png')
        # plt.savefig(save_dir+cell_name+'.pdf')
        plt.savefig(save_dir+cell_name+'.svg')
        # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar
        plt.show()

