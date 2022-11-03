import pandas as pd
from math import pi,sqrt
import numpy as np
from open_pickle import read_from_pickle

def calculate_Rneck(cell_name,Ra,spine_num=None):
    L=np.array(get_parameter(cell_name,'neck_length',spine_num))
    R=np.array(get_parameter(cell_name,'neck_diam',spine_num))/2
    #print(L,R)
    if np.size(R)>1:
        R[np.where(R==0)]=1
    else:
        if R==0:
            R=1
    Ra=Ra*10000 #change the units to be in micron
    return (L*Ra/(pi*R**2))/1e6 #in Mega Oum


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
    neck_length=np.mean(parameter_cv['neck_length'])
    spine_density=np.mean(parameter_cv['spine_density'])
    # if spine_density!=None:
    # return R_head,neck_diam,neck_length,spine_density
    return R_head,neck_diam,neck_length

def get_spine_xyz(cell_name,spine_num,before_after='_after_shrink'):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    if "after" in before_after:
        x=parameter_cv['x'][spine_num]
        y=parameter_cv['y'][spine_num]
        z=parameter_cv['z'][spine_num]
    elif "before" in before_after:
        x=parameter_cv['x0'][spine_num]
        y=parameter_cv['y0'][spine_num]
        z=parameter_cv['z0'][spine_num]
    return (x,y,z)

def get_spine_part(cell_name,spine_num):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return parameter_cv['dend_type'][spine_num]

def get_building_spine(cell_name,spine_num):
    df = pd.read_excel('cells_initial_information/Data2.xlsx')
    parameter_cv=df[df['cell_name']==cell_name].reset_index()
    return {'NECK_LENGHT':parameter_cv['neck_length'][spine_num],'NECK_DIAM':parameter_cv['neck_diam'][spine_num],'HEAD_DIAM':get_R_head(cell_name,spine_num)*2}
def get_full_param():
    all_neck_L,all_neck_d,all_PSD,all_PSD_ration=[],[],[],[]
    for cell_name in read_from_pickle('cells_name2.p'):
        if cell_name=='2017_04_03_B':continue
        neck_L=get_parameter(cell_name,'neck_length')
        neck_d=get_parameter(cell_name,'neck_diam')
        PSD=get_parameter(cell_name,'PSD')
        PSD_ration=get_parameter(cell_name,'PSD/spine head')
        all_neck_L=np.append(all_neck_L,neck_L)
        all_neck_d=np.append(all_neck_d,neck_d)
        all_PSD=np.append(all_PSD,PSD)
        all_PSD_ration=np.append(all_PSD_ration,PSD_ration)
    return all_neck_L,all_neck_d,all_PSD,all_PSD_ration
def get_spine_params(spine_type='groger_spine',cell_name=''):
    # 'groger_spine' 'mouse_spine','human_spine','shaft_spine'
    if spine_type=='groger_spine':
        return get_building_spine(cell_name)['NECK_LENGHT'],get_building_spine(cell_name)['NECK_DIAM'],get_building_spine(cell_name)['HEAD_DIAM']
    else:
        df = pd.read_excel('cells_initial_information/Data2.xlsx')
        parameter_cv=df[df['cell_name']==spine_type].reset_index()
        return parameter_cv['neck_length'],parameter_cv['neck_diam'],get_R_head(cell_name,num='list')*2
def get_sec_and_seg(cell_name,spine_num=None,file_type='swc',before_after='_after_shrink',with_distance=False,from_picture=True,special_sec=''):
    #sepcial_sec could be '_1', '_2' .etc
    #this is correct syn to after shrink!
    # df = pd.read_excel('cells_outputs_data_short/'+cell_name+'/synaptic_location_seperate.xlsx',index_col=0)
    if file_type=='swc':
        df=pd.read_excel('cells_initial_information/synaptic_location_seperate.xlsx',index_col=0)
        if from_picture is None:
            if cell_name in read_from_pickle('cells_sec_from_picture.p'):
                from_picture=True
            else:
                from_picture=False
        if from_picture:
            dist_from_soma='dist_from_soma'
            seg_num='seg_num'
        else:
            dist_from_soma='dist_from_soma_from_XYZ_measure'
            seg_num='seg_from_XYZ'
            # df=pd.read_excel('cells_initial_information/synaptic_location_seperate'+before_after+'_swc_section.xlsx',index_col=0)
    else:
        df=pd.read_excel('cells_outputs_data_short/synaptic_location_seperate'+before_after+'.xlsx',index_col=0)
        dist_from_soma='dist_from_soma'
        seg_num='seg_num'

    if not spine_num is None:
        if with_distance:
            return df[cell_name+str(spine_num)+special_sec]['sec_name'],float(df[cell_name+str(spine_num)+special_sec][seg_num]),float(df[cell_name+str(spine_num)+special_sec][dist_from_soma])
        else:
            # print(df[cell_name+str(spine_num)+special_sec]['sec_name'],float(df[cell_name+str(spine_num)+special_sec]['seg_num']))
            return df[cell_name+str(spine_num)+special_sec]['sec_name'],float(df[cell_name+str(spine_num)+special_sec][seg_num])
    else:
        secs,segs,dis=[],[],[]
        for i in range(get_n_spinese(cell_name)):
            secs.append(df[cell_name+str(i)+special_sec]['sec_name'])
            segs.append(float(df[cell_name+str(i)+special_sec][seg_num]))
            dis.append(float(df[cell_name+str(i)+special_sec][dist_from_soma]))
        if with_distance:
            return secs,segs,dis
        else:
            return secs,segs
if __name__ == '__main__': 
    
    from open_pickle import read_from_pickle
    for cell_name in read_from_pickle('cells_name2.p'):
        print(cell_name,get_sec_and_seg(cell_name))
    cell_name='2017_04_03_B'
    print(get_sec_and_seg(cell_name,from_picture=True))
    get_parameter(cell_name,'PSD')
    get_F_factor_params('human_spine')
    get_R_head(cell_name,i=0)
    get_spine_xyz('2017_05_08_A_5-4(0)',0)
    # get_psd(cell_name)
