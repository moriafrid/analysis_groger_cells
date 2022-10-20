from matplotlib import pyplot as plt
from add_figure import add_figure, adgust_subplot
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
from function_Figures import find_RA, legend_size, get_MOO_result_parameters, get_std_halloffame
import numpy as np
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


fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
shapes = (1, 3)
plt.title('RA_min_error')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax0_3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

adgust_subplot(ax0_1,'AMPA-PSD' ,'PSD','gmax AMPA [nS]',latter='A')
adgust_subplot(ax0_2,'NMDA-PSD','PSD','gmax NMDA [mV]',latter='B')
adgust_subplot(ax0_3,'AMPA-NMDA','gmax AMPA [nS]','Vmax NMDA [mV]',latter='C')
all_AMPA,all_std_AMPA,all_NMDA,all_std_NMDA,all_PSD,all_AMPA_NMDA,all_PSD_NMDA,all_W_NMDA,all_V_NMDA=[],[],[],[],[],[],[],[],[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    print(cell_name)
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    W_AMPA=[]
    j=0
    dictMOO={'passive_parameter':find_RA(save_folder+cell_name),'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
    PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
    RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
    W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
    W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
    V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)
    distance=get_MOO_result_parameters(cell_name,'distance',**dictMOO)
    std_AMPA,std_NMDA=get_std_halloffame(cell_name,folder2run=save_folder)
    if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
        W_NMDA,V_NMDA,std_NMDA=[None]*len(PSD),[None]*len(PSD),[None]*len(PSD)
    all_AMPA=np.append(all_AMPA, W_AMPA)
    all_PSD=np.append(all_PSD, PSD)
    all_std_AMPA=np.append(all_std_AMPA, std_AMPA*np.ones(len(W_AMPA)))#(PSD/max(PSD))/sum(PSD/max(PSD)))
    if None in W_NMDA:
        all_std_NMDA=np.append(all_std_NMDA, None)#(PSD/max(PSD))/sum(PSD/max(PSD)))
    else:
        all_std_NMDA=np.append(all_std_NMDA, std_NMDA*np.ones(len(W_AMPA)))#(PSD/max(PSD))/sum(PSD/max(PSD)))
        # ax0_1.errorbar(PSD, W_AMPA, std_AMPA*10, linestyle='None',ecolor=colors[i],elinewidth=scatter_size-4)
        # ax0_2.errorbar(PSD, W_NMDA, std_NMDA*10, linestyle='None',ecolor=colors[i],elinewidth=scatter_size-4)
        # ax0_3.errorbar(W_AMPA, W_NMDA,std_NMDA*10, std_AMPA*100, linestyle='None',ecolor=colors[i],elinewidth=scatter_size-6)
        all_W_NMDA=np.append(all_W_NMDA, W_NMDA)
        all_V_NMDA=np.append(all_V_NMDA, V_NMDA)
        all_PSD_NMDA=np.append(all_PSD_NMDA, PSD)
        all_AMPA_NMDA=np.append(all_AMPA_NMDA, W_AMPA)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,W_NMDA,**plot_dict)
    ax0_3.scatter(W_AMPA,V_NMDA,**plot_dict)


ax0_3.legend(loc='upper right',bbox_to_anchor=(1.2, 0.55),prop={'size': legend_size-1})

# ax0_1.errorbar(all_PSD, all_AMPA, all_std_AMPA, linestyle='None')
x_data=np.arange(0,max(all_PSD)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_PSD, all_AMPA)
ax0_1.plot(x_data, linear_fit(x_data, *popt1), '-')
ax0_1.text(0.5,0.03,'g_density='+str(round(popt1[0],2)),transform=ax0_1.transAxes,size='16')

# ax0_2.errorbar(all_PSD, all_NMDA, all_std_NMDA, linestyle='None')
popt2, pcov2 = curve_fit(linear_fit, all_PSD_NMDA, all_W_NMDA)
ax0_2.plot(x_data, linear_fit(x_data, *popt2), '-')
ax0_2.text(0.5,0.03,'g_density='+str(round(popt2[0],2)),transform=ax0_2.transAxes,size='16')

