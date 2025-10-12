import pandas as pd
import numpy as np

raw_co2_data_file_path = "raw_data/owid-co2-data.csv"
iso_code_country_data_file_path = "../iso_alpha3_codes.csv"

df_co2 = pd.read_csv(raw_co2_data_file_path, engine='python')
df_iso = pd.read_csv(iso_code_country_data_file_path, engine='python')

# Filter column: country, year, iso_code, co2
df_co2 = df_co2[["country", "year", "iso_code", "co2"]]


# Filter year value >= 2000
df_co2 = df_co2[df_co2["year"] >= 2000]


# Kiểm tra các datapoint không có iso_code (mã quốc gia)
missing_iso = df_co2[df_co2['iso_code'].isna()]['country'].unique()
print("Các country không có iso_code:")
print(missing_iso)

# Các country không có iso_code:
# ['Africa' 'Africa (GCP)' 'Asia' 'Asia (GCP)'
#  'Asia (excl. China and India)' 'Central America (GCP)' 'Europe'
#  'Europe (GCP)' 'Europe (excl. EU-27)' 'Europe (excl. EU-28)'
#  'European Union (27)' 'European Union (28)' 'High-income countries'
#  'International aviation' 'International shipping'
#  'International transport' 'Kosovo' 'Kuwaiti Oil Fires'
#  'Kuwaiti Oil Fires (GCP)' 'Least developed countries (Jones et al.)'
#  'Low-income countries' 'Lower-middle-income countries'
#  'Middle East (GCP)' 'Non-OECD (GCP)' 'North America'
#  'North America (GCP)' 'North America (excl. USA)' 'OECD (GCP)'
#  'OECD (Jones et al.)' 'Oceania' 'Oceania (GCP)' 'Ryukyu Islands'
#  'Ryukyu Islands (GCP)' 'South America' 'South America (GCP)'
#  'Upper-middle-income countries' 'World']
# Nhận xét: Đa số các 'country' không có iso_code đều không phải là quốc gia, ngoại trừ Kosovo là một lãnh thổ tranh chấp với Serbia và không có ISO_Code --> Remove 

# Filter: remove các datapoint không có iso_code vì lý do không phải quốc gia đã phân tích
df_co2 = df_co2[df_co2['iso_code'].notna()]


# Reset index
df_co2.reset_index(drop=True, inplace=True)
df_co2.index = df_co2.index + 1

# Check iso_code
code_df_co2 = set(df_co2['iso_code'].dropna().unique())
code_df_iso = set(df_iso['ISO_Alpha3'].dropna().unique())
invalid_codes = code_df_co2 - code_df_iso
print("Các mã iso_code không hợp lệ:")
print(invalid_codes)

# Thống kê cơ bản
num_of_country = df_co2["iso_code"].nunique()
num_missing = df_co2["co2"].isna().sum()


print("Số quốc gia: ", num_of_country)
print("Số lượng missing value: ",num_missing)

# Export dataframe to csv
df_co2.to_csv("final_co2_data.csv", index=False)


