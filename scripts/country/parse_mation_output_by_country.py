import os
import datetime

import pandas as pd

def parse_df_create_dirs(df):
    for _, row in df.iterrows():
        country = row['Country']
        dir_path = f'scripts/country/output/{country}'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def parse_df_into_country(df):
    dfs = {}

    for _, row in df.iterrows():
        if row['Country'] not in dfs:
            dfs.update({row['Country']: pd.DataFrame(columns=df.columns)})

        dfs[row['Country']] = pd.concat([dfs[row['Country']], pd.DataFrame([row])], ignore_index=True)

    for country in dfs:
        dfs[country].to_csv(f'scripts/country/output/{country}/data.csv')

# driver
# NOTE running will currently write over existing output data
days_ago = 10
today_dt = datetime.datetime.today()

cur_file_path = os.getcwd()
mation_output_dir = os.path.join(
    cur_file_path,
    f'mation-out/{today_dt.year}-{today_dt.month}-{today_dt.day}_{days_ago}-days_ago/output.csv'
    )
mation_output_path = os.path.abspath(mation_output_dir)

df = pd.read_csv(mation_output_path)
parse_df_create_dirs(df)
parse_df_into_country(df)
