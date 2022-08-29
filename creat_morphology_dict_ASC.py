import numpy as np
import sys
from glob import glob
import pickle
from extra_function import load_ASC
from open_pickle import read_from_pickle

if len(sys.argv) != 3:
    cell_name=read_from_pickle('cells_name2.p')[0]
    file_type='shrinkXYZ.ASC'

    print('before or after need to be choose')
else:
    cell_name=sys.argv[1]
    file_type=sys.argv[2]
if 'shrinkXYZ' in file_type:
    before_after='_after_shrink'
else:
    before_after='_before_shrink'

folder_="cells_initial_information/"
def run(id, prev_id,sec,type, parent_point=np.array([0, 0, 0]), print_=True):
    global morphology_dict,sec_num
    sec_points = np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,:3]
    sec_diams = np.array([list(i) for i in sec.psection()['morphology']['pts3d']])[:,3]
    if print_:
        print(sec.name(), len(sec.children()))

    sec_points -= sec_points[0] - parent_point
    x,y,z,diam=[],[],[],[]
    for i, point in enumerate(sec_points):
        x.append(point[0].round(4))
        y.append(point[1].round(4))
        z.append(point[2].round(4))
        diam.append(round(sec_diams[i],4))
        prev_id=id
        id+=1
    sec_num+=1
    morphology_dict[sec_num]={'sec name':sec.name().split('.')[-1],'x':x,'y':y,'z':z,'d':diam}

    for child in sec.children():
        id=run(id,prev_id,child, type, parent_point = sec_points[-1] ,print_=print_)
    return id

def get_closest_z(soma_point, sec_point, soma_r):
    # dists = [[np.linalg.norm(point[:3]- sec_point[:3]), point[:3]] for point in soma_points]
    # dists.sort()
    # factor = soma_r/dists[0][0]
    vec = (-soma_point + sec_point[:3])
    vec/=np.linalg.norm(vec)
    return soma_point + vec * soma_r

id=2
fname = glob(folder_+cell_name+'/*'+file_type)[0]

if not 'shrinkXYZ' in file_type and 'shrinkXYZ' in fname:
    fname = glob(folder_+cell_name+'/*'+file_type)[1]


print(fname)

print(fname.split('/')[1])
morphology_dict={}
cell=None
cell=load_ASC(fname)

sec_num=0
soma_points = np.array([list(i) for i in cell.soma.psection()['morphology']['pts3d']]).mean(axis=0)
morphology_dict[sec_num]={'sec name':cell.soma.name().split('.')[-1],'x':round(soma_points[0],4),'y':round(soma_points[1],4),'z':round(soma_points[2],4),'d':round(soma_points[3],4)}


for child in cell.soma.children():

    parent_point = get_closest_z(soma_points[:3],
                                 np.array(child.psection()['morphology']['pts3d'][0])[:3],
                                 soma_r = round(cell.soma.diam/2.0, 4))
    id=run(id,1,child,type, print_=type==2, parent_point=parent_point)



with open(folder_+cell_name+"/dict_morphology/ASC"+before_after+".pickle", 'wb') as handle:
    pickle.dump(morphology_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
cell=None






