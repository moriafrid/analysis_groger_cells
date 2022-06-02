from neuron import h, gui
import numpy as np
import sys
from glob import glob
if len(sys.argv) != 2:
    # cell_name="2017_05_08_A_5-4(0)"
    # cell_name="2017_05_08_A_4-5(0)"
    cell_name="2017_03_04_A_6-7(0)"
else:
    cell_name=sys.argv[1]
folder_="cells_initial_information/"

h.load_file("import3d.hoc")
h.load_file("nrngui.hoc")
h.load_file('stdlib.hoc')
h.load_file("stdgui.hoc")
class Cell: pass
def mkcell(fname):
    #def to read ACS file
  loader = h.Import3d_GUI(None)
  loader.box.unmap()
  loader.readfile(fname)
  c = Cell()
  loader.instantiate(c)
  return c
def instantiate_swc(filename):
    h.load_file('import3d.hoc')
    h('objref cell, tobj')
    h.load_file('allen_model.hoc')
    h.execute('cell = new allen_model()')
    h.load_file(filename)
    nl = h.Import3d_SWC_read()
    nl.quiet = 1
    nl.input(filename)
    i3d = h.Import3d_GUI(nl, 0)
    i3d.instantiate(h.cell)
    return h.cell

# cell=instantiate_swc(folder_+cell_name+'/morphology_z_correct.swc')
# print (cell)
# sp = h.PlotShape()
# sp.show(0)  # show diameters
# a=1
pass
max_dz = 40
def run(id, prev_id,sec,type, parent_point=np.array([0, 0, 0]), print_=True):
    sec_points = np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,:3]
    sec_diams = np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,3]
    if print_:
        print(sec.name(), len(sec.children()))
    acc_z_diff = 0
    for i in range(1, len(sec_points)):
        sec_points[i][2] -= acc_z_diff
        if abs(sec_points[i][2]-sec_points[i-1][2])>max_dz:
            if sec_points[i][2]-sec_points[i-1][2]>0:
                acc_z_diff+=sec_points[i][2]-sec_points[i-1][2]-max_dz
                sec_points[i][2] -= sec_points[i][2]-sec_points[i-1][2]-max_dz
            else:
                acc_z_diff+=sec_points[i][2]-sec_points[i-1][2]+max_dz
                sec_points[i][2]-= sec_points[i][2]-sec_points[i-1][2]+max_dz

    sec_points -= sec_points[0] - parent_point
    for i, point in enumerate(sec_points):
        swc_file.write(str(id)+' '+str(type)+' '+
                       ' '.join(point[:3].round(4).astype(str).tolist()) +
                       ' ' + str(round(sec_diams[i]/ 2.0, 4))+' '+str(prev_id)+'\n')
        prev_id=id
        id+=1
    for child in sec.children():
        id=run(id,prev_id,child, type, parent_point = sec_points[-1] ,print_=print_)
    return id

######################################################
# build the model
######################################################

fname = glob(folder_+cell_name+'/*.ASC')[0]
cell=mkcell(fname)
sp2 = h.PlotShape()
sp2.color_all(3)
sp2.show(0)  # show diameters
soma_points = np.array([list(i) for i in cell.soma[0].psection()['morphology']['pts3d']]).mean(axis=0)
swc_file = open(folder_+cell_name+'/morphology_z_correct.swc', 'w')
swc_file.write('# generated by Vaa3D Plugin sort_neuron_swc\n')
swc_file.write('# source file(s): '+fname+'\n')
swc_file.write('# id,type,x,y,z,r,pid\n')
swc_file.write('1 1 '+
               ' '.join(soma_points[:3].round(4).astype(str).tolist())+
               ' '+str(round(cell.soma[0].diam/2.0, 4))+' -1\n')

def get_closest_z(soma_point, sec_point, soma_r):
    # dists = [[np.linalg.norm(point[:3]- sec_point[:3]), point[:3]] for point in soma_points]
    # dists.sort()
    # factor = soma_r/dists[0][0]
    vec = (-soma_point + sec_point[:3])
    vec/=np.linalg.norm(vec)
    return soma_point + vec * soma_r

id=2
try:cell.axon
except: cell.axon=[]
try:cell.apic
except: cell.apic=[]
for child in cell.soma[0].children():
    type=None
    if child in cell.dend:
        type=3 #2 for dend
    elif child in cell.axon:
        type=2
    elif child in cell.apic:
        type=4

    if "2017_03_04_A_6-7" in cell_name:
        if child==cell.dend[56]:
            type=2
        elif child==cell.axon[0]:
            type=3
    if type is None:
        raise Exception('no type chosen')
    parent_point = get_closest_z(soma_points[:3],
                                 np.array(child.psection()['morphology']['pts3d'][0])[:3],
                                 soma_r = round(cell.soma[0].diam/2.0, 4))
    id=run(id,1,child,type, print_=type==2, parent_point=parent_point)

swc_file.close()
cell=None
cell=instantiate_swc(folder_+cell_name+'/morphology_z_correct.swc')
print (cell)
sp = h.PlotShape()
sp.show(0)  # show diameters
a=1






