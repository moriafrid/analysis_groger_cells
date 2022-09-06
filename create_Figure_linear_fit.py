from matplotlib import pyplot as plt
from add_figure import add_figure, adgust_subplot
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg, get_parameter, get_n_spinese, calculate_Rneck
from function_Figures import find_RA, legend_size, get_MOO_result_parameters
from glob import glob
import numpy as np
import string
import sys
from scipy.optimize import curve_fit
if len(sys.argv)!=2:
    save_folder='final_data/total_moo/'
    print("sys.argv not running" ,len(sys.argv))
else:
    save_folder=sys.argv[1]
save_dir=save_folder+'Figure6_AMPA_NMDA_linear_fit/'
create_folder_dirr(save_dir)
scatter_size=8
passive_parameter_names=['RA_min_error','RA_best_fit','RA=100','RA=120']
# def linear_fit(x, a, c):
#     return a*x+c
def linear_fit(x, a):
    return a*x
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
fig2 = plt.figure(figsize=(10, 15))  # , sharex="row", sharey="row"
shapes = (3, 2)
fig2.subplots_adjust(left=0.15,right=0.95,top=0.9,bottom=0.1,hspace=0.15, wspace=0.2)
plt.title('RA min error Rneck against AMPA and NMDA')
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 1), rowspan=1, colspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(2, 0), colspan=1, rowspan=1)
ax6 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)

adgust_subplot(ax1,'AMPA','','Rin [Mohm]',bottom_visiability=False)
adgust_subplot(ax2,'NMDA' ,'','Rin [Mohm]',bottom_visiability=False)
adgust_subplot(ax3,'','','Rin spine [Mohm]',bottom_visiability=False)
adgust_subplot(ax4,'','','Rin spine [Mohm]',bottom_visiability=False)
adgust_subplot(ax5,'','gmax AMPA [nS]' ,'Rneck [Mohm]')
adgust_subplot(ax6,'','gmax NMDa [nS]','Rneck [Mohm]')
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    j=0
    W_AMPA=[]
    while len(W_AMPA)==0:
        print(W_AMPA)
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        Rneck=get_MOO_result_parameters(cell_name,'Rneck',**dictMOO)
        Rin_spine=get_MOO_result_parameters(cell_name,'spine_head_Rin',**dictMOO)
        Rin_soma=get_MOO_result_parameters(cell_name,'soma_Rin',**dictMOO)
        j+=1
    ax1.scatter(W_AMPA,Rin_soma,**plot_dict)
    ax2.scatter(W_NMDA,Rin_soma,**plot_dict)
    ax3.scatter(W_AMPA,Rin_spine,**plot_dict)
    ax4.scatter(W_NMDA,Rin_spine,**plot_dict)
    ax5.scatter(W_AMPA,Rneck,**plot_dict)
    ax6.scatter(W_NMDA,Rneck,**plot_dict)
plt.savefig(save_dir+'/Resistance-Conductance.png')
plt.savefig(save_dir+'/Resistance-Conductance.svg')
plt.show()


fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
shapes = (1, 2)
fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
plt.title('RA=100')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax0_1,'AMPA g_max' ,'PSD','gmax AMPA [nS]')
adgust_subplot(ax0_2,'NMDA g_max','PSD','gmax NMDA [nS]')
all_AMPA,all_NMDA,all_PSD=[],[],[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    W_AMPA=[]
    j=2
    while len(W_AMPA)==0:
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)

        j+=1
        print(W_AMPA)
    all_AMPA=np.append(all_AMPA, W_AMPA)
    all_NMDA=np.append(all_NMDA, W_NMDA)
    all_PSD=np.append(all_PSD, PSD)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,W_NMDA,**plot_dict)
ax0_2.legend()
x_data=np.arange(0,max(all_PSD)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_PSD, all_AMPA)
ax0_1.plot(x_data, linear_fit(x_data, *popt1), '-')
ax0_1.text(0.05,0.9,'g_density='+str(round(popt1[0],2)),transform=ax0_1.transAxes)
popt2, pcov2 = curve_fit(linear_fit, all_PSD, all_NMDA)
ax0_2.plot(x_data, linear_fit(x_data, *popt2), '-')
ax0_2.text(0.5,0.9,'g_density='+str(round(popt2[0],2)),transform=ax0_2.transAxes)
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=100.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=100.svg')
# plt.show()

fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
shapes = (1, 2)
plt.title('RA_min_error')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax0_1,'AMPA g_max' ,'PSD','gmax AMPA [nS]')
adgust_subplot(ax0_2,'NMDA g_max','PSD','gmax NMDA [nS]')

for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    W_AMPA=[]
    j=0
    while len(W_AMPA)==0:
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        distance=get_MOO_result_parameters(cell_name,'distance',**dictMOO)
        j+=1
        print(W_AMPA)
    all_AMPA=np.append(all_AMPA, W_AMPA)
    all_NMDA=np.append(all_NMDA, W_NMDA)
    all_PSD=np.append(all_PSD, PSD)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,W_NMDA,**plot_dict)


ax0_2.legend()
x_data=np.arange(0,max(all_PSD)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_PSD, all_AMPA)
ax0_1.plot(x_data, linear_fit(x_data, *popt1), '-')
ax0_1.text(0.05,0.9,'g_density='+str(round(popt1[0],2)),transform=ax0_1.transAxes)
popt2, pcov2 = curve_fit(linear_fit, all_PSD, all_NMDA)
ax0_2.plot(x_data, linear_fit(x_data, *popt2), '-')
ax0_2.text(0.5,0.9,'g_density='+str(round(popt2[0],2)),transform=ax0_2.transAxes)

plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.svg')
# plt.show()


fig1 = plt.figure(figsize=(16, 6))  # , sharex="row", sharey="row"
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
shapes = (1, 3)
fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.11, wspace=0.2)
plt.title('RA min error')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax0_3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

adgust_subplot(ax0_1,'PSD - distance','distance [um]','PSD [um^2]')
adgust_subplot(ax0_2,'AMPA - distance' ,'distance [um]','gmax AMPA [nS]')
adgust_subplot(ax0_3,'NMDA - distance','distance [um]','gmax NMDA [nS]')

for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    j=0
    W_AMPA=[]
    while len(W_AMPA)==0:
        print(W_AMPA)
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        distance=get_MOO_result_parameters(cell_name,'distance',**dictMOO)
        j+=1
    ax0_1.scatter(distance,PSD,**plot_dict)
    if cell_name=='2017_04_03_B':continue
    ax0_2.scatter(distance,W_AMPA,**plot_dict)
    ax0_3.scatter(distance,W_NMDA,**plot_dict)
# ax0_3.legend()
plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.png')
plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.svg')
# plt.show()


