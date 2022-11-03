from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from add_figure import add_figure, adgust_subplot
from create_folder import create_folder_dirr
from open_pickle import read_from_pickle
from function_Figures import find_RA, legend_size, get_MOO_result_parameters, get_std_halloffame
import numpy as np
import sys
from read_spine_properties import get_n_spinese
from scipy.optimize import curve_fit
from scipy.stats import linregress
import scipy.odr
import scipy.stats

if len(sys.argv)!=2:
    save_folder='final_data/total_moo/'
    print("sys.argv not running" ,len(sys.argv))
else:
    save_folder=sys.argv[1]
save_dir=save_folder+'Figure6_AMPA_NMDA_linear_fit/'
create_folder_dirr(save_dir)
scatter_size=8
passive_parameter_names=['RA_min_error','RA_best_fit','RA=100','RA=120']
def linear_fit1(x, a, c):
    return a*x+c
def linear_fit0(x, a):
    return a*x


def f_wrapper_for_odr(beta, x): # parameter order for odr
    return linear_fit0(x, *beta)
def f_wrapper_for_odr1(beta, x): # parameter order for odr
    return linear_fit1(x, *beta)
def return_fit_parameters(x,y,func):
    parameters, cov= curve_fit(func, x, y)
    # if func==linear_fit0:
    model = scipy.odr.odrpack.Model(f_wrapper_for_odr)
    data = scipy.odr.odrpack.Data(x,y)
    myodr = scipy.odr.odrpack.ODR(data, model, beta0=parameters,  maxit=0)
    myodr.set_job(fit_type=2)
    parameterStatistics = myodr.run()
    df_e = len(x) - len(parameters) # degrees of freedom, error
    cov_beta = parameterStatistics.cov_beta # parameter covariance matrix from ODR
    sd_beta = parameterStatistics.sd_beta * parameterStatistics.sd_beta
    ci = []
    t_df = scipy.stats.t.ppf(0.975, df_e)
    ci = []
    for i in range(len(parameters)):
        ci.append([parameters[i] - t_df * parameterStatistics.sd_beta[i], parameters[i] + t_df * parameterStatistics.sd_beta[i]])

    tstat_beta = parameters / parameterStatistics.sd_beta # coeff t-statistics
    pstat_beta = (1.0 - scipy.stats.t.cdf(np.abs(tstat_beta), df_e)) * 2.0    # coef. p-values
    return parameters,tstat_beta,pstat_beta


def add_curve_fit(ax,x,y,m_name='m',units=1,name_units='',x_m=0.3,start_in_zero=True,plot_curve=True):
    if not plot_curve: start_in_zero =False
    if start_in_zero:
        linear_fit=linear_fit0
        m,t,p=return_fit_parameters(x,y,linear_fit0)
        popt=m
        m=m[0]
        t=t[0]
        p=p[0]
        y_pred = linear_fit(x, *popt)
        r2=r2_score(y,y_pred)
    else:
        linear_fit=linear_fit1
        slope, intercept, r, p, se = linregress(x, y)
        popt=[slope,intercept]
        r2=r**2
        # linear_fit=linear_fit1
    # ax0_1.errorbar(all_PSD, all_AMPA, all_std_AMPA, linestyle='None')
    x_data=np.arange(0,max(x)+0.01,0.0005)
    # popt, pcov = curve_fit(linear_fit, x, y)
    x_m=0.7-1/40*(len(m_name)+len(name_units))
    if plot_curve:
        print(x_m)
        ax.plot(x_data, linear_fit(x_data, *popt), '-')
        roundnum=1
        m_slope=round(popt[0]*units,roundnum)
        while m_slope==0:
            m_slope=round(popt[0]*units,roundnum)
            roundnum+=1
        ax.text(x_m,0.03,m_name+'='+str(m_slope)+name_units,transform=ax.transAxes,size='16')
    ax.text(0.03,0.92,'r='+str(round(r2,2)),transform=ax.transAxes,size='16',fontweight='bold')
    if round(p,2)!=0:
        pp=round(p,2)
    elif round(p,3)!=0:
        pp=round(p,3)
    else:
        pp=round(p,4)

    ax.text(0.03,0.86,'p='+str(pp),transform=ax.transAxes,size='16',fontweight='bold')


colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']

