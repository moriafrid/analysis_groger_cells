from plot_morphology_Yoni import plot_morph
from create_folder import create_folder_dirr
from read_spine_properties import get_n_spinese
from function_Figures import *
from matplotlib import pyplot as plt

if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p'):
        #if '4-3' in cell_name: continue
        before_after='_after_shrink'
        base_dir='final_data/'+cell_name+'/'
        save_dir='final_data/Figure1/'
        create_folder_dirr(save_dir)
        print(cell_name)
        fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
        fig.suptitle(cell_name, fontsize=30)# fig.set_figheight(6)
        # fig.set_figwidth(6)
        shapes = (2, 4)
        ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
        ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
        ax4 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

        # plt.subplots_adjust(hspace=0.3, wspace=0.3)

        decided_passive_params=find_RA(base_dir)
        # if cell_name in ['2017_03_04_A_6-7','2017_05_08_A_5-4']: decided_passive_params='RA_best_fit'
        plot_morph(ax1, cell_name, before_after,without_axons=True)

        if get_n_spinese(cell_name)>1:
            ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1, sharey=ax2)
            ax5 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
            plot_pickle(ax2,base_dir+'clear_short_pulse_after_peeling.p','clear_short_pulse')
            plot_short_pulse_model(ax3,glob(base_dir+decided_passive_params+'_pickles.p')[0])
            plot_syn_model2(ax4,glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0])
            # morph_path=glob("cells_initial_information/"+cell_name+'/*'+before_after+'.swc')[0]
            # dendogram=None
            # dendogram = Dendogram('dend_only', morph_path, add_sec2,load_func=load_swc,E_PAS=E_PAS,passive_val={"RM":parameters['RM'],"RA":parameters['RA'],"CM":parameters['CM']})
            # dendogram.cumpute_distances(dendogram.cell.soma)
            # max_y=dendogram.plot(base_dir,ax=ax4,title='',ylabel="distance from soma (um)")
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

            

        plt.savefig(save_dir+cell_name+'.png',dpi=500)
        plt.savefig(save_dir+cell_name+'.pdf',dpi=500)
        plt.savefig(save_dir+cell_name+'.svg',dpi=500)
        # pickle.dump(fig, open(save_dir+cell_name+'.p', 'wb'))  # cant work with scalebar
        plt.show()

