# Import the libraries that will be used
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import json
import re

# Read in the data into dataframes and rename the columns
raw_data_file_path = "data/dataset.xlsx"
raw_data_dfs = {}
raw_file_column_names = {
    "hours_worked_2011": ["local authority code", "local authority name", "LSOA code", "employed residents", "<15hrs", "16<30hrs", "31<48 hrs", "49+hrs"],
    "hours_worked_2021": ["local authority code", "local authority name", "LSOA code", "employed residents", "<15hrs", "16<30hrs", "31<48 hrs", "49+hrs"],
    "travel_method_2011": ["local authority code", "local authority name", "LSOA code", "employed residents", "wfh", "underground", "train", "bus", "taxi", "motorcycle", "car driver", "car passenger", "bicycle", "walk", "other"],
    "travel_method_2021": ["local authority code", "local authority name", "LSOA code", "employed residents", "wfh", "underground", "train", "bus", "taxi", "motorcycle", "car driver", "car passenger", "bicycle", "walk", "other"],
    "travel_distance_2011": ["local authority code", "local authority name", "LSOA code", "employed residents", "<2km", "2<5km", "5<10km", "10<20km", "20<30km", "30<40km", "40<60km", "60+km", "wfh", "other"],
    "travel_distance_2021": ["local authority code", "local authority name", "LSOA code", "employed residents", "<2km", "2<5km", "5<10km", "10<20km", "20<30km", "30<40km", "40<60km", "60+km", "wfh", "other"]
}
with pd.ExcelFile(raw_data_file_path) as file:
    for sheet_name in raw_file_column_names:
        print(f"Reading {sheet_name}...")
        raw_data_dfs[sheet_name] = pd.read_excel(
            file, sheet_name=sheet_name, names=raw_file_column_names[sheet_name])
print("Done :)")


# Read the shape file that will allow maps to be made
lsoa_geometries_file_path = "scripts/LSOA_geometries.shp"
lsoa_geometries = gpd.read_file(lsoa_geometries_file_path)

# Merge the dataframes with the shapefile on "LSOA code" so all the dataframes contain a geography column
for df_name, df in raw_data_dfs.items():
    merged_df = df.merge(
        lsoa_geometries[["LSOA code", "geometry"]], on="LSOA code", how="left")

    raw_data_dfs[df_name] = gpd.GeoDataFrame(merged_df, geometry="geometry")

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

# Rename columns
for df_name, df in raw_data_dfs.items():
    df.columns = new_column_names[df_name]


# Define function and regex for rounding to 2DP
def mround(match):
    return "{:.2f}".format(float(match.group()))


pat = re.compile(r"\d+\.\d{3,}")

# Only keep the local_authority_code, local_authority_name, lsoa_code and geometry columns
for df_name, df in tqdm(raw_data_dfs.items()):
    raw_data_dfs[df_name] = df[["local_authority_code",
                                "local_authority_name", "geometry"]]
    raw_data_dfs[df_name] = raw_data_dfs[df_name].dissolve(
        # Merge the shapes by local_authority_name
        by="local_authority_code", aggfunc='first', as_index=False)

    # Convert geometry column to GeoJSON format
    geometry_json = raw_data_dfs[df_name]["geometry"].to_json()
    geometry_dict = json.loads(geometry_json)
    features = geometry_dict['features']
    raw_data_dfs[df_name]["geometry"] = [re.sub(pat, mround, json.dumps(feature['geometry'])) for feature in features]


areas = raw_data_dfs["travel_distance_2021"].rename(
    columns={"local_authority_name": "name", "local_authority_code": "code"})

areas.to_csv("data/local_authority_geometries.csv", index=False)
