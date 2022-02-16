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

def get_F_factor_params(spin_type,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==spin_type].reset_index()

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
    neck_diam=np.mean(parameter_cv['neck_diam'])
    neck_length=np.mean(parameter_cv['neck_diam'])
    spine_density=np.mean(parameter_cv['spine_density'])
    return R_head,neck_diam,neck_length,spine_density


    return R_head,neck_diam,neck_length

def get_spine_xyz(cell_name,spine_num,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    x=parameter_cv['x'][spine_num]
    y=parameter_cv['y'][spine_num]
    z=parameter_cv['z'][spine_num]
    return (x,y,z)

def get_spine_part(cell_name,spine_num,folder='/ems/elsc-labs/segev-i/moria.fridman/project/analysis_groger_cells/cells_initial_information'):
    df = pd.read_excel(folder+'/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return parameter_cv['dend_type'][spine_num]



if __name__ == '__main__':
    cell_name='2017_03_04_A_6-7'
    get_parameters(cell_name,['PSD','neck_length'])
    get_F_factor_params('human_spine')
    get_spine_xyz('2017_05_08_A_5-4',0)
