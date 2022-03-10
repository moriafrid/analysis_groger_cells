import numpy as np
def get_passive_val(passive_val_dict):
    RA=passive_val_dict['RA']
    CM=passive_val_dict['CM']
    RM=passive_val_dict['RM']
    return str(RA),str(CM),str(RM)
def found_min_parameter(list_dicts,parameter='CM'):
    temp_dict=list_dicts[0]
    for passive_val_dict in list_dicts:
        if passive_val_dict[parameter]<temp_dict[parameter]:
            temp_dict=passive_val_dict
    return temp_dict
def get_RA(passive_val_dict):
    return(passive_val_dict['RA'])

def get_error(passive_val_dict):
    return(passive_val_dict['error'])

def found(list_dicts,RA_num):
    return_dict=None
    for i in [0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,-7,7,-8,8,-9,9,-10,10]:
        for dict_temp in list_dicts:
            if round(get_RA(dict_temp))==RA_num+i:
                return_dict= dict_temp
            if not return_dict is None:
                return(dict_temp)
    raise "dict with RA="+str(RA_num)+'+-10 is not found'

def found_best_RA(list_dicts,max_error=0.1):
    last_dict_temp=list_dicts[0]
    i=0
    while get_error(last_dict_temp)<=max_error:
        # print(get_error(last_dict_temp)<=max_error)
        dict_temp=list_dicts[i]
        if get_RA(dict_temp)>get_RA(last_dict_temp):
            last_dict_temp=dict_temp
            # print(last_dict_temp)
        i+=1
    else:
        return last_dict_temp

def mean_best_n(list_dicts,n):
    RA,RM,CM,error=[],[],[],[]
    for i in range(n):
        RA.append(list_dicts[i]['RA'])
        RM.append(list_dicts[i]['RM'])
        CM.append(list_dicts[i]['CM'])
        error.append(list_dicts[i]['error'])
    print('std from '+str(n)+' best solution is ',{'RA':np.std(RA),'RM':np.std(RM),'CM':np.std(CM),'error':np.std(error)})
    return {'RA':np.mean(RA),'RM':np.mean(RM),'CM':np.mean(CM),'error':np.mean(error)}
