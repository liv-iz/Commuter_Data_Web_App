# Import the libraries that will be used
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm

# Read in the data into dataframes and rename the columns
data_file_path = Path.cwd() / "data/dataset_prepared.xlsx"
data_dfs = {}
new_column_names = {
    "hours_worked_2011": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "less_than_15", "between_16_and_30", "between_31_and_48", "more_than_48", "geometry"],
    "hours_worked_2021": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "less_than_15", "between_16_and_30", "between_31_and_48", "more_than_48", "geometry"],
    "travel_method_2011": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "work_from_home", "underground", "train", "bus", "taxi", "motorcycle", "car_driver", "car_passenger", "bicycle", "walk", "other", "geometry"],
    "travel_method_2021": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "work_from_home", "underground", "train", "bus", "taxi", "motorcycle", "car_driver", "car_passenger", "bicycle", "walk", "other", "geometry"],
    "travel_distance_2011": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "less_than_2", "between_3_and_5", "between_6_and_10", "between_11_and_20",
                             "between_21_and_30", "between_31_and_40", "between_41_and_60", "more_than_60", "work_from_home", "other", "geometry"],
    "travel_distance_2021": ["local_authority_code", "local_authority_name", "lsoa_code", "employed_residents", "less_than_2", "between_3_and_5", "between_6_and_10", "between_11_and_20",
                             "between_21_and_30", "between_31_and_40", "between_41_and_60", "more_than_60", "work_from_home", "other", "geometry"]
}
with pd.ExcelFile(data_file_path) as file:
    for sheet_name in new_column_names:
        print(f"Reading {sheet_name}...")
        data_dfs[sheet_name] = pd.read_excel(
            file, sheet_name=sheet_name, names=new_column_names[sheet_name])
print("Done :)")

for df_name, df in data_dfs.items():
    df['census_year'] = 2011 if df_name in ['hours_worked_2011',
                                            'travel_method_2011', 'travel_distance_2011'] else 2021

table_mapping = {
    "hours_worked_2011": "hours",
    "hours_worked_2021": "hours",
    "travel_method_2011": "travel_method",
    "travel_method_2021": "travel_method",
    "travel_distance_2011": "travel_distance",
    "travel_distance_2021": "travel_distance"
}

data_file_path = Path.cwd() / "data/local_authority_geometries.csv"
areas = pd.read_csv(data_file_path)

engine = create_engine("sqlite:///instance/project.db", echo=False)
for df_name, df in tqdm(data_dfs.items()):
    df.to_sql(table_mapping[df_name], con=engine, if_exists="append", index=False)

areas.to_sql("local_authority", con=engine, if_exists="append", index=False)