if __name__=='__main__':
    # adgust_subplot(ax8,'','Rneck [Mohm]','',latter='H')
    all_W_AMPA,all_W_NMDA,all_V_NMDA,all_g_NMDA,all_PSD,all_color,all_RA=[],[],[],[],[],[],[]
    all_I_spine_head,all_I_spine_base,all_V_spine_head,all_V_spine_base,all_Rin_spine_head,all_Rin_spine_base,all_V_soma_NMDA=[],[],[],[],[],[],[]
    all_Rin_soma,all_Rtrans_spine_head,all_Rtrans_spine_base,all_Rneck=[],[],[],[]
    all_V_spine_head_const,all_Rin_spine_head_const=[],[]
    W_AMPA=[]
    all_W_AMPA_cumulativ,all_g_NMDA_cumulativ,all_PSD_cumulativ=[],[],[]
    for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
        if cell_name=='2017_04_03_B':continue
        j=0
        W_AMPA=[]
        while len(W_AMPA)==0:
            dictMOO={'passive_parameter':passive_parameter_names[j],'syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
            RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
            W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
            W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
            g_NMDA=get_MOO_result_parameters(cell_name,'g_NMDA_spine',**dictMOO)
            V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)
            V_soma_NMDA=get_MOO_result_parameters(cell_name,'V_soma_NMDA',**dictMOO)
            V_spine_head=get_MOO_result_parameters(cell_name,'spine_head_V_high',**dictMOO)
            V_spine_base=get_MOO_result_parameters(cell_name,'neck_base_V_high',**dictMOO)
            Rin_spine_head=get_MOO_result_parameters(cell_name,'spine_head_Rin',**dictMOO)
            Rin_spine_base=get_MOO_result_parameters(cell_name,'neck_base_Rin',**dictMOO)
            PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
            Rneck=get_MOO_result_parameters(cell_name,'Rneck',**dictMOO)
            Rin_soma=get_MOO_result_parameters(cell_name,'soma_Rin',**dictMOO)
            Rtrans_spine_head=get_MOO_result_parameters(cell_name,'spine_head_Rtrans',**dictMOO)
            Rtrans_spine_base=get_MOO_result_parameters(cell_name,'neck_base_Rtrans',**dictMOO)
            j+=1
            print(cell_name,sum(W_NMDA))
            Rin_spine_head_const=get_MOO_result_parameters(cell_name,'spine_head_Rin',MOO_file='results_MOO_const_weigth_Rin_result',**dictMOO)
            V_spine_head_const=get_MOO_result_parameters(cell_name,'spine_head_V_high',MOO_file='results_MOO_const_weigth_Rin_result',**dictMOO)

        if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
            W_NMDA,V_NMDA,V_soma_NMDA,g_NMDA=[None]*len(PSD),[None]*len(PSD),[None]*len(PSD),[None]*len(PSD)
        all_PSD=np.append(all_PSD, PSD)
        all_PSD_cumulativ=np.append(all_PSD_cumulativ,sum(all_PSD_cumulativ)+W_AMPA)

        all_color=np.append(all_color,[colors[i]]*get_n_spinese(cell_name))
        all_RA=np.append(all_RA, RA)
        all_W_AMPA=np.append(all_W_AMPA,W_AMPA)
        all_W_AMPA_cumulativ=np.append(all_W_AMPA_cumulativ,sum(all_W_AMPA_cumulativ)+W_AMPA)
        all_W_NMDA=np.append(all_W_NMDA, W_NMDA)
        all_V_NMDA=np.append(all_V_NMDA,V_NMDA)
        all_V_soma_NMDA=np.append(all_V_soma_NMDA,V_soma_NMDA)
        all_V_spine_head=np.append(all_V_spine_head, V_spine_head)
        all_V_spine_base=np.append(all_V_spine_base,V_spine_base)
        all_Rin_spine_head=np.append(all_Rin_spine_head, Rin_spine_head)
        all_Rin_spine_base=np.append(all_Rin_spine_base,Rin_spine_base)
        all_I_spine_head=np.append(all_I_spine_head,list(V_spine_head/Rin_spine_head))
        all_I_spine_base=np.append(all_I_spine_base,list(V_spine_base/Rin_spine_base))

        all_Rin_soma=np.append(all_Rin_soma, Rin_soma)
        all_Rtrans_spine_head=np.append(all_Rtrans_spine_head,Rtrans_spine_head)
        all_Rtrans_spine_base=np.append(all_Rtrans_spine_base, Rtrans_spine_base)
        all_Rneck=np.append(all_Rneck,Rneck)
        all_g_NMDA=np.append(all_g_NMDA,g_NMDA)
        all_g_NMDA_cumulativ=np.append(all_g_NMDA_cumulativ,sum(all_g_NMDA_cumulativ)+W_AMPA)

        all_Rin_spine_head_const=np.append(all_Rin_spine_head_const,Rin_spine_head_const)
        all_V_spine_head_const=np.append(all_V_spine_head_const,V_spine_head_const)
    all_V_spine_base_NMDA,all_PSD_NMDA,all_V_spine_head_NMDA,all_V_NMDA_NMDA,all_color_NMDA,all_W_AMPA_NMDA,all_W_NMDA_NMDA,all_V_soma_NMDA_NMDA,all_g_NMDA_NMDA=[],[],[],[],[],[],[],[],[]
    all_Rin_spine_head_NMDA,all_Rin_spine_base_NMDA,all_Rtrans_spine_base_NMDA,all_Rtrans_spine_head_NMDA,all_Rneck_NMDA=[],[],[],[],[]
    all_color=list(all_color)

    for i,val in enumerate(all_V_NMDA):
        if val != None :
            all_V_spine_head_NMDA=np.append(all_V_spine_head_NMDA,all_V_spine_head[i])
            all_V_spine_base_NMDA=np.append(all_V_spine_base_NMDA,all_V_spine_base[i])
            all_V_NMDA_NMDA=np.append(all_V_NMDA_NMDA,val)
            all_V_soma_NMDA_NMDA=np.append(all_V_soma_NMDA_NMDA,all_V_soma_NMDA[i])
            all_color_NMDA=np.append(all_color_NMDA,all_color[i])
            all_W_AMPA_NMDA=np.append(all_W_AMPA_NMDA,all_W_AMPA[i])
            all_W_NMDA_NMDA=np.append(all_W_NMDA_NMDA,all_W_NMDA[i])
            all_PSD_NMDA=np.append(all_PSD_NMDA,all_PSD[i])
            all_g_NMDA_NMDA=np.append(all_g_NMDA_NMDA,all_g_NMDA[i])
            all_Rin_spine_head_NMDA=np.append(all_Rin_spine_head_NMDA,all_Rin_spine_head[i])
            all_Rin_spine_base_NMDA=np.append(all_Rin_spine_base_NMDA,all_Rin_spine_base[i])
            all_Rtrans_spine_base_NMDA=np.append(all_Rtrans_spine_base_NMDA,all_Rtrans_spine_base[i])
            all_Rtrans_spine_head_NMDA=np.append(all_Rtrans_spine_head_NMDA,all_Rtrans_spine_head[i])
            all_Rneck_NMDA=np.append(all_Rneck_NMDA,all_Rneck[i])

    # fig=add_figure('','N','cumulative')
    # fig.set_size_inches(6,7)
    # fig.subplots_adjust(left=0.2,right=0.95,top=0.9,bottom=0.15)
    # ax=fig.axes[0]
    # N=range(len(all_W_AMPA_cumulativ))
    # # plot_dict={'label':cell_name,'lw':scatter_size-1,'color':all_color}
    # all_W_AMPA_cumulativ,all_PSD_cumulativ,all_g_NMDA_cumulativ=[],[],[]
    # for i,a in enumerate(sorted(all_W_AMPA)):
    #     all_W_AMPA_cumulativ=np.append(all_W_AMPA_cumulativ,sum(all_W_AMPA[:i+1]))
    #     all_PSD_cumulativ=np.append(all_PSD_cumulativ,sum(all_PSD[:i+1]))
    #     all_g_NMDA_cumulativ=np.append(all_g_NMDA_cumulativ,sum(all_g_NMDA_NMDA[:i+1]))
    #
    # ax.plot(N,all_W_AMPA_cumulativ,label='g_AMPA')
    # ax.plot(N,all_g_NMDA_cumulativ,label='g_NMDA')
    # ax.plot(N,all_PSD_cumulativ,label='PSD')
    # ax.legend()
    # plt.savefig(save_dir+'/cumulative param.png')
    # plt.savefig(save_dir+'/cumulative param.svg')
    # plt.show()
    # plt.close()


    fig = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    fig.subplots_adjust(left=0.1,right=0.95,top=0.9,bottom=0.2,hspace=0.3, wspace=0.25)
    shapes = (2, 3)
    N=range(len(all_W_AMPA_cumulativ))
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 0), rowspan=1, colspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)
    adgust_subplot(ax1,'','','',latter='A')
    adgust_subplot(ax2,'','','',latter='B')
    adgust_subplot(ax3,'','','',latter='C')
    adgust_subplot(ax4,'','PSD','',latter='D')
    adgust_subplot(ax5,'','AMPA','',latter='E')
    adgust_subplot(ax6,'','NMDA','',latter='F')
    ax1.hist(all_W_AMPA, bins=6)
    ax2.hist(all_g_NMDA_NMDA, bins=6)
    ax3.hist(all_PSD, bins=6)
    all_W_AMPA_cumulativ,all_PSD_cumulativ,all_g_NMDA_cumulativ=[],[],[]

    for i,a in enumerate(sorted(all_W_AMPA)):
        all_W_AMPA_cumulativ=np.append(all_W_AMPA_cumulativ,sum(all_W_AMPA[:i+1]))
        all_PSD_cumulativ=np.append(all_PSD_cumulativ,sum(all_PSD[:i+1]))
        all_g_NMDA_cumulativ=np.append(all_g_NMDA_cumulativ,sum(all_g_NMDA_NMDA[:i+1]))
    N=range(len(all_W_AMPA_cumulativ))
    ax4.plot(N,all_PSD_cumulativ,label='PSD')
    ax5.plot(N,all_W_AMPA_cumulativ,label='g_AMPA')
    ax6.plot(N,all_g_NMDA_cumulativ,label='g_NMDA')
    plt.savefig(save_dir+'/hist param.png')
    plt.savefig(save_dir+'/hist param.svg')
    # plt.show()
    plt.close()

    fig2 = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    fig2.subplots_adjust(left=0.1,right=0.95,top=0.9,bottom=0.1,hspace=0.3, wspace=0.25)
    shapes = (2, 3)
    plt.title('max EPSP  against resistance')
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(0, 2), rowspan=1, colspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

    adgust_subplot(ax1,'','Rin spine head [MOum]','EPSP  spine head [mV]',latter='A')
    adgust_subplot(ax2,'','Rin spine base [MOum]','EPSP  spine base [mV]',latter='B')
    adgust_subplot(ax3,'','Rtrans spine head [Oum]','EPSP  spine head [mV]',latter='C')
    adgust_subplot(ax4,'','Rtrans spine base [Oum]','EPSP  spine base [mV]',latter='D')
    adgust_subplot(ax5,'','Rneck [MOum*1e-2]','EPSP  spine head [mV]',latter='E')
    adgust_subplot(ax6,'','Rneck [MOum*1e-2]','EPSP  spine base [mV]',latter='F')

    dict4plot={'ax1':[all_Rin_spine_head,all_V_spine_head],'ax2':[all_Rin_spine_base,all_V_spine_base],'ax3':[all_Rtrans_spine_head,all_V_spine_head],
     'ax4':[all_Rtrans_spine_base,all_V_spine_base],'ax5':[all_Rneck,all_V_spine_head],'ax6':[all_Rneck,all_V_spine_base]}
    plot_dict={'color':all_color,'lw':scatter_size-2}
    # plot_dict={'color':all_color,'label':cell_name,'lw':scatter_size-2}
    for key,item in dict4plot.items():
        ax=eval(key)
        ax.scatter(item[0],item[1],**plot_dict)
        add_curve_fit(ax,item[0],item[1],start_in_zero=False,plot_curve=False)
    ax1.scatter(all_Rin_spine_head_const,all_V_spine_head_const,color=all_color,lw=scatter_size-6,marker='*')
    add_curve_fit(ax1,all_Rin_spine_head_const,all_V_spine_head_const,start_in_zero=False,plot_curve=False)

    plt.savefig(save_dir+'/V againg resistance.png')
    plt.savefig(save_dir+'/V against resistance.svg')
    # plt.show()
    plt.close()

    fig=add_figure('','PSD [um^2]','Isyn [nA]')
    # fig = plt.gcf()
    fig.set_size_inches(6,7)
    fig.subplots_adjust(left=0.2,right=0.95,top=0.9,bottom=0.15)
    ax=fig.axes[0]
    plot_dict={'label':cell_name,'lw':scatter_size-1,'color':all_color}
    ax.scatter(all_PSD,all_I_spine_head,**plot_dict)
    add_curve_fit(ax,all_PSD,all_I_spine_head,name_units='um^2/pA')
    plt.savefig(save_dir+'/gregor-current_PSD1.png')
    plt.savefig(save_dir+'/gregor-current_PSD1.svg')
    # plt.show()
    plt.close()

    fig3 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
    fig3.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.3)
    shapes = (1, 3)
    plt.title('RA_min_error')
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

    adgust_subplot(ax1,'' ,'PSD [um^2]','gmax AMPA [nS]',latter='A')
    adgust_subplot(ax2,'','PSD [um^2]','g NMDA [nS]',latter='B')
    adgust_subplot(ax3,'','gmax AMPA [nS]','g NMDA [mV]',latter='C')
    dict4plot={'ax1':[all_PSD,all_W_AMPA,'m'],'ax2':[all_PSD,all_g_NMDA,'m'],'ax3':[all_W_AMPA,all_g_NMDA,'AMPA/NMDA']}
    plot_dict={'label':cell_name,'lw':scatter_size-1,'color':all_color}
    for key,item in dict4plot.items():
        ax=eval(key)
        ax.scatter(item[0],item[1],**plot_dict)
        # add_curve_fit(ax,item[0],item[1],start_in_zero=False,plot_curve=False)

    # ax3.legend(loc='upper right',bbox_to_anchor=(1.2, 0.55),prop={'size': legend_size-1})

    add_curve_fit(ax1,all_PSD, all_W_AMPA,'m',name_units='pS/um^2')
    add_curve_fit(ax2,all_PSD_NMDA, all_g_NMDA_NMDA,'m',name_units='pS/um^2',start_in_zero=False)
    add_curve_fit(ax3,all_W_AMPA_NMDA, all_g_NMDA_NMDA,'AMPA/NMDA',name_units='AU',x_m=0.62,start_in_zero=False)

    plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.png')
    plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA_min_error.svg')
    # plt.show()
    plt.close()




    fig2 = plt.figure(figsize=(15, 10))  # , sharex="row", sharey="row"
    # fig2.subplots_adjust(left=0.05,right=0.99,top=0.95,bottom=0.05,hspace=0.2, wspace=0.25)
    fig2.subplots_adjust(left=0.1,right=0.95,top=0.9,bottom=0.1,hspace=0.25, wspace=0.2)
    shapes = (2, 3)
    plt.title('RA min error EPSP on spine and base')
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax4 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
    ax5 = plt.subplot2grid(shape=shapes, loc=(0, 2), rowspan=1, colspan=1)
    ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

    adgust_subplot(ax1,'','','EPSP spine head [mV]',latter='A')
    adgust_subplot(ax2,'','PSD [um^2]','EPSP spine base [mV]',latter='B')
    adgust_subplot(ax3,'','','',latter='C')
    adgust_subplot(ax4,'','AMPA [nS]','',latter='D')
    adgust_subplot(ax5,'','','',latter='E')
    adgust_subplot(ax6,'','NMDA [nS]','',latter='F')


    dict4plot={'ax1':[all_PSD,all_V_spine_head],'ax2':[all_PSD,all_V_spine_base],'ax3':[all_W_AMPA,all_V_spine_head],
     'ax4':[all_W_AMPA,all_V_spine_base],'ax5':[all_g_NMDA_NMDA,all_V_spine_head_NMDA],'ax6':[all_g_NMDA_NMDA,all_V_spine_base_NMDA]}
    # plot_dict={'color':all_color,'label':cell_name,'lw':scatter_size-2}
    for key,item in dict4plot.items():
        print(key)
        if key in ['ax5','ax6']:
            plot_dict={'color':all_color_NMDA,'lw':scatter_size-2}
        else:
            plot_dict={'color':all_color,'lw':scatter_size-2}
        ax=eval(key)
        ax.scatter(item[0],item[1],**plot_dict)
        add_curve_fit(ax,item[0],item[1],start_in_zero=False,plot_curve=False)

    plt.savefig(save_dir+'/V_high.png')
    plt.savefig(save_dir+'/V_high.svg')
    # plt.show()
    plt.close()

    fig1 = plt.figure(figsize=(15, 6))  # , sharex="row", sharey="row"
    fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.25)
    shapes = (1, 3)
    plt.title('gmax AMPA against NMDA')
    ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

    adgust_subplot(ax1,'' ,'gmax AMPA [nS]','g NMDA [nS]',latter='A')
    adgust_subplot(ax2,'','gmax AMPA [nS]','Vmax NMDA spine head [mV]',latter='B')
    adgust_subplot(ax3,'','gmax AMPA [nS]','Vmax NMDA soma[mV]',latter='C')
    dict4plot={'ax1':[all_W_AMPA_NMDA,all_g_NMDA_NMDA],'ax2':[all_W_AMPA_NMDA,all_V_NMDA_NMDA],'ax3':[all_W_AMPA_NMDA,all_V_soma_NMDA_NMDA]}
    # plot_dict={'color':all_color,'label':cell_name,'lw':scatter_size-2}
    for key,item in dict4plot.items():
        print(key)
        plot_dict={'color':all_color_NMDA,'lw':scatter_size-2}
        ax=eval(key)
        ax.scatter(item[0],item[1],**plot_dict)
        add_curve_fit(ax,item[0],item[1],start_in_zero=False,plot_curve=True)
    plt.savefig(save_dir+'/NMDA against AMPA.png')
    plt.savefig(save_dir+'/NMDA against AMPA.svg')
    plt.close()

    fig1 = plt.figure(figsize=(20, 10))  # , sharex="row", sharey="row"
    fig1.subplots_adjust(left=0.05,right=0.95,top=0.95,bottom=0.1,hspace=0.2, wspace=0.25)
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
    adgust_subplot(ax2,'','Rin spine head [Mohm]','g NMDA [nS]',latter='B')
    adgust_subplot(ax3,'','','',latter='C')
    adgust_subplot(ax4,'','Rin spine base [Mohm]','',latter='D')
    adgust_subplot(ax5,'','','',latter='E')
    adgust_subplot(ax6,'','Rtranfer [Mohm]','',latter='F')
    adgust_subplot(ax7,'','','',latter='G')
    adgust_subplot(ax8,'','Rneck [Mohm]','',latter='H')
    dict4plot={'ax1':[all_Rin_spine_head,all_W_AMPA],'ax3':[all_Rin_spine_base,all_W_AMPA],'ax5':[all_Rtrans_spine_base,all_W_AMPA],'ax7':[all_Rneck,all_W_AMPA],
               'ax2':[all_Rin_spine_head_NMDA,all_g_NMDA_NMDA],'ax4':[all_Rin_spine_base_NMDA,all_g_NMDA_NMDA],'ax6':[all_Rtrans_spine_base_NMDA,all_g_NMDA_NMDA],'ax8':[all_Rneck_NMDA,all_g_NMDA_NMDA]}
    for key,item in dict4plot.items():
        if key in ['ax1','ax3','ax5','ax7']:
            plot_dict={'label':cell_name,'lw':scatter_size-1,'color':all_color}
        else:
            plot_dict={'label':cell_name,'lw':scatter_size-1,'color':all_color_NMDA}
        ax=eval(key)
        ax.scatter(item[0],item[1],**plot_dict)
        add_curve_fit(ax,item[0],item[1],start_in_zero=False,plot_curve=False)

    plt.savefig(save_dir+'/Resistance-Conductance.png')
    plt.savefig(save_dir+'/Resistance-Conductance.svg')
    # plt.show()
    plt.close()

    fig1 = plt.figure(figsize=(16, 6))  # , sharex="row", sharey="row"
    shapes = (1, 3)
    fig1.subplots_adjust(left=0.1,right=0.95,top=0.80,bottom=0.15,hspace=0.11, wspace=0.3)
    plt.title('RA min error')
    ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    ax0_3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)

    adgust_subplot(ax0_1,'','distance [um]','PSD [um^2]','A')
    adgust_subplot(ax0_2,'' ,'distance [um]','gmax AMPA [nS]','B')
    adgust_subplot(ax0_3,'','distance [um]','g NMDA [mV]','C')
    # adgust_subplot(ax0_3,'','PSD/spine_head_area','gmax [mV]','C')

    all_AMPA,all_NMDA,all_PSD,all_dis,all_dis_NMDA,all_g_NMDA=[],[],[],[],[],[]
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
            g_NMDA=get_MOO_result_parameters(cell_name,'g_NMDA_spine',**dictMOO)

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
            W_NMDA,V_NMDA,g_NMDA=[None]*len(PSD),[None]*len(PSD),[None]*len(PSD)
        else:
            all_g_NMDA=np.append(all_g_NMDA, g_NMDA)
            all_dis_NMDA=np.append(all_dis_NMDA, distance)
            ax0_3.scatter(distance,g_NMDA,**plot_dict)

        ax0_2.scatter(distance,W_AMPA,**plot_dict)

    # ax0_3.legend()

    add_curve_fit(ax0_1,all_dis, all_PSD,units=10000,name_units='um',start_in_zero=False)
    add_curve_fit(ax0_2,all_dis, all_AMPA,units=1000,name_units='pS/um',start_in_zero=False)
    add_curve_fit(ax0_3,all_dis_NMDA, all_g_NMDA,units=1000,name_units='pS/um',start_in_zero=False)
    plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.png')
    plt.savefig(save_dir+'/distance_against_PSD_AMPA_NMDA_RA_min_error.svg')
    # plt.show()


    fig1 = plt.figure(figsize=(10, 6))  # , sharex="row", sharey="row"
    colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
    shapes = (1, 2)
    fig1.subplots_adjust(left=0.1,right=0.95,top=0.85,bottom=0.15,hspace=0.01, wspace=0.3)
    plt.title('RA=70')
    ax0_1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
    ax0_2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
    adgust_subplot(ax0_1,'' ,'PSD [um^2]','gmax AMPA [nS]',latter='A')
    adgust_subplot(ax0_2,'','PSD [um^2]','g NMDA [mV]',latter='B')
    all_AMPA,all_NMDA,all_PSD,all_PSD_NMDA,all_g_NMDA=[],[],[],[],[]
    for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
        if cell_name=='2017_04_03_B':continue
        plot_dict={'color':colors[i],'label':cell_name,'lw':scatter_size-2}
        W_AMPA=[]
        dictMOO={'passive_parameter':'RA=70','syn_num':None,'from_picture':cell_name in read_from_pickle('cells_sec_from_picture.p'),'double_spine_area':False}
        while len(W_AMPA)==0:
            PSD=get_MOO_result_parameters(cell_name,'PSD',**dictMOO)
            RA=get_MOO_result_parameters(cell_name,'RA',**dictMOO)
            W_AMPA=get_MOO_result_parameters(cell_name,'W_AMPA',**dictMOO)
            W_NMDA=get_MOO_result_parameters(cell_name,'W_NMDA',**dictMOO)
            V_NMDA=get_MOO_result_parameters(cell_name,'V_syn_NMDA',**dictMOO)
            g_NMDA=get_MOO_result_parameters(cell_name,'g_NMDA_spine',**dictMOO)

        if sum(W_NMDA)<=0.005*sum(PSD/max(PSD)):
            W_NMDA,V_NMDA,g_NMDA=[None]*len(PSD),[None]*len(PSD),[None]*len(PSD)
        else:
            all_g_NMDA=np.append(all_g_NMDA, g_NMDA)
            all_PSD_NMDA=np.append(all_PSD_NMDA, PSD)

        all_AMPA=np.append(all_AMPA, W_AMPA)
        all_PSD=np.append(all_PSD, PSD)
        ax0_1.scatter(PSD,W_AMPA,**plot_dict)
        ax0_2.scatter(PSD,g_NMDA,**plot_dict)
    # ax0_2.legend()
    add_curve_fit(ax0_1,all_PSD,all_AMPA,name_units='m',start_in_zero=False)
    add_curve_fit(ax0_2,all_PSD_NMDA,all_g_NMDA,name_units='m',start_in_zero=False)

    plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=70.png')
    plt.savefig(save_dir+'/AMPA_NMDA_PSD_RA=70.svg')
    # plt.show()






