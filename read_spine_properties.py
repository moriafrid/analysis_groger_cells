import pandas as pd
from math import pi,sqrt
import numpy as np

def get_n_spinese(cell_name):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    return len(df[df['cell_name']==cell_name])

def get_parameter(cell_name,par_name,spine_num=None):
    from math import isnan
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    par=[]
    if spine_num is None:
        for i in range(get_n_spinese(cell_name)):
            par.append(parameter_cv[par_name][i])
            if isnan(parameter_cv[par_name][i]):
                print(par_name +" in "+cell_name+" at place "+str(i)+ "is empty at Data2.xlx")
    else:
        par=parameter_cv[par_name][spine_num]
        if isnan(parameter_cv[par_name][spine_num]):
            print(par_name +" in "+cell_name+ "is empty at Data2.xlx")
    return par

def get_R_head(cell_name,i=None):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    if not True in list(pd.isna(parameter_cv['R_head'])):
        R_head=parameter_cv['R_head']
    elif not True in list(pd.isna(parameter_cv['head_diam'])):
        R_head=parameter_cv['head_diam']/2
    elif not True in list(pd.isna(parameter_cv['V_head'])):
        V_head=parameter_cv['V_head']
        R_head = (V_head/(4*pi/3))**(1/3) #µm
    elif not True in list(pd.isna(parameter_cv['head_area'])):
        head_area=parameter_cv['head_area']
        R_head=np.sqrt(head_area/(4*pi))
    if i==None:
        return np.mean(R_head)
    elif i=='list':
        return R_head
    else:
        return R_head[i]

def get_F_factor_params(spine_type,i=0):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==spine_type].reset_index()
    R_head=get_R_head(spine_type)
    neck_diam=np.mean(parameter_cv['neck_diam'])
    neck_length=np.mean(parameter_cv['neck_diam'])
    spine_density=np.mean(parameter_cv['spine_density'])
    # if spine_density!=None:
    return R_head,neck_diam,neck_length,spine_density
    return R_head,neck_diam,neck_length

def get_spine_xyz(cell_name,spine_num):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    x=parameter_cv['x'][spine_num]
    y=parameter_cv['y'][spine_num]
    z=parameter_cv['z'][spine_num]
    return (x,y,z)

def get_spine_part(cell_name,spine_num):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return parameter_cv['dend_type'][spine_num]

def get_building_spine(cell_name,spine_num):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return {'NECK_LENGHT':parameter_cv['neck_length'][spine_num],'NECK_DIAM':parameter_cv['neck_diam'][spine_num],'HEAD_DIAM':get_R_head(cell_name,spine_num)*2}

def get_spine_params(spine_type,cell_name=''):
    # 'groger_spine' 'mouse_spine','human_spine','shaft_spine'
    if spine_type=='groger_spine':
        return get_building_spine(cell_name)['NECK_LENGHT'],get_building_spine(cell_name)['NECK_DIAM'],get_building_spine(cell_name)['HEAD_DIAM']
    else:
        df = pd.read_excel('cells_initial_information/Data2.xlsx')
        parameter_cv=df[df['cell_name']==spine_type].reset_index()
        return parameter_cv['neck_length'],parameter_cv['neck_diam'],get_R_head(cell_name,num='list')*2
def get_sec_and_seg(cell_name,spine_num=None):
    df = pd.read_excel('cells_outputs_data_short/'+cell_name+'/synaptic_location_seperate.xlsx',index_col=0)
    if not spine_num is None:
        return df[str(spine_num)]['sec_name'],df[str(spine_num)]['seg_num']
    else:
        sec,seg=[],[]
        for i in range(get_n_spinese(cell_name)):
            sec.append(df[str(i)]['sec_name'])
            seg.append(df[str(i)]['seg_num'])
        return sec,seg
if __name__ == '__main__':
    cell_name='2017_03_04_A_6-7(0)'
    get_parameter(cell_name,'PSD')
    get_F_factor_params('human_spine')
    get_R_head(cell_name,i=0)
    get_spine_xyz('2017_05_08_A_5-4(0)',0)
    # get_psd(cell_name)
