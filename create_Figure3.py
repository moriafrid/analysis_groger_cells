from matplotlib import pyplot as plt
from add_figure import add_figure
from open_pickle import read_from_pickle
from read_spine_properties import get_sec_and_seg, get_parameter, get_n_spinese
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

    base_dir='final_data/'+cell_name+'/'
    decided_passive_params=find_RA(base_dir)
    dicty=read_from_pickle(glob(base_dir+'Rins_pickles*'+decided_passive_params+'.p')[0])
    add_figure('R_transfer syn','oum','PSD')

    add_figure('R_in syn','oum','PSD')



plt.show()

