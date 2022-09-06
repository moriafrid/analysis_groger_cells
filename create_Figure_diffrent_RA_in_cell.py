import pandas as pd
from matplotlib import pyplot as plt
from add_figure import add_figure, adgust_subplot
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg, get_parameter, get_n_spinese, calculate_Rneck
from function_Figures import find_RA, legend_size, get_MOO_result_parameters
import numpy as np
import string
import sys
if len(sys.argv)!=2:
    save_folder='final_data/total_moo/'
    print("sys.argv not running" ,len(sys.argv))
else:
    save_folder=sys.argv[1]
save_dir=save_folder+'Figure_5/'
create_folder_dirr(save_dir)
scatter_size=8
passive_parameter_names=['RA_min_error','RA_best_fit','RA=100','RA=120']

fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
shapes = (1, 2)
fig1.subplots_adjust(left=0.1,right=0.90,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax0_1,'gmax AMPA diffrent Ra' ,'PSD','gmax AMPA [nS]')
adgust_subplot(ax0_2,'gmax NMDA diffrent Ra','PSD','gmax NMDA [nS]')
all_AMPA,all_NMDA,all_PSD=[],[],[]
all_AMPA=np.zeros(1,9)
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')[:]):
    if cell_name=='2017_04_03_B':continue

    plot_dict={'color':colors[i],'lw':scatter_size-2}
    # for num in range(get_n_spinese(cell_name)):
    dictMOO={'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
    PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
    RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
    W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
    W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
    index2del1=np.unique(list(np.where(W_AMPA>7)[0])+list(np.where(W_NMDA>1.5)[0]))
    index2del=[]
    if len(index2del1)>0:
        deleteRA=' delete RA '+str(RA[index2del1])
        if get_n_spinese(cell_name)==2:
            for t in index2del1:
                if (t % 2) != 0 and t-1 not in index2del1:
                    # index2del.append(int((t-1)/2))
                    index2del.append(t-1)

                index2del.append(t)
        else:
            index2del=index2del1
    else:
        deleteRA=''
    PSD=np.delete(PSD,index2del)
    W_AMPA=np.delete(W_AMPA,index2del)
    W_NMDA=np.delete(W_NMDA,index2del)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,W_NMDA,**plot_dict,label=cell_name+deleteRA)

    ax0_2.legend(loc="upper right", bbox_to_anchor=(1.2, 1),prop={'size': legend_size-2})
    all_AMPA[i]=W_AMPA
    # all_AMPA=np.append(all_AMPA, [W_AMPA])
    all_NMDA=np.append(all_NMDA, W_NMDA)
    all_PSD=np.append(all_PSD, PSD)
df = pd.DataFrame(all_AMPA, columns=[read_from_pickle('cells_sec_from_picture.p')])
df.plot.box()
plt.savefig(save_dir+'/AMPA_NMDA_PSD_all_make_sense.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_all_make_sense.svg')
# plt.show()

fig1 = plt.figure(figsize=(15, 15))  # , sharex="row", sharey="row"
shapes = (5, 5)
fig1.subplots_adjust(left=0.05,right=0.90,top=0.85,bottom=0.1,hspace=0.01, wspace=0.2)
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
    adgust_subplot(eval('ax'+str(i)+'_0'),'gmax AMPA [nS]','RA','gmax AMPA [nS]')
    adgust_subplot(eval('ax'+str(i)+'_1'),'gmax NMDA [nS]' ,'RA','gmax NMDA [nS]')

    for num in range(get_n_spinese(cell_name)):
        dictMOO={'syn_num':num,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        plot_dict={'color':colors[num],'label':cell_name,'lw':scatter_size-2}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        eval('ax'+str(i)+'_'+str(num)).scatter(RA,W_AMPA,**plot_dict)
        eval('ax'+str(i)+'_'+str(num)).scatter(RA,W_NMDA,**plot_dict)
    plt.savefig(save_dir+'AMPA_NMDA_RA.png')
    plt.savefig(save_dir+'AMPA_NMDA_RA.svg')

plt.show()

colors=['red','blue']
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    fig1 = plt.figure(figsize=(18, 6))  # , sharex="row", sharey="row"
    shapes = (1, 2)
    fig1.subplots_adjust(left=0.05,right=0.90,top=0.85,bottom=0.1,hspace=0.01, wspace=0.2)
    fig1.set_title('cell_name')
    ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    adgust_subplot(ax0_1,'Dependency of AMPA by RA' ,'RA','gmax AMPA [nS]')
    adgust_subplot(ax0_2,'Dependency of NMDA by RA','RA','gmax NMDA [nS]')
    for num in range(get_n_spinese(cell_name)):
        dictMOO={'syn_num':num,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        plot_dict={'color':colors[num],'label':cell_name,'lw':scatter_size-2}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        ax0_1.scatter(RA,W_AMPA,**plot_dict)
        ax0_2.scatter(RA,W_NMDA,**plot_dict)
    plt.savefig(save_dir+cell_name+'_AMPA_NMDA_RA.png')
    plt.savefig(save_dir+cell_name+'_AMPA_NMDA_RA.svg')

plt.show()

fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
shapes = (1, 2)
fig1.subplots_adjust(left=0.1,right=0.90,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax0_1,'gmax AMPA diffrent Ra' ,'PSD','gmax AMPA [nS]')
adgust_subplot(ax0_2,'gmax NMDA diffrent Ra','PSD','gmax NMDA [nS]')
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    # for num in range(get_n_spinese(cell_name)):
    dictMOO={'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
    PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
    RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
    W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
    W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,W_NMDA,**plot_dict)
    ax0_2.legend()
plt.savefig(save_dir+'/AMPA_NMDA_PSD_all.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_all.svg')



# for n, ax in enumerate([ax0_1,ax0_2,ax0_3]):
#     ax.text(-0.1, 1.1, string.ascii_uppercase[n], transform=ax.transAxes, size=25)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
