import numpy as np
from neuron import h, gui
import sys
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import signal
from find_apic import find_apic
from extra_function import load_hoc,load_ASC, SIGSEGV_signal_arises,create_folder_dirr,create_folders_list
from glob import glob
import pandas as pd
from open_pickle import read_from_pickle
from calculate_F_factor import calculate_F_factor
from read_spine_properties import get_n_spinese
do_calculate_F_factor=True
print("the number of parameters that sys loaded in dendogram.py is ",len(sys.argv),flush=True)
print(len(sys.argv), sys.argv)

if len(sys.argv) != 11:
    print("the function doesn't run with sys.argv",flush=True)
    cell_name= '2017_05_08_A_5-4'
    file_type2read='ASC'
    passive_val={'RA':100.0,'CM':1.0,'RM':10000.0}
    name='RA=120'
    resize_diam_by=1.0
    shrinkage_factor=1.0
    SPINE_START=20
    folder_='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/'
else:
    print("the sys.argv len is correct",flush=True)
    cell_name = sys.argv[1]
    file_type2read=sys.argv[2] #hoc ar ASC
    passive_val={"RA":float(sys.argv[3]),"CM":float(sys.argv[4]),'RM':float(sys.argv[5])}
    name=sys.argv[6]
    resize_diam_by = float(sys.argv[7]) #how much the cell sweel during the electrophisiology records
    shrinkage_factor =float(sys.argv[8]) #how much srinkage the cell get between electrophysiology record and LM
    SPINE_START=int(sys.argv[9])
    folder_= sys.argv[10] #'/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_outputs_data'
print(name, passive_val)

data_dir= "cells_initial_information/"
save_dir ="cells_outputs_data/"
cell_file=glob(folder_+data_dir+cell_name+'/*'+file_type2read)[0]
folder_save=folder_+save_dir+cell_name+"/data/cell_properties/"+file_type2read+'_SPINE_START='+str(SPINE_START)+'/'
folder_save+="/dend*"+str(round(resize_diam_by,2))+'&F_shrinkage='+str(round(shrinkage_factor,2))
folder_save+=name+'_'+str(passive_val)+'/'
create_folder_dirr(folder_save)

colors_dict = {"soma":"black",
               "apical": "blue",
               "oblique":"cyan",
               "trunk":"purple",
               "basal": "red",
               "axon": "green",
               "else": "gold",
               "synapse": "grey"}

signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
if file_type2read=='hoc':
    load_func=load_hoc
elif file_type2read=='ASC':
    load_func=load_ASC

def get_segment_length_lamda(seg):
    """
	return the segment  e_length
	:param seg_len:
	:param RM:
	:param RA:
	:return:
	"""
    sec = seg.sec
    seg_len = sec.L/sec.nseg #micro meter
    d = seg.diam #micro meter
    R_total = 1.0 / seg.g_pas #Rm[cm^2*oum] sce.Ra[cm*oum]
    lamda = np.sqrt((R_total / sec.Ra) * (d / 10000.0) / 4.0) #micro meter
    # return (float(seg_len) / 10000.0) / lamda
    return lamda



def add_sec(self, sec):
    """
    electric dendogram
    :param sec:
    :return:
    """
    sec_length = 0
    for seg in sec:
        sec_length += get_segment_length_lamda(seg)
    parent = h.SectionRef(sec=sec).parent
    self.tree_dendogram_dist[sec] = self.tree_dendogram_dist[parent] + sec_length


def add_sec2(self, sec):
    """
    morpho dendogram
    :param sec:
    :return:
    """
    h.distance(0, 0.5, sec=self.cell.soma)
    self.tree_dendogram_dist[sec] = h.distance(1, sec=sec)

def get_spine_area():
    neck_length=0.78
    neck_diam = 1.64
    head_volume = 0.14
    head_r = (head_volume*3/4/np.pi)**(1/3)
    head_area = 4*np.pi*head_r**3
    neck_area = np.pi * neck_diam * neck_length
    return head_area +neck_area


def change_model_pas(cell,CM=1, RA = 250, RM = 20000.0, E_PAS = -70.0,F_factor=1.9):
    h.dt = 0.1
    h.distance(0,0.5, sec=cell.soma)
    for sec in cell.all_sec():
      sec.Ra = RA
      sec.cm = CM  # *shrinkage_factor    #*(1.0/0.7)
      sec.g_pas = (1.0 / RM)  #*shrinkage_factor  #*(1.0/0.7)
      sec.e_pas = E_PAS
    for sec in cell.dend:
      for seg in sec: #count the number of segment and calclate g_factor and total dend distance,
          if h.distance(seg) > SPINE_START:
              seg.cm *= F_factor
              seg.g_pas *= F_factor
    return cell
# def run_find_apic(apics,last_apic):
#     for child in last_apic.children():
#         apics.append(child)
#         run_find_apic(apics,child)
class Dendogram():
    def __init__(self,
                 name,
                 morph_path,
                 length_function,
                 color_dict = colors_dict,
                 diam_factor=None,
                 del_axon=True,
                 load_func=''):
        self.name=name
        self.colors_dict = color_dict
        self.does_axon_inside_cell=True
        self.cell=None
        if del_axon:
            self.cell = load_func(morph_path)
            self.does_axon_inside_cell=False
        else:
            self.cell = load_func(morph_path,delete_axon=False)
            if len(self.cell.axon)==0:
                self.does_axon_inside_cell=False
                print("cell "+cell_name+ " don't have axons inside")
        for sec in self.cell.all_sec():
            sec.insert('pas')
            sec.nseg = max(int(sec.L), 1)
        if do_calculate_F_factor:
           F_factor=calculate_F_factor(self.cell,'mouse_spine')
        else:
           F_factor = 1.9
        self.cell=change_model_pas(self.cell, CM=passive_val['CM'], RA = passive_val['RA'], RM = passive_val['RM'], E_PAS = E_PAS,F_factor=F_factor)
        self.tree_dendogram_dist = dict()
        self.tree_dendogram_dist[self.cell.soma] = 0
        self.add_sec = length_function
        self.diam_factor=diam_factor
        try: self.apic=self.cell.apic
        except:self.apic= find_apic(self.cell,self.does_axon_inside_cell)
        synapses_dict=pd.read_excel(folder_+save_dir+"synaptic_location_seperate.xlsx",index_col=0)
        synapses_locations=[]
        for i in range(get_n_spinese(cell_name)):
            sec=synapses_dict[cell_name+str(i)]['sec_name']
            seg=float(synapses_dict[cell_name+str(i)]['seg_num'])
            synapses_locations.append([sec,seg])
        self.dots_loc=synapses_locations
        # self.syn = synapses_locations
        # self.dots_loc = np.array([[syn[0],float(syn[1])] for syn in self.syn])
        # self.dots_loc = np.array(dots_loc)
        # self.dots_loc = np.array([[eval('self.cell.'+syn_[0], {'self':self}, {}),syn_[1]] for syn_ in self.syn])

    def cumpute_distances(self, base_sec):
        for sec in h.SectionRef(sec=base_sec).child:
            self.add_sec(self, sec)
            self.cumpute_distances(sec)

    def add_syn(self, sec, seg):
        h.distance(0, 0.5, sec=self.cell.soma)
        self.tree_dendogram_dist[sec] = h.distance(seg, sec=sec)

    def get_color(self, sec):
        if sec in self.cell.apic:
            return self.colors_dict["apical"]
        elif sec in self.cell.dend:
            if sec in self.apic:
                return self.colors_dict["apical"]
            else:
                return self.colors_dict["basal"]
        elif sec in self.cell.soma:
            return self.colors_dict["soma"]
        elif self.does_axon_inside_cell:
            if sec in self.cell.axon:
                return self.colors_dict["axon"]
        else:
            return self.colors_dict["else"]

    def plot_synapse(self, sec_start, sec_end, pos, x_axis):
        print('synapse plot',pos)
        syn_dis=sec_start + abs(sec_end - sec_start) * float(pos)
        plt.scatter(x_axis, syn_dis, color=colors_dict["synapse"])
        plt.annotate('syn distance\n' + str(round(syn_dis,3)),fontsize=10, xy=(x_axis, syn_dis), xycoords='data',
                     xytext=(0.3, 0.5), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.005,lw=0.0005),
                     horizontalalignment='center', verticalalignment='top',
                     )
        return syn_dis
    def plot_func(self, sec, x_pos, color):
        parent = h.SectionRef(sec=sec).parent
        if sec in self.done_section:
            raise BaseException("problem with morph")
        else:
            self.done_section.add(sec)
        sec_name = sec.name()
        sec_name = sec_name[sec_name.find(".") + 1:]
        sec_name = sec_name[sec_name.find(".") + 1:]

        if h.SectionRef(sec=sec).nchild() == 0:
            plt.plot([x_pos, x_pos], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                     linewidth=1 if self.diam_factor is None else sec.diam*self.diam_factor)
            for synapse in self.dots_loc:
                sec_n=synapse[0]
                seg=synapse[1]
                if sec_name == sec_n:
                    dendogram_syn_distance =self.plot_synapse(self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], seg, x_pos)
                    print('synapse dendogram len is ',dendogram_syn_distance)
            return x_pos + 1.0, x_pos

        elif h.SectionRef(sec=sec).nchild() == 1:
            for synapse in self.dots_loc:
                sec_n=synapse[0]
                loc=synapse[1]
                if sec_name == sec_n:
                    self.plot_synapse(self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], loc, x_pos)
            # x_pos+=1
            x_pos, start_pos = self.plot_func(h.SectionRef(sec=sec).child[0], x_pos, color)
            plt.plot([start_pos, start_pos], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                     linewidth=1 if self.diam_factor is None else sec.diam*self.diam_factor)
            return x_pos, start_pos

        x_pos, start_pos = self.plot_func(h.SectionRef(sec=sec).child[0], x_pos, color)
        for i in range(1, int(h.SectionRef(sec=sec).nchild()) - 1, 1):
            x_pos, end_pos = self.plot_func(h.SectionRef(sec=sec).child[i], x_pos, color)

        x_pos, end_pos = self.plot_func(h.SectionRef(sec=sec).child[int(h.SectionRef(sec=sec).nchild()) - 1], x_pos,
                                   color)
        mid_x = start_pos + abs(end_pos - start_pos) / 2.0
        plt.plot([mid_x, mid_x], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                 linewidth=1 if self.diam_factor is None else sec.diam*self.diam_factor)
        plt.plot([start_pos, end_pos], [self.tree_dendogram_dist[sec]] * 2, color=self.get_color(sec), linewidth=1 if self.diam_factor is None else sec.diam*self.diam_factor)
        for sec_n, loc in self.dots_loc:
            if sec_name == sec_n:
                self.plot_synapse(self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], loc, mid_x)

        return x_pos, mid_x

    def plot(self, save_folder, max_y=None,title='Dendogram',ylabel='distance from soma'):
        plt.figure(figsize=(10, 10))
        plt.title(title+'\n'+name+' '+str(passive_val),fontsize=24)
        plt.ylabel(ylabel,fontsize=16)
        x_pos = 0.0
        start_pos=0.0
        self.done_section = set()
        for i in range(0, int(h.SectionRef(sec=self.cell.soma).nchild()), 1):
            sec = h.SectionRef(sec=self.cell.soma).child[i]
            if sec in self.apic:
                x_pos, start_pos = self.plot_func(sec, x_pos, color=self.get_color(sec))
        for i in range(0, int(h.SectionRef(sec=self.cell.soma).nchild()), 1):
            sec = h.SectionRef(sec=self.cell.soma).child[i]
            if sec not in self.apic:
                x_pos, end_pos = self.plot_func(sec, x_pos, color=self.get_color(sec))
        plt.plot([start_pos, end_pos], [0] * 2, color=self.colors_dict["soma"], linewidth=1 if self.diam_factor is None else self.cell.soma.diam *self.diam_factor)
        mid_x = start_pos + abs(end_pos - start_pos) / 2.0
        plt.plot([mid_x, mid_x], [-0.01, 0], color=self.colors_dict["soma"], linewidth=1 if self.diam_factor is None else self.cell.soma.diam *self.diam_factor)
        plt.xticks([])

        legend_elements = [
            Line2D([0], [0], color=self.colors_dict["soma"], lw=2, label="soma"),
            Line2D([0], [0], color=self.colors_dict["apical"], lw=2, label="apical"),
            Line2D([0], [0], color=self.colors_dict["basal"], lw=2, label="basal"),
            Line2D([0], [0], color=self.colors_dict["trunk"], lw=2, label="trunk"),
            Line2D([0], [0], color=self.colors_dict["oblique"], lw=2, label="oblique"),
            Line2D([0], [0], color=self.colors_dict["synapse"], lw=2, label="synapse")
        ]
        plt.legend(handles=legend_elements, loc="best")
        if max_y is None:
            max_y = plt.ylim()[1]
        plt.ylim([-0.1, max_y])
        plt.savefig(save_folder + self.name)
        plt.savefig(save_folder + self.name+ ".pdf")
        plt.close()
        self.done_section = set()
        return max_y

    # def find_apic(self):
    #     print("unsure that there isn't cell.axon that send to find_apic.py or del_axon=False")
    #     last_dend_diam=0
    #     for dend in self.cell.soma.children():
    #         if not self.del_axon and self.does_axon_inside_cell:
    #             if dend in self.cell.axon: continue
    #         if dend.diam>last_dend_diam:
    #             start_apic=dend
    #             last_dend_diam=dend.diam
    #     apics=[start_apic]
    #     run_find_apic(apics,start_apic)
    #     return apics


save_folder_E = folder_save+'/E_dendogram/'
save_folder_M = folder_save+'/M_dendogram/'
create_folders_list([save_folder_E,save_folder_M])


E_PAS=read_from_pickle(folder_+save_dir+cell_name+'/data/electrophysio_records/short_pulse_parameters.p')['E_pas']
# for i in [1,2,3,5,8,9,10,11,12]:
# path = "05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Bluecell_spinec91.ASC"
# syn_poses['05_08_A_01062017_Splice_shrink_FINISHED_LABEL_Bluecell_spinec91']=[(-5.56, -325.88, -451.42)]
morph_path=glob(folder_+data_dir+"/"+cell_name+'/*'+file_type2read)[0]
cell=load_func(morph_path)
# dendogram = Dendogram('dend_only', p, add_sec2)#@#
# dendogram.cumpute_distances(dendogram.cell.soma)#@#
dendogram=None
dendogram = Dendogram('dend_only', morph_path, add_sec2,load_func=load_func)
dendogram.cumpute_distances(dendogram.cell.soma)
max_y=dendogram.plot(save_folder_M,title=save_folder_M.split('/')[-2],ylabel="distance from soma (um)")

dendogram=None
dendogram = Dendogram('all', morph_path, add_sec2, load_func=load_func,del_axon=False)
dendogram.cumpute_distances(dendogram.cell.soma)
max_y = dendogram.plot(save_folder_M,title=save_folder_M.split('/')[-2],ylabel="distance from soma (um)")

dendogram=None
dendogram = Dendogram('dend_only_with_syn', morph_path, add_sec,load_func=load_func, del_axon=False)
dendogram.cumpute_distances(dendogram.cell.soma)
max_y = dendogram.plot(save_folder_E,title=save_folder_E.split('/')[-2],ylabel="distance from soma (lamda)")

dendogram=None
dendogram = Dendogram('all_with_syn', morph_path, add_sec,load_func=load_func)
dendogram.cumpute_distances(dendogram.cell.soma)
max_y = dendogram.plot(save_folder_E,title=save_folder_E.split('/')[-2],ylabel="distance from soma (lamda)")
dendogram=None
print('dendogram.py is complte to run for '+cell_name)
