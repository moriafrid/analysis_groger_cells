import pandas as pd
def get_passive_parameter(cell_name,spine_start=20,fit_condition='const_param',file_type='z_correct.swc'):
    p='cells_initial_information/'+cell_name+'/results_passive_fits.csv'
    df = pd.read_csv(p)
    #creat the value to run on
    df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type), :].to_dict('records')
    curr = df.loc[(df["fit_condition"] == fit_condition) & (df["file_type"] == file_type)&(df["spine_start"] == spine_start), :]
    passive_vals_dict={}
    for name in curr.parameter_type:
        passive_vals_dict[name]= curr.loc[df.parameter_type == name,].to_dict('records')[0]
    return passive_vals_dict
