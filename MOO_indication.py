import numpy as np
from matplotlib import pyplot as plt
from glob import glob
import shutil
from create_folder import create_folder_dirr
from add_figure import add_figure
from function_Figures import find_RA
from open_pickle import read_from_pickle

def copy_file(copy,paste,extra_name=''):
    if extra_name!='':
        extra_name='_'+extra_name
    if 'txt' in copy:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.txt')[0]+extra_name+'.txt'+copy.split('.txt')[1])
    elif 'tmp' in copy:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.tmp')[0]+extra_name+'.tmp'+copy.split('.tmp')[1])
    else:
        shutil.copy(copy,paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.p'+copy.split('.p')[1])
    if 'png' not in copy and 'final_pop' not in copy and "pickles" not in copy and "txt" not in copy  and "tmp" not in copy:
        try:
            fig=read_from_pickle(copy)
            plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.png')
            # plt.savefig(paste+'/'+copy.split('/')[-1].split('.p')[0]+extra_name+'.svg')
            plt.close()
        except:
            print('')

def plot_moo_configuration(cell_name,folder2run='final_data/total_moo/'):
    base_dir=folder2run+'/'+cell_name+'/'
    passive_param=find_RA(base_dir)
    population=read_from_pickle(glob(base_dir+'/cp*'+passive_param+'.tmp')[0])
    avg=np.array([i['avg'] for i in population['logbook']])
    std=np.array([i['std'] for i in population['logbook']])
    min_=np.array([i['min'] for i in population['logbook']])
    max_=np.array([i['max'] for i in population['logbook']])
    X = np.arange(len(avg))
    add_figure(cell_name,'generation','error')
    plt.fill_between(X, avg-std, avg+std, alpha=0.25)
    plt.plot(X, avg)
    plt.plot(X, min_)
    plt.plot(X, max_,lw=0.5)
    plt.title(cell_name)
    create_folder_dirr(folder2run+'/moo_errors/')
    copy_file(glob(base_dir+'/cp*'+passive_param+'.tmp')[0],folder2run+'/moo_errors/',extra_name=cell_name)
    plt.savefig(folder2run+'/moo_errors/'+cell_name+'.png')
    plt.show()
if __name__=='__main__':
    for cell_name in read_from_pickle('cells_name2.p'):
        plot_moo_configuration(cell_name)
