from open_pickle import read_from_pickle
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd
from extra_fit_func import find_short_pulse_edges
folder_='cells_outputs_data_short/'
folder_data='cells_initial_information/'
all_data=[]
for cell_name in read_from_pickle('cells_name2.p'):
    pulse=read_from_pickle(glob(folder_+cell_name+'/data/electrophysio_records/short_pulse/mean_short_pulse.p')[0])[0]
    plt.plot(pulse)
    if cell_name not in ['2017_04_03_B','2016_05_12_A','2016_04_16_A','2017_03_04_A_6-7']:
        start,end=find_short_pulse_edges(pulse)
        plt.scatter([start,end],[pulse[start],pulse[end]],label=str([start,end]))
        plt.close()
        # plt.show()
    else:
        plt.show()
        start=int(input('where the pulse start'))
        end=int(input('where the pulse end'))
        plt.plot(pulse)
        plt.scatter([start,end],[pulse[start],pulse[end]],label=str([start,end]))
        plt.show()

    len=end-start
    dict_for_records={}
    dicty={'start':start,'end':end,'len':len}
    dict_for_records['cell_name']=cell_name
    dict_for_records.update(dicty)
    all_data.append(dict_for_records)
    output_df = pd.DataFrame.from_records(all_data)
    output_df.to_csv(folder_+"short_pulse_edges.csv", index=False)



