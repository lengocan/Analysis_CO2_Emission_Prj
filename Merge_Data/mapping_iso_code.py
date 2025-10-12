import pandas as pd
import re

def normalize_country_name(name):
    return re.sub(r'[^a-z0-9]', '', str(name).lower())

deforestation_file_path = "Ha_Data/deforestation.csv"
iso_code_file_path = "iso_alpha3_codes.csv"

df_deforest = pd.read_csv(deforestation_file_path, engine='python')
df_iso_code = pd.read_csv(iso_code_file_path, engine='python')

df_deforest['_country_norm'] = df_deforest['country'].apply(normalize_country_name)
df_iso_code['_country_norm'] = df_iso_code['Country'].apply(normalize_country_name)

df_mapped = pd.merge(
    df_deforest,
    df_iso_code[['_country_norm', 'ISO_Alpha3']],
    on='_country_norm',
    how='left'
)

df_mapped = df_mapped.drop(columns=['_country_norm'])
df_mapped = df_mapped[['country', 'area_ha', 'Year', 'Deforestation', 'ISO_Alpha3']]
df_mapped = df_mapped.rename(columns={
    'ISO_Alpha3': 'iso_code',
})

missing_iso = df_mapped[df_mapped['iso_code'].isna()]

# In ra tên country chưa có iso_code
print(missing_iso['country'].unique())

hardcode_iso = {
    'Bolivia': 'BOL',
    'Brunei': 'BRN',
    'Democratic Republic of the Congo': 'COD',
    'Iran': 'IRN',
    'Laos': 'LAO',
    'Micronesia': 'FSM',
    'México': 'MEX',
    'North Korea': 'PRK',
    'Palestine': 'PSE',
    'Republic of the Congo': 'COG',
    'Russia': 'RUS',
    'South Korea': 'KOR',
    'Swaziland': 'SWZ',
    'Syria': 'SYR',
    'São Tomé and Príncipe': 'STP',
    'Tanzania': 'TZA',
    'Turkey': 'TUR',
    'Venezuela': 'VEN',
    'Åland': 'ALA'
}
for country, code in hardcode_iso.items():
    df_mapped.loc[df_mapped['country'] == country, 'iso_code'] = code

missing_iso = df_mapped[df_mapped['iso_code'].isna()]

# In ra tên country chưa có iso_code
print(missing_iso['country'].unique())

df_mapped.to_csv('Ha_Data/deforestation_mapped_iso_code.csv',index=False)