import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_field(curr_field="SPINE_PSD_AREA", n_row=4):
    recs = []
    key = curr_field if curr_field in all_results.keys() else "SPINE_PSD_AREA"
    for curr in all_results[key]:
        d = {key: curr["parameters"][key]}
        for i, n in enumerate(curr["results"]["dendrite_names"]):
            d[n] = calc_height(curr["results"]["dendrite_v"][i, :])
        for i, n in enumerate(curr["results"]["spine_names"]):
            d[n] = calc_height(curr["results"]["spine_v"][i, :])
        d["spine_g_nmda"] = calc_height(curr["results"]["spine_conductance_nmda"])
        d["spine_g_ampa"] = calc_height(curr["results"]["spine_conductance_ampa"])
        recs.append(d)
    df = pd.DataFrame.from_records(recs)
    a = list(df.columns)
    a.remove(key)
    a.remove("spine_g_nmda")
    a.remove("spine_g_ampa")
    a.remove("spine_head_psd0-0.5")
    a.remove("spine_head_psd0-1.0")
    plt.figure()
    f, axes = plt.subplots(n_row, int(np.ceil(len(a) // n_row)) + 1, sharex=True)
    for i, curr_n in enumerate(a):
        axes[i % n_row, i // n_row].plot(df[curr_field], df[curr_n])
        if i % n_row == axes.shape[0] - 1:
            axes[i % n_row, i // n_row].set_xlabel(curr_field.replace("_", " ").capitalize())
        axes[i % n_row, i // n_row].set_title("V : " + curr_n.replace("_", " ").capitalize(), fontsize=8)
    plt.tight_layout()
    return df

all_results = pickle.load(open("for_moria" + 'results_pickles.p', 'rb'))
print(all_results.keys())
calc_height = lambda v: v.max() - v.min()

df = plot_field(curr_field="SPINE_PSD_AREA")
df2 = plot_field(curr_field="dend_ra")
df3 = plot_field(curr_field="dend_rm")
df4 = plot_field(curr_field="synapse_w_ampa")
df5 = plot_field(curr_field="synapse_w_nmda")
# df6 = plot_field(curr_field="spine_g_ampa")  # cant change gmax in the mods => todo this is missing
plt.show()
print("")