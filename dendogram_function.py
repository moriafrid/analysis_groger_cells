import numpy as np
from neuron import h
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import signal
from find_apic import find_apic
from extra_function import load_swc, SIGSEGV_signal_arises
from glob import glob
from open_pickle import read_from_pickle
from calculate_F_factor import calculate_F_factor
from read_spine_properties import get_n_spinese, get_sec_and_seg
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'
do_calculate_F_factor=True
from function_Figures import text_size,fontsize
colors_dict = {"soma":"black",
               "apical": "blue",
               "oblique":"cyan",
               "trunk":"purple",
               "basal": "red",
               "axon": "green",
               "else": "gold",
               "synapse": "grey"}
SPINE_START=20
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
addlw=0

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
    return (float(seg_len) / 10000.0) / lamda
    # return lamda



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

class Dendogram():
    def __init__(self,
                 name,
                 morph_path,
                 length_function,
                 cell_name='',
                 double_spine='False',
                 color_dict = colors_dict,
                 diam_factor=None,
                 del_axon=True,
                 load_func=load_swc,
                 E_PAS=-70,
                 passive_val={}):
        self.name=name
        self.colors_dict = color_dict
        self.E_PAS=E_PAS
        self.passive_val=passive_val
        self.does_axon_inside_cell=True
        self.cell=None
        if del_axon:
            self.cell = load_func(morph_path)
            self.does_axon_inside_cell=False
        else:
            self.cell = load_func(morph_path,delete_axon=False)
            if len(self.cell.axon)==0:
                self.does_axon_inside_cell=False
        for sec in self.cell.all_sec():
            sec.insert('pas')
            sec.nseg = max(int(sec.L), 1)
        if do_calculate_F_factor:
           F_factor=calculate_F_factor(self.cell,double_spine=double_spine)
        else:
           F_factor = 1.9
        self.cell=change_model_pas(self.cell, CM=self.passive_val['CM'], RA = self.passive_val['RA'], RM = self.passive_val['RM'], E_PAS = self.E_PAS,F_factor=F_factor)
        self.tree_dendogram_dist = dict()
        self.tree_dendogram_dist[self.cell.soma] = 0
        self.add_sec = length_function
        self.diam_factor=diam_factor
        try: self.apic=self.cell.apic
        except:self.apic= find_apic(self.cell,self.does_axon_inside_cell)
        synapses_locations=[]
        for i in range(get_n_spinese(cell_name)):
            sec,seg=get_sec_and_seg(cell_name,i)
            synapses_locations.append([sec,seg])
        self.dots_loc=synapses_locations

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

    def plot_synapse(self,ax, sec_start, sec_end, pos, x_axis):
        print('synapse plot',pos)
        syn_dis=sec_start + abs(sec_end - sec_start) * float(pos)
        ax.scatter(x_axis, syn_dis, color=colors_dict["synapse"],lw=2+addlw)
        x_place=x_axis/100
        # y_place=syn_dis/sum(ax.get_ylim())+0.5
        y_place=0.8
        ax.annotate(str(round(syn_dis,3)),fontsize=10, xy=(x_axis, syn_dis), xycoords='data',
                     xytext=(x_place, y_place), textcoords='axes fraction',
                     arrowprops=dict(facecolor='black', shrink=0.005,lw=0.00005),
                     horizontalalignment='center', verticalalignment='top',
                     )

        return syn_dis
    def plot_func(self, ax,sec, x_pos, color):
        parent = h.SectionRef(sec=sec).parent
        if sec in self.done_section:
            raise BaseException("problem with morph")
        else:
            self.done_section.add(sec)
        sec_name = sec.name()
        sec_name = sec_name[sec_name.find(".") + 1:]
        sec_name = sec_name[sec_name.find(".") + 1:]

        if h.SectionRef(sec=sec).nchild() == 0:
            ax.plot([x_pos, x_pos], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                     linewidth=1+addlw if self.diam_factor is None else sec.diam*self.diam_factor)
            for synapse in self.dots_loc:
                sec_n=synapse[0]
                seg=synapse[1]
                if sec_name == sec_n:
                    dendogram_syn_distance =self.plot_synapse(ax,self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], seg, x_pos)
                    print('synapse dendogram len is ',dendogram_syn_distance)
            return x_pos + 1.0, x_pos

        elif h.SectionRef(sec=sec).nchild() == 1:
            for synapse in self.dots_loc:
                sec_n=synapse[0]
                loc=synapse[1]
                if sec_name == sec_n:
                    self.plot_synapse(ax,self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], loc, x_pos)
            # x_pos+=1
            x_pos, start_pos = self.plot_func(ax,h.SectionRef(sec=sec).child[0], x_pos, color)
            ax.plot([start_pos, start_pos], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                     linewidth=1+addlw if self.diam_factor is None else sec.diam*self.diam_factor)
            return x_pos, start_pos

        x_pos, start_pos = self.plot_func(ax,h.SectionRef(sec=sec).child[0], x_pos, color)
        for i in range(1, int(h.SectionRef(sec=sec).nchild()) - 1, 1):
            x_pos, end_pos = self.plot_func(ax,h.SectionRef(sec=sec).child[i], x_pos, color)

        x_pos, end_pos = self.plot_func(ax,h.SectionRef(sec=sec).child[int(h.SectionRef(sec=sec).nchild()) - 1], x_pos,
                                   color)
        mid_x = start_pos + abs(end_pos - start_pos) / 2.0
        ax.plot([mid_x, mid_x], [self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec]], color=self.get_color(sec),
                 linewidth=1+addlw if self.diam_factor is None else sec.diam*self.diam_factor)
        ax.plot([start_pos, end_pos], [self.tree_dendogram_dist[sec]] * 2, color=self.get_color(sec), linewidth=1+addlw if self.diam_factor is None else sec.diam*self.diam_factor)
        for sec_n, loc in self.dots_loc:
            if sec_name == sec_n:
                self.plot_synapse(ax,self.tree_dendogram_dist[parent], self.tree_dendogram_dist[sec], loc, mid_x)

        return x_pos, mid_x

    def plot(self, ax, max_y=None,title='Dendogram',ylabel='distance from soma'):
        ax.set_ylabel(ylabel,fontsize=16)
        x_pos = 0.0
        start_pos=0.0
        self.done_section = set()
        for i in range(0, int(h.SectionRef(sec=self.cell.soma).nchild()), 1):
            sec = h.SectionRef(sec=self.cell.soma).child[i]
            if sec in self.apic:
                x_pos, start_pos = self.plot_func(ax,sec, x_pos, color=self.get_color(sec))
        for i in range(0, int(h.SectionRef(sec=self.cell.soma).nchild()), 1):
            sec = h.SectionRef(sec=self.cell.soma).child[i]
            if sec not in self.apic:
                x_pos, end_pos = self.plot_func(ax,sec, x_pos, color=self.get_color(sec))
        ax.plot([start_pos, end_pos], [0] * 2, color=self.colors_dict["soma"], linewidth=1+addlw if self.diam_factor is None else self.cell.soma.diam *self.diam_factor)
        mid_x = start_pos + abs(end_pos - start_pos) / 2.0
        ax.plot([mid_x, mid_x], [-0.01, 0], color=self.colors_dict["soma"], linewidth=1+addlw if self.diam_factor is None else self.cell.soma.diam *self.diam_factor)
        ax.set_xticks([])

        # legend_elements = [
        #     Line2D([0], [0], color=self.colors_dict["soma"], lw=2, label="soma"),
        #     Line2D([0], [0], color=self.colors_dict["apical"], lw=2, label="apical"),
        #     Line2D([0], [0], color=self.colors_dict["basal"], lw=2, label="basal"),
        #     Line2D([0], [0], color=self.colors_dict["trunk"], lw=2, label="trunk"),
        #     Line2D([0], [0], color=self.colors_dict["oblique"], lw=2, label="oblique"),
        #     Line2D([0], [0], color=self.colors_dict["synapse"], lw=2, label="synapse")
        # ]
        legend_elements = [
            Line2D([0], [0], color=self.colors_dict["apical"], lw=2, label="apical"),
            Line2D([0], [0], color=self.colors_dict["basal"], lw=2, label="basal"),
        ]
        ax.legend(handles=legend_elements, loc="best")
        if max_y is None:
            max_y = ax.get_ylim()[1]
        ax.set_ylim([-0.1, max_y])


        self.done_section = set()
        ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_position('zero')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        return max_y

def func_dendogram(ax,dirr,type='E_dendogram',with_axon=False):
    cell_name=dirr.split('/')[2]
    file_type2read='z_correct.swc'
    morph_path=glob("cells_initial_information/"+cell_name+'/*'+file_type2read)[0]
    cell=load_swc(morph_path)
    dicty=read_from_pickle(dirr)
    E_PAS=dicty['parameters']['E_PAS']
    passive_val={'RA':dicty['parameters']['RA'],'CM':dicty['parameters']['CM'],'RM':dicty['parameters']['RM']}
    kwargs={'cell_name':cell_name,'load_func':load_swc,'E_PAS':E_PAS,'passive_val':passive_val}
    dendogram=None
    if type=='M_dendogram':

        if len(cell.axon)>1 and with_axon:
            dendogram = Dendogram('all', morph_path, add_sec2,cell_name=cell_name, del_axon=False,**kwargs)
            dendogram.cumpute_distances(dendogram.cell.soma)
            max_y = dendogram.plot(ax,ylabel="distance from soma (um)")
        else:
            dendogram = Dendogram('dend_only', morph_path, add_sec2,**kwargs)
            dendogram.cumpute_distances(dendogram.cell.soma)
            max_y=dendogram.plot(ax,ylabel="distance from soma (um)")
    elif type=='E_dendogram':
        if len(cell.axon)>1 and with_axon:
            dendogram = Dendogram(ax,'all_with_syn', morph_path, add_sec, del_axon=False,**kwargs)
            dendogram.cumpute_distances(dendogram.cell.soma)
            max_y = dendogram.plot(ax,ylabel="distance from soma (lamda)")
            dendogram=None
        else:
            dendogram = Dendogram('dend_only_with_syn', morph_path, add_sec,**kwargs)
            dendogram.cumpute_distances(dendogram.cell.soma)
            max_y = dendogram.plot(ax,ylabel="distance from soma (lamda)")
    cell=None
    print('dendogram.py is complete to run for '+cell_name)

if __name__=='__main__':
    fig,ax=plt.subplots()
    cell_name=read_from_pickle('cells_name2.p')[-1]
    dirr='final_data/'+cell_name+'/Rins_pickles_full_relative_RA_best_fit.p'
    func_dendogram(ax,dirr)
    plt.show()
