from utiles import *
import pickle,os
import numpy as np
import matplotlib.pyplot as plt

def close_event():
    plt.close()

base_dir="traces_for_peeling_new2/"
base_dir_save="traces_for_peeling_new2/"

try:
    os.mkdir(base_dir_save)
except:pass

dt = 0.025
fig, ax = plt.subplots(1, 1)
timer = fig.canvas.new_timer(interval=2000)
timer.add_callback(close_event)
for cell in ["171101HuSHS2C2IN0toIN1", "171101HuSHS2C2IN0toIN3", "171101HuSHS2C2IN3toIN1", "180207HuSHS4C2IN1toIN0"]:
    # if not cell == "171101HuSHS2C2IN0toIN3": continue

    print(cell)
    try:
        os.mkdir(base_dir_save+cell)
    except:
        pass
    print(cell)
    with open(base_dir+cell+"_data.p", 'rb') as handle:
        data = pickle.load(handle)
    dt = data["T"][1]-data["T"][0]
    filterd_traces_first = data["V"]
    filterd_traces_first = []
    for trace in data["V"]:
        for trace1 in data["V"]:
            base_line = trace1[:100].mean()
            plt.plot(np.arange(0, len(trace1)*dt,dt), trace1-base_line-70, color="k")
        base_line = trace[:100].mean()
        plt.plot(np.arange(0, len(trace)*dt,dt),trace-base_line-70, color="r")
        timer.start()
        plt.show()

        check = input('is the trace good bad or ugly? (good=enter)')
        pas = np.mean(trace[:100])
        if check == '':
            filterd_traces_first.append(trace-pas-70)
        # filterd_traces_first.append(trace)
    filterd_traces_first = np.array(filterd_traces_first)
    np.savetxt(base_dir_save+cell+"/peeling.txt", np.array([np.arange(0, len(filterd_traces_first[0])*dt,dt), np.mean(filterd_traces_first,axis=0).flatten()]).T)

    with open(base_dir_save +cell +"_data.p", 'wb') as handle:
        pickle.dump({"T":data["T"],"V":filterd_traces_first}, handle, protocol=pickle.HIGHEST_PROTOCOL)



