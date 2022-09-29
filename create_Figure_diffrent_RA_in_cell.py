import string
from glob import glob
from matplotlib import pyplot as plt
from add_figure import add_figure, adgust_subplot
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg, get_parameter, get_n_spinese, calculate_Rneck
from function_Figures import find_RA, legend_size, get_MOO_result_parameters, plot_pickle, plot_short_pulse_model, \
    plot_syn_model2, plot_syn_model
import sys
if len(sys.argv)!=2:
    save_folder='final_data/total_moo/'
    print("sys.argv not running" ,len(sys.argv))
else:
    save_folder=sys.argv[1]
save_dir=save_folder+'Figure7_RA_influence/'
create_folder_dirr(save_dir)
scatter_size=5

def create_fig_RA():
    fig1 = plt.figure(figsize=(18, 6))  # , sharex="row", sharey="row"
    shapes = (2, 5)
    fig1.subplots_adjust(left=0.05,right=0.90,top=0.85,bottom=0.1,hspace=0.1, wspace=0.2)
    # plt.title('cell_name')
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=2, colspan=2)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 3), rowspan=1, colspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(0, 4), colspan=1, rowspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(1, 2), rowspan=1, colspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)
    ax7 = plt.subplot2grid(shape=shapes, loc=(1, 4), colspan=1, rowspan=1)
    for n, ax in enumerate([ax1,ax2,ax3,ax4,ax5,ax6,ax7]):
        #string.ascii_uppercase[n]
        ax.text(-0.2, 0.9, string.ascii_uppercase[n], transform=ax.transAxes, size=20)
    return [fig1, ax1,ax2,ax3,ax4,ax5,ax6,ax7]
def plot_passsive(ax1,ax2,decided_passive_params,base_dir0):
    base_dir=base_dir0+decided_passive_params+'/'
    plot_short_pulse_model(ax1,glob(base_dir+decided_passive_params+'_pickles.p')[0],show_legend=False,text_place=[-0.2,1.02])
    if get_n_spinese(cell_name)==2:
        plot_syn_model2(ax2,glob(base_dir+'AMPA&NMDA_soma_seperete_pickles*_relative_'+decided_passive_params+'.p')[0],bbox_to_anchor=(1.25,0.1))
    else:
        plot_syn_model(ax2,glob(base_dir+'AMPA&NMDA_soma_pickles_*'+decided_passive_params+'.p')[0],show_legend=False)
colors=['red','blue']
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name!='2017_02_20_B':continue
    fig,ax1,ax2,ax3,ax4,ax5,ax6,ax7=create_fig_RA()
    adgust_subplot(ax2,'','','AMPA [nS]',bottom_visiability=False)
    adgust_subplot(ax5,'' ,'RA','NMDA [nS]')
    base_dir=save_folder+'/'+cell_name+'/'
    plot_pickle(ax1,base_dir+"RA const against errors2.p")
    # for passive_parameter in ['RA_min_error','RA=300','RA_best_fit']:
    plot_passsive(ax3,ax4,find_RA(base_dir),base_dir)
    if cell_name in ['2016_04_16_A','2017_05_08_A_4-5']:
        plot_passsive(ax6,ax7,'RA=200',base_dir)
    else:
        plot_passsive(ax6,ax7,'RA=300',base_dir)
    for num in range(get_n_spinese(cell_name)):
        dictMOO={'syn_num':num,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        plot_dict={'color':colors[num],'label':cell_name,'lw':scatter_size-2}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        ax2.scatter(RA,W_AMPA,**plot_dict)
        ax5.scatter(RA,W_NMDA,**plot_dict)
    plt.savefig(save_dir+cell_name+'RA.png')
    plt.savefig(save_dir+cell_name+'RA.svg')
    # plt.show()


passive_parameter_names=['RA=70','RA_min_error','RA_best_fit','RA=100','RA=120']

fig1 = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
shapes = (5, 4)
fig1.subplots_adjust(left=0.1,right=0.95,top=0.95,bottom=0.05,hspace=0.27, wspace=0.22)
colors=['red','blue']
ax0_0 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 1), rowspan=1, colspan=1)
ax1_0 = plt.subplot2grid(shape=shapes, loc=(0, 2), rowspan=1, colspan=1)
ax1_1 = plt.subplot2grid(shape=shapes, loc=(0, 3), rowspan=1, colspan=1)
ax2_0 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
ax2_1 = plt.subplot2grid(shape=shapes, loc=(1, 1), rowspan=1, colspan=1)
ax3_0 = plt.subplot2grid(shape=shapes, loc=(1, 2), rowspan=1, colspan=1)
ax3_1 = plt.subplot2grid(shape=shapes, loc=(1, 3), rowspan=1, colspan=1)
ax4_0 = plt.subplot2grid(shape=shapes, loc=(2, 0), rowspan=1, colspan=1)
ax4_1 = plt.subplot2grid(shape=shapes, loc=(2, 1), rowspan=1, colspan=1)
ax5_0 = plt.subplot2grid(shape=shapes, loc=(2, 2), rowspan=1, colspan=1)
ax5_1 = plt.subplot2grid(shape=shapes, loc=(2, 3), rowspan=1, colspan=1)
ax6_0 = plt.subplot2grid(shape=shapes, loc=(3, 0), rowspan=1, colspan=1)
ax6_1 = plt.subplot2grid(shape=shapes, loc=(3, 1), rowspan=1, colspan=1)
ax7_0 = plt.subplot2grid(shape=shapes, loc=(3, 2), rowspan=1, colspan=1)
ax7_1 = plt.subplot2grid(shape=shapes, loc=(3, 3), rowspan=1, colspan=1)
ax8_0 = plt.subplot2grid(shape=shapes, loc=(4, 0), rowspan=1, colspan=1)
ax8_1 = plt.subplot2grid(shape=shapes, loc=(4, 1), rowspan=1, colspan=1)
ax9_0 = plt.subplot2grid(shape=shapes, loc=(4, 2), rowspan=1, colspan=1)
ax9_1 = plt.subplot2grid(shape=shapes, loc=(4, 3), rowspan=1, colspan=1)


for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    ax=eval('ax'+str(i)+'_0')
    print(ax)
    if i>=8:
        bottom_title='RA'
        bottom_visiability=True
    else:
        bottom_title=''
        bottom_visiability=False
    adgust_subplot(eval('ax'+str(i)+'_0'),cell_name,bottom_title,'AMPA [nS]',bottom_visiability=bottom_visiability,titlesize=20,latter=string.ascii_uppercase[i])
    adgust_subplot(eval('ax'+str(i)+'_1'),'' ,bottom_title,'NMDA [nS]',bottom_visiability=bottom_visiability,titlesize=20)

    for num in range(get_n_spinese(cell_name)):
        dictMOO={'syn_num':num,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        plot_dict={'color':colors[num],'label':PSD[num],'lw':scatter_size-2}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        eval('ax'+str(i)+'_0').scatter(RA,W_AMPA,**plot_dict)
        eval('ax'+str(i)+'_1').scatter(RA,W_NMDA,**plot_dict)
        eval('ax'+str(i)+'_1').legend()

plt.savefig(save_dir+'AMPA_NMDA_RA.png')
plt.savefig(save_dir+'AMPA_NMDA_RA.svg')
# plt.show()
