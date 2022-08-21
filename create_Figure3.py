from matplotlib import pyplot as plt
from add_figure import add_figure, adgust_subplot
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg, get_parameter, get_n_spinese, calculate_Rneck
from function_Figures import find_RA
from glob import glob
add_figure('all cells psd against distance from soma','soma distance [um]','PSD [um^2]')

for cell_name in read_from_pickle('cells_name2.p'):
    diss,psd=[],[]
    for i in range(get_n_spinese(cell_name)):
        sec,seg,dis=get_sec_and_seg(cell_name,with_distance=True,spine_num=i)
        # secs.append(sec)
        # segs.append(seg)
        diss.append(dis)
        psd.append(get_parameter(cell_name,'PSD',i))
    plt.scatter(diss,psd,lw=8)




fig = plt.figure(figsize=(20, 20))  # , sharex="row", sharey="row"
shapes = (2, 3)
ax1 = plt.subplot2grid(shape=shapes, loc=(0, 0), rowspan=1, colspan=1)
ax2 = plt.subplot2grid(shape=shapes, loc=(0, 1), colspan=1, rowspan=1)
ax3 = plt.subplot2grid(shape=shapes, loc=(0, 2), colspan=1, rowspan=1)
ax4 = plt.subplot2grid(shape=shapes, loc=(1, 0), colspan=1, rowspan=1)
ax5 = plt.subplot2grid(shape=shapes, loc=(1, 1), colspan=1, rowspan=1)
ax6 = plt.subplot2grid(shape=shapes, loc=(1, 2), colspan=1, rowspan=1)

colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4']
for i,cell_name in enumerate(read_from_pickle('cells_name2.p')):
    color=colors[i]
    base_dir='final_data/'+cell_name+'/'
    decided_passive_params=find_RA(base_dir)
    dicty=read_from_pickle(glob(base_dir+'Rins_pickles*'+decided_passive_params+'.p')[0])
    PSD=dicty['parameters']['PSD']

    adgust_subplot(ax1,'R transfer syn','PSD','MOum')
    ax1.scatter(PSD,dicty['spine_head']['Rtrans'],color=color)
    ax1.scatter(PSD,dicty['neck_base']['Rtrans'],marker='*',color=colors[i+1])

    adgust_subplot(ax2,'Rins','PSD','MOum')
    ax2.scatter(PSD,dicty['spine_head']['Rin'],color=color)
    ax2.scatter(PSD,dicty['neck_base']['Rin'],marker='*',color=colors[i+1])
    ax2.scatter(sum(PSD),dicty['soma']['Rin'],marker='o',color=color)

    adgust_subplot(ax3,'AMPA and NMDA','PSD','AMPA [nS]')
    ax3.scatter(PSD,dicty['parameters']['reletive_strengths']*dicty['parameters']['W_AMPA'],color=color)

    adgust_subplot(ax4,'AMPA and NMDA','PSD','NMDA [nS]')
    ax4.scatter(PSD,dicty['parameters']['reletive_strengths']*dicty['parameters']['W_NMDA'],marker='*',color=color)

    adgust_subplot(ax5,'Rneck','PSD','micron')
    ax5.scatter(PSD,calculate_Rneck(cell_name,dicty['parameters']['RA']))

    adgust_subplot(ax6,'Distance from Soma','PSD','micron')
    ax6.scatter(PSD,dicty['parameters']['distance'])
plt.savefig('final_data/Figure3/PDF relation.png')
plt.savefig('final_data/Figure3/PDF relation.svg')





plt.show()

