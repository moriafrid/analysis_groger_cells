# check the results:
from extra_function import load_ASC,SIGSEGV_signal_arises,load_swc
from glob import glob
import signal
from neuron import gui,h
signal.signal(signal.SIGSEGV, SIGSEGV_signal_arises)
cell=None
cell_name='6-7'
for type in ['correct.swc']:
    print(glob('cells_initial_information/2017*'+cell_name+'/*'+type)[0])
    cell=load_swc(glob('cells_initial_information/2017*'+cell_name+'/*'+type)[0])
sp = h.PlotShape()
sp.show(0)  # show diameters
import numpy as np
import matplotlib.pyplot as plt
def get_z_jump(sec, prev_z,place=2):
    res = []
    for z in np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,place]:
        res.append(abs(z-prev_z))
        prev_z=z
    for child in sec.children():
        res+=get_z_jump(child, prev_z)
    return res
# def get_jump(sec, prev):
#     res_x,res_y,res_z = [],[],[]
#     print(prev)
#     prev_x,prev_y,prev_z=np.array(prev)
#     for x,y,z in zip([np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,0],np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,1],np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,2]]):
#         res_x.append(abs(x-prev_x))
#         prev_x=x
#         res_y.append(abs(y-prev_y))
#         prev_y=y
#         res_z.append(abs(z-prev_z))
#         prev_z=z
#     prev=[prev_x,prev_y,prev_z]
#     for child in sec.children():
#         result=get_jump(child, prev)
#         res_x+=result[0]
#         res_y+=result[1]
#         res_z+=result[2]
#
#     return [res_x,res_y,res_z]
plt.figure()
plt.title(cell_name)
res_x=[]
mean_soma_x = np.array(cell.soma.psection()['morphology']['pts3d'])[:,0].mean()
for child in cell.soma.children():
    res_x+=get_z_jump(child, mean_soma_x,place=0)
plt.scatter([0]*len(res_x), res_x,label='scatter x '+str(len(res_x)))

res_y=[]
mean_soma_y=np.array(cell.soma.psection()['morphology']['pts3d'])[:,1].mean()
for child in cell.soma.children():
    res_y+=get_z_jump(child, mean_soma_y,place=1)
plt.scatter([0]*len(res_y), res_y,label='scatter y '+str(len(res_y)))

res_z=[]
mean_soma_z = np.array(cell.soma.psection()['morphology']['pts3d'])[:,2].mean()
for child in cell.soma.children():
    res_z+=get_z_jump(child, mean_soma_z)
plt.scatter([0]*len(res_z), res_z,label='scatter z '+str(len(res_z)))
plt.legend()
plt.figure()
plt.scatter([0]*len(res_z), res_z,label='scatter z')

plt.legend()
plt.show()
# mean_soma = np.array(cell.soma.psection()['morphology']['pts3d'])[:,:3].mean(axis=0)
# res_x,res_y,res_z = [],[],[]
# for child in cell.soma.children():
#     result=get_jump(child, mean_soma)
#     res_x+=result[0]
#     res_y+=result[1]
#     res_z+=result[2]
# plt.scatter([0]*len(res), res)