x_data=np.arange(0,max(all_AMPA_NMDA)+0.01,0.0005)
popt3, pcov3 = curve_fit(linear_fit, all_AMPA_NMDA, all_V_NMDA)
ax0_3.plot(x_data, linear_fit(x_data, *popt3),'-',color=colors[0])
ax0_3.text(0.65,0.03,'AMPA/NMDA='+str(round(popt3[0],2)),transform=ax0_3.transAxes,size='16')

plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.svg')
# plt.show()

fig1 = plt.figure(figsize=(16, 6))  # , sharex="row", sharey="row"
shapes = (1, 3)
fig1.subplots_adjust(left=0.1,right=0.95,top=0.80,bottom=0.15,hspace=0.11, wspace=0.2)
plt.title('RA min error')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax0_3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

adgust_subplot(ax0_1,'PSD - distance','distance [um]','PSD [um^2]','A')
adgust_subplot(ax0_2,'AMPA - distance' ,'distance [um]','gmax AMPA [nS]','B')
adgust_subplot(ax0_3,'NMDA - distance','distance [um]','Vmax NMDA [mV]','C')
all_AMPA,all_NMDA,all_PSD,all_dis,all_dis_NMDA=[],[],[],[],[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    j=0
    W_AMPA=[]
    while len(W_AMPA)==0:
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        distance=get_MOO_result_parameters(cell_name,'distance',**dictMOO)
        j+=1
        print(W_AMPA)

    all_AMPA=np.append(all_AMPA, W_AMPA)
    all_PSD=np.append(all_PSD, PSD)
    all_dis=np.append(all_dis, distance)


    ax0_1.scatter(distance,PSD,**plot_dict)
    if cell_name=='2017_04_03_B':continue

    if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
        W_NMDA,V_NMDA=[None]*len(PSD),[None]*len(PSD)
    else:
        all_NMDA=np.append(all_NMDA, V_NMDA)
        all_dis_NMDA=np.append(all_dis_NMDA, distance)
    ax0_2.scatter(distance,W_AMPA,**plot_dict)
    ax0_3.scatter(distance,V_NMDA,**plot_dict)

# ax0_3.legend()


x_data=np.arange(0,max(all_dis)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_dis, all_PSD)
ax0_1.plot(x_data, linear_fit(x_data, *popt1), '-')
ax0_1.text(0.6,0.03,'m='+str(round(popt1[0]*10000,2))+' cm',transform=ax0_1.transAxes,size=16)

popt2, pcov2 = curve_fit(linear_fit, all_dis, all_AMPA)
ax0_2.plot(x_data, linear_fit(x_data, *popt2), '-')
ax0_2.text(0.6,0.03,'m='+str(round(popt2[0]*1000,2))+' pS/um',transform=ax0_2.transAxes,size=16)


popt3, pcov3 = curve_fit(linear_fit, all_dis_NMDA, all_NMDA)
ax0_3.plot(x_data, linear_fit(x_data, *popt3), '-')
ax0_3.text(0.6,0.03,'m='+str(round(popt3[0]*1000,2))+' pS/um',transform=ax0_3.transAxes,size=16)
plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.png')
plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.svg')
# plt.show()


fig2 = plt.figure(figsize=(20, 10))  # , sharex="row", sharey="row"
fig2.subplots_adjust(left=0.05,right=0.95,top=0.95,bottom=0.1,hspace=0.2, wspace=0.25)
shapes = (2, 4)
plt.title('RA min error Rneck against AMPA and NMDA')
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 1), rowspan=1, colspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
ax7 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
ax8 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

