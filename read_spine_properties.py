import pandas as pd
from math import pi,sqrt
import numpy as np

def get_n_spinese(cell_name,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    return len(df[df['cell_name']==cell_name])

def get_parameters(cell_name,par_list,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    par=[]
    for par_name in par_list:
        par.append([parameter_cv[par_name][1]])
        if par==[parameter_cv[par_name][1]]:
            print(par_name +"   is empty at Data2.xlx")
    return par
def get_R_head(parameter_cv):
    if not True in list(pd.isna(parameter_cv['R_head'])):
        R_head=np.mean(parameter_cv['R_head'])
    elif not True in list(pd.isna(parameter_cv['head_diam'])):
        R_head=np.mean(parameter_cv['head_diam'])/2
    elif not True in list(pd.isna(parameter_cv['V_head'])):
        V_head=np.mean(parameter_cv['V_head'])
        R_head = (V_head/(4*pi/3))**(1/3) #µm
    elif not True in list(pd.isna(parameter_cv['head_area'])):
        head_area=np.mean(parameter_cv['head_area'])
        R_head=sqrt(head_area/(4*pi))
    return R_head
def get_F_factor_params(spin_type,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==spin_type].reset_index()
    R_head=get_R_head(parameter_cv)
    neck_diam=np.mean(parameter_cv['neck_diam'])
    neck_length=np.mean(parameter_cv['neck_diam'])
    spine_density=np.mean(parameter_cv['spine_density'])
    # if spine_density!=None:
    return R_head,neck_diam,neck_length,spine_density
    return R_head,neck_diam,neck_length

def get_spine_xyz(cell_name,spine_num,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    x=parameter_cv['x'][spine_num]
    y=parameter_cv['y'][spine_num]
    z=parameter_cv['z'][spine_num]
    return (x,y,z)

def get_spine_part(cell_name,spine_num):
    df = pd.read_excel('/cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return parameter_cv['dend_type'][spine_num]
def get_building_spine(cell_name,spine_num):
    df = pd.read_excel('/cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return {'NECK_LENGHT':parameter_cv['neck_length'][spine_num],'NECK_DIAM':parameter_cv['neck_diam'][spine_num],'HEAD_DIAM':get_R_head(parameter_cv)*2}
def get_spine_params(spine_type,cell_name='',folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    # 'groger_spine' 'mouse_spine','human_spine','shaft_spine'
    if spine_type=='groger_spine':
        return get_building_spine(cell_name)['NECK_LENGHT'],get_building_spine(cell_name)['NECK_DIAM'],get_building_spine(cell_name)['HEAD_DIAM']
    else:
        df = pd.read_excel(folder+'/Data2.xlsx')
        parameter_cv=df[df['cell_name']==spine_type].reset_index()
        return parameter_cv['neck_length'],parameter_cv['neck_diam'],get_R_head(parameter_cv)*2
def get_psd(cell_name):
    a=[]
    for i in get_n_spinese(cell_name):
        a.append(get_parameters(cell_name,['PSD'])
    return a
if __name__ == '__main__':
    cell_name='2017_03_04_A_6-7'
    get_parameters(cell_name,['PSD','neck_length'])
    get_F_factor_params('human_spine')
    get_spine_xyz('2017_05_08_A_5-4',0)
