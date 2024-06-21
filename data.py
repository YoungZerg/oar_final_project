import pandas as pd
import plotly.express as px
from count_to_reg import country_to_region
url = r"https://docs.google.com/spreadsheets/d/e/2PACX-1vQi1ZPN5BhKaUopcNx2rReTSQ5KvMK6HHmC6J-5lmg5UNqKrU11WNm-4neyl5JAWrZly4ZWdoC57H-D/pub?gid=1752899854&single=true&output=csv"

df = pd.read_csv(url)

all_regions = df[df['Code']=="Region"].copy()

for_drop = ['High income', 'Low and middle income', 'Low income', 'Lower middle income', 'Middle income', 'Upper middle income']
for_drop2 = ['High income',
             'Low and middle income',
             'Low income',
             'Lower middle income',
             'Middle income',
             'Upper middle income',
             'East Asia and Pacific',
             'Europe and Central Asia',
             'European Union',
             'Latin America and Caribbean',
             'Middle East and North Africa',
             'North America',
             'South Asia',
             'Sub-Saharan Africa']

cleaned_regions = all_regions[~all_regions['Entity'].isin(for_drop)].copy()
geo_regions = cleaned_regions['Entity'].unique()


df_c = df.copy()
df_c['Code'] = df_c['Code'].replace('OWID_KOS', 'KOS')
df_c = df_c[~df_c['Code'].isin(['OWID_WRL', 'Region'])].copy()
unique_codes = df_c['Code'].unique()

world_df = df[df['Code'].str.contains('OWID_WRL')].copy()


converted_dataset = df_c.copy()
converted_dataset['Region'] = converted_dataset['Entity'].map(country_to_region)