adgust_subplot(ax1,'','','gmax AMPA [nS]',latter='A')
adgust_subplot(ax2,'','Rin spine head [Mohm]','Vmax NMDA [nS]',latter='B')
adgust_subplot(ax3,'','','',latter='C')
adgust_subplot(ax4,'','Rin spine base [Mohm]','',latter='D')
adgust_subplot(ax5,'','','',latter='E')
adgust_subplot(ax6,'','Rtranfer [Mohm]','',latter='F')
adgust_subplot(ax7,'','','',latter='G')
adgust_subplot(ax8,'','Rneck [Mohm]','',latter='H')
all_AMPA,all_NMDA,all_PSD=[],[],[]
W_AMPA=[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    j=0
    W_AMPA=[]
    while len(W_AMPA)==0:
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)

        Rneck=get_MOO_result_parameters(cell_name,'Rneck',**dictMOO)
        Rin_spine_head=get_MOO_result_parameters(cell_name,'spine_head_Rin',**dictMOO)
        Rin_spine_base=get_MOO_result_parameters(cell_name,'neck_base_Rin',**dictMOO)
        Rin_soma=get_MOO_result_parameters(cell_name,'soma_Rin',**dictMOO)
        Rtrans_spine_head=get_MOO_result_parameters(cell_name,'spine_head_Rin',**dictMOO)
        Rtrans_spine_base=get_MOO_result_parameters(cell_name,'neck_base_Rin',**dictMOO)
        j+=1
        print(W_AMPA)
    if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
        W_NMDA,V_NMDA=[None]*len(PSD),[None]*len(PSD)
    ax1.scatter(Rin_spine_head,W_AMPA,**plot_dict)
    ax3.scatter(Rin_spine_base,W_AMPA,**plot_dict)
    ax5.scatter(Rtrans_spine_base,W_AMPA,**plot_dict)
    ax7.scatter(Rneck,W_AMPA,**plot_dict)
    ax2.scatter(Rin_spine_head,V_NMDA,**plot_dict)
    ax4.scatter(Rin_spine_base,V_NMDA,**plot_dict)
    ax6.scatter(Rtrans_spine_base,V_NMDA,**plot_dict)
    ax8.scatter(Rneck,V_NMDA,**plot_dict)
plt.savefig(save_dir+'/Resistance-Conductance.png')
plt.savefig(save_dir+'/Resistance-Conductance.svg')
# plt.show()

fig2 = plt.figure(figsize=(10, 15))  # , sharex="row", sharey="row"
fig2.subplots_adjust(left=0.15,right=0.95,top=0.95,bottom=0.1,hspace=0.2, wspace=0.25)
shapes = (3, 2)
plt.title('RA min error V on spine and base')
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(2, 0), colspan=1, rowspan=1)

ax4 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(1, 1), rowspan=1, colspan=1)
ax6 = plt.subplot2grid(shape=shapes, loc=(2, 1), colspan=1, rowspan=1)
# ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
# ax7 = plt.subplot2grid(shape=shapes, loc=(0, 3), colspan=1, rowspan=1)
# ax8 = plt.subplot2grid(shape=shapes, loc=(1, 3), colspan=1, rowspan=1)

adgust_subplot(ax1,'','','AMPA [nS]',latter='A')
adgust_subplot(ax2,'','','NMDA [nS]',latter='B')
adgust_subplot(ax3,'','V_high spine head','PSD',latter='C')

adgust_subplot(ax4,'','','',latter='D')
adgust_subplot(ax5,'','','',latter='F')
adgust_subplot(ax6,'','V_high spine base','',latter='G')
# adgust_subplot(ax8,'','Rneck [Mohm]','',latter='H')
all_AMPA,all_NMDA,all_PSD=[],[],[]
I_spine_head,I_spine_base=[],[]
W_AMPA=[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    j=0
    W_AMPA=[]
    while len(W_AMPA)==0:
        dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
        W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
        W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
        V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)

        V_spine_head=get_MOO_result_parameters(cell_name,'spine_head_V_high',**dictMOO)
        V_spine_base=get_MOO_result_parameters(cell_name,'neck_base_V_high',**dictMOO)
        Rin_spine_head=get_MOO_result_parameters(cell_name,'spine_head_Rin',**dictMOO)
        Rin_spine_base=get_MOO_result_parameters(cell_name,'neck_base_Rin',**dictMOO)
        PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
        I_spine_head=np.append(I_spine_head,list(V_spine_head/Rin_spine_head))
        I_spine_base=np.append(I_spine_base,list(V_spine_base/Rin_spine_base))
        all_PSD=np.append(all_PSD, PSD)
        j+=1
        print(cell_name,sum(W_NMDA))
    if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
        W_NMDA,V_NMDA=[None]*len(PSD),[None]*len(PSD)
    ax1.scatter(V_spine_head,W_AMPA,**plot_dict)
    ax2.scatter(V_spine_head,V_NMDA,**plot_dict)
    ax5.scatter(V_spine_base,V_NMDA,**plot_dict)
    ax3.scatter(V_spine_head,PSD,**plot_dict)
    ax4.scatter(V_spine_base,W_AMPA,**plot_dict)
    ax6.scatter(V_spine_base,PSD,**plot_dict)

