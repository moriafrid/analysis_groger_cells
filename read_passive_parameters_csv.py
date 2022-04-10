import pandas as pd
def get_passive_parameter(cell_name,double_spine_area='False',shrinkage_resize=[1.0,1.0],
                          spine_start=20,fit_condition='const_param',file_type='z_correct.swc',passive_param_name=None):
    print(shrinkage_resize)
    p='cells_initial_information/'+cell_name+'/results_passive_fits.csv'
    df = pd.read_csv(p)
    #creat the value to run on
    df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type), :].to_dict('records')

    if eval(double_spine_area):
        curr = df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type)&(df["spine_start"] == spine_start)&(df['shrinkage&resize_factors']==str(shrinkage_resize))&(df['double_spine_area']==eval(double_spine_area)), ]
    else:
        curr = df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type)&(df["spine_start"] == spine_start)&(df['shrinkage&resize_factors']==str(shrinkage_resize)), ]

    if passive_param_name is not None:
        return curr.loc[df.parameter_type == passive_param_name,:].to_dict('records')[0]

    else:
        passive_vals_dict={}
        for name in curr.parameter_type:
            passive_vals_dict[name]= curr.loc[df.parameter_type == name,:].to_dict('records')[0]
        return passive_vals_dict
