from utils import *
import json
import lightgbm as lgb
import numpy as np
import pandas as pd
from datetime import datetime

###################################################
####################################################
# Input
air_pollution = "no2"
with_o3 = True
if_union = True
if_tc = False
single_site_code = 'MY1'
csv_path = "MaryleboneRoad.csv"
#####################################################
#####################################################

# Functions
def extract_year(row):
    date_unix = int(row["date_unix"])
    return datetime.utcfromtimestamp(date_unix).year


def extract_siteInfo(row, site_info_dict, colname):
    ap_code = row["ap_code"]

    return site_info_dict[ap_code][colname]


if with_o3:
    o3_str = "with_o3"
else:
    o3_str = "without_o3"

if if_union:
    output_path = air_pollution + "_union_" + o3_str + "_" + csv_path
    model_path = "models/" + o3_str + "/" + air_pollution + "_model.txt"
else:
    output_path = air_pollution +"_"+single_site_code + "_single_" + o3_str + "_" + csv_path
    model_path = "models/single_model/"+ air_pollution +"_"+single_site_code+"_"+o3_str+ "_single_model.txt"

data_fill_path = "configs/" + air_pollution + "_unionSites_" + o3_str + "_median.json"

if if_tc:
    if air_pollution != 'no2':
        raise ValueError
    if not with_o3:
        raise ValueError
    if if_union:
        raise ValueError
    if single_site_code!='MY1':
        raise ValueError
    output_path = "no2_MY1_single_with_o3_tc_MaryleboneRoad.csv"
    model_path = "models/single_model/no2_MY1_with_o3_tc_single_model.txt"

if not with_o3:
    if "o3" in continuous_variables:
        continuous_variables.remove("o3")
if with_o3:
    if "o3" not in continuous_variables:
        continuous_variables.append("o3")
    if "o3" in air_pollutions:
        air_pollutions.remove("o3")


features_names = continuous_variables + category_variables

# Opening JSON file
with open(data_fill_path) as json_file:
    data_fill = json.load(json_file)

model = lgb.Booster(model_file=model_path)
df_csv = pd.read_csv(csv_path)


# data preprocess steps
df_csv["year"] = df_csv.apply(lambda row: extract_year(row), axis=1)


if "code" in df_csv.columns and "ap_code" not in df_csv.columns:
    df_csv = df_csv.rename(columns={"code": "ap_code"})


if not if_union:
    df_csv = df_csv[df_csv['ap_code']==single_site_code]


for colname in site_info_columns:
    df_csv[colname] = df_csv.apply(
        lambda row: extract_siteInfo(row, site_info_dict, colname), axis=1
    )

for ap_code in np.unique(df_csv["ap_code"]):

    for colname in continuous_variables:
        condition = df_csv["ap_code"] == ap_code
        df_csv.loc[condition, colname] = df_csv.loc[condition, colname].fillna(
            data_fill[ap_code][colname]
        )


for c in category_variables:
    if c in df_csv.columns:
        df_csv[c] = df_csv[c].astype("category")

if not if_union:
    for item in site_info_columns+['ap_code']:
        if item in features_names:
            features_names.remove(item)

if if_tc:
    features_names.append('tc')

print (features_names)
y_predicts = model.predict(df_csv[features_names])
df_csv[air_pollution + "_predict"] = y_predicts
df_csv.to_csv(output_path, sep=',', index=False)