plt.savefig(save_dir+'/V_high.png')
plt.savefig(save_dir+'/V_high.svg')
# plt.show()

fig2 = plt.figure(figsize=(10, 10))  # , sharex="row", sharey="row"
fig2.subplots_adjust(left=0.15,right=0.95,top=0.95,bottom=0.1,hspace=0.2, wspace=0.25)
shapes = (1, 1)
plt.title('Synaptic current against PSD')
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
# ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax1,'','PSD [um^2]','Isyn [nA]',latter='A',xylabelsize=30,xytitlesize=30)
# adgust_subplot(ax2,'','PSD [um^2]','I spine base [nA]',latter='B')
plot_dict={'color':'black','label':cell_name,'lw':scatter_size-1}
ax1.scatter(all_PSD,I_spine_head,**plot_dict)
#ax2.scatter(all_PSD,I_spine_base,**plot_dict)

x_data=np.arange(0,max(all_PSD)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_PSD, I_spine_head)
ax1.plot(x_data, linear_fit(x_data, *popt1), '-')
# ax1.text(0.5,0.03,'g_density='+str(round(popt1[0],2)),transform=ax1.transAxes,size='16')
popt2, pcov2 = curve_fit(linear_fit, all_PSD, I_spine_base)
# ax2.plot(x_data, linear_fit(x_data, *popt2), '-')
# ax2.text(0.5,0.03,'g_density='+str(round(popt2[0],2)),transform=ax2.transAxes,size='16')
plt.savefig(save_dir+'/gregor-current_PSD1.png')
plt.savefig(save_dir+'/gregor-current_PSD1.svg')
# plt.show()

fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
shapes = (1, 2)
fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.2)
plt.title('RA=70')
ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
adgust_subplot(ax0_1,'AMPA g_max' ,'PSD','gmax AMPA [nS]',latter='A')
adgust_subplot(ax0_2,'NMDA g_max','PSD','Vmax NMDA [mV]',latter='B')
all_AMPA,all_NMDA,all_PSD,all_PSD_NMDA=[],[],[],[]
W_AMPA=[]
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    if cell_name=='2017_04_03_B':continue
    plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
    W_AMPA=[]
    dictMOO={'passive_parameter':'RA=70','syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}

    PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
    RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
    W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
    W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
    V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)

    if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
        W_NMDA,V_NMDA=[None]*len(PSD),[None]*len(PSD)
    else:
        all_NMDA=np.append(all_NMDA, V_NMDA)
        all_PSD_NMDA=np.append(all_PSD_NMDA, PSD)

    all_AMPA=np.append(all_AMPA, W_AMPA)
    all_PSD=np.append(all_PSD, PSD)
    ax0_1.scatter(PSD,W_AMPA,**plot_dict)
    ax0_2.scatter(PSD,V_NMDA,**plot_dict)
ax0_2.legend()
x_data=np.arange(0,max(all_PSD)+0.01,0.0005)
popt1, pcov1 = curve_fit(linear_fit, all_PSD, all_AMPA)
ax0_1.plot(x_data, linear_fit(x_data, *popt1), '-')
ax0_1.text(0.05,0.9,'g_density='+str(round(popt1[0],2)),transform=ax0_1.transAxes)
popt2, pcov2 = curve_fit(linear_fit, all_PSD_NMDA, all_NMDA)
ax0_2.plot(x_data, linear_fit(x_data, *popt2), '-')
ax0_2.text(0.5,0.9,'g_density='+str(round(popt2[0],2)),transform=ax0_2.transAxes)
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=70.png')
plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=70.svg')
# plt.show()






