import glob
import os
import pandas as pd
import pickle
import numpy as np

if __name__ == '__main__':
    files = glob.glob("C:\\Users\\sapir\\Downloads\\d\\*.p")
    output_csv = os.path.join("C:\\Users\\sapir\\Downloads\\d", "simulation_results.csv")
    print(files)
    ra0str_to_number = lambda str_value: str_value.replace("RA0=", "")
    is_float = lambda str_of_num: str_of_num.replace('.', '', 1).isdigit()
    contents = [pickle.load(open(f, 'rb')) for f in files]
    flat_records = []
    for c in contents:
        for ra0 in c.keys():
            record = c[ra0]  # dict with {CM, RM, RA, error list}
            record["RA0"] = float(ra0str_to_number(ra0)) if is_float(ra0str_to_number(ra0)) else np.nan
            record["error_decay"] = record["error"][0]
            record["error_percentage"] = record["error"][1]
            record["error_rmsd"] = record["error"][2]
            record.pop("error")  # remove error (was replaced by specific values)
            flat_records.append(record)
    output_df = pd.DataFrame.from_records(flat_records)
    print(output_df.columns)
    print(output_df)
    output_df.to_csv(output_csv, index=False)
    print("Save dataframe to ", output_csv)
