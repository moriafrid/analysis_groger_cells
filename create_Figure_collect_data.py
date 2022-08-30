from dendogram_function import func_dendogram
from plot_morphology_Yoni import plot_morph
from create_folder import create_folder_dirr
from read_spine_properties import get_n_spinese
import string
import sys
from function_Figures import *

if sys.argv!=3:
    cell_name=read_from_pickle('cells_name2.p')[0]
    folder2run='final_data/correct_seg_syn_from_picture'
    print("sys.argv isn't run")
else:
    cell_name=sys.argv[1]
    folder2run=sys.argv[2]

if __name__=='__main__':
    #if '4-3' in cell_name: continue
    before_after='_after_shrink'
    base_dir=folder2run+'/'+cell_name+'/'
    save_dir=folder2run+'/Figure4/'
    create_folder_dirr(save_dir)
    print(cell_name)
    fig = plt.figure(figsize=(22, 8))  # , sharex="row", sharey="row"
    fig.suptitle(cell_name, fontsize=40)# fig.set_figheight(6)
    # plt.rcParams.update({'font.size': 50})
    # fig.set_figwidth(6)
    shapes = (2, 5)
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

    ax6 = plt.subplot2grid(shape=shapes, loc=(0, 4), colspan=1, rowspan=1)
    ax7 = plt.subplot2grid(shape=shapes, loc=(1, 4), colspan=1, rowspan=1)
    # plt.subplots_adjust(hspace=0.3, wspace=0.3)
    decided_passive_params=find_RA(base_dir)
    if 'syn_xyz' in folder2run:
        from_picture=False
    else:
        from_picture=True
    plot_morph(ax1, cell_name, before_after,without_axons=True,from_picture=from_picture)

    if get_n_spinese(cell_name)>1:
        ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2)
        ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
        plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
        plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_pickles.p')[0])
        plot_syn_model2(ax4,glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0])
        # plot_pickle(ax5,glob(base_dir+'Voltage Spine&Soma_full_relative_'+decided_passive_params+'.p')[0])
        # plot_syn_voltage(ax5,glob(base_dir+'Voltage Spine&Soma_pickles*relative_'+decided_passive_params+'.p')[0])
        plot_neck_voltage(ax5,glob(base_dir+'Voltage in neck_pickles*'+decided_passive_params+'.p')[0])
    else:
        ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2) # , sharex=ax2
        ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1, sharey=ax4) # , sharex=ax4
        plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
        plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_pickles.p')[0])
        plot_pickle(ax4,base_dir+'clear_syn_after_peeling.p','clear_syn')
        plot_syn_model(ax5,glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p')[0])

    plot_pickle(ax6,base_dir+"RA const against errors2.p")
    func_dendogram(ax7,glob(base_dir+'Rins_pickles_*'+decided_passive_params+'.p')[0])

    for n, ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6,ax7]):
        ax.text(-0.1, 0.9, string.ascii_uppercase[n], transform=ax.transAxes,
                size=20, weight='bold')
    # for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7]:
    #     ax.legend(fontsize=8, loc='best')
        # for child in ax.get_children():
        #     if isinstance(child, matplotlib.text.Annotation):
        #         # pass
        #         child.fontsize=50 # and do something
    # plt.show()

    plt.savefig(save_dir+cell_name+'.png')
    plt.savefig(save_dir+cell_name+'.pdf')
    plt.savefig(save_dir+cell_name+'.svg')
    plt.show()


    # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar
