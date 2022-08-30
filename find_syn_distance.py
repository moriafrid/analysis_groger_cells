from calculate_F_factor import calculate_F_factor
from function_Figures import find_RA
from extra_function import load_swc
from open_pickle import *
from read_spine_properties import get_sec_and_seg, get_parameter
from neuron import h
from glob import glob
import numpy as np
import sys
if len(sys.argv)!=2:
    number=9
else:
    number=int(sys.argv[1])
cell_name='2017_04_03_B'#read_from_pickle('cells_name2.p')[number]#@need to be run form the consule and the cell number need to be change
print(cell_name)
cell_file=glob('cells_initial_information/'+cell_name+'/*after_shrink.swc')[0]
# cell_file=glob('cells_initial_information/'+cell_name+'/morphology.swc')[0]

cell=load_swc(cell_file)
SPINE_START=20
for sec in cell.all_sec():
    sec.insert('pas')
    sec.nseg = max(int(sec.L), 1)
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


def add_sec(sec):
    """
    electric dendogram
    :param sec:
    :return:
    """
    sec_length = 0
    for seg in sec:
        sec_length += get_segment_length_lamda(seg)
    # parent = h.SectionRef(sec=sec).parent
    # tree_dendogram_dist[sec] = tree_dendogram_dist[parent] + sec_length
    return sec_length

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

base_dir='final_data/total_moo/'+cell_name+'/'
decided_passive_params=find_RA(base_dir)
dict_result=read_from_pickle(glob(base_dir+decided_passive_params+'_pickles.p')[0])['parameter']
for sec,seg in zip(get_sec_and_seg(cell_name,from_picture=False)[0],get_sec_and_seg(cell_name,from_picture=False)[1]):
    sec=eval('cell.'+sec)
    print(h.distance(cell.soma(0.5),sec(seg)))
cell=change_model_pas(cell,CM=dict_result['CM'], RA = dict_result['RA'], RM = dict_result['RM'], E_PAS = dict_result['E_PAS'],F_factor=calculate_F_factor(cell))
i=0
for sec,seg in zip(get_sec_and_seg(cell_name,from_picture=False)[0],get_sec_and_seg(cell_name,from_picture=False)[1]):
    sec= eval('cell.'+sec)
    print(sec,seg)
    print('soma distance:')
    print(h.distance(sec(seg)))
    print(h.distance(sec(0)))
    print(h.distance(sec(1)))

    print(0,h.distance(cell.apic[3](0)))
    print(1,h.distance(cell.apic[3](1)))

    for s in np.arange(0,1.2,0.2):
        print(s,h.distance(cell.apic[7](s)))
    # print('new_seg')
    x=(h.distance(cell.soma(0.5), sec(seg))-get_parameter(cell_name,par_name='dis_from_soma',spine_num=i))
    new_seg=((seg*sec.L)-x)/sec.L
    try:print('')#print(new_seg,h.distance(cell.soma(0.5), sec(new_seg)))
    except:print('the founding segment is too far')

    # print('lambda:')
    sec_t=sec
    sections=[sec_t]
    total_lambda=[add_sec(sec_t)]
    while sec_t!=cell.soma:
        total_lambda.append(add_sec(sec_t))
        sec_t=sec_t.parentseg().sec
        sections.append(sec_t)

    # print(len(sections))
    # print(sum(total_lambda))
    i+=1
