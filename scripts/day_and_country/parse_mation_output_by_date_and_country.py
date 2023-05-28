import csv
import os
import datetime

import pandas as pd

def reset_countries_found():
    return {
        'AUD': False,
        'CAD': False,
        'CHF': False,
        'CNY': False,
        'EUR': False,
        'GBP': False,
        'JPY': False,
        'NZD': False,
        'USD': False,
    }

def parse_df_create_dirs(df):
    for _, row in df.iterrows():
        # check if dir exists -> output/{date}/{country}; else create
        date_str = row['Date'].replace('/', '-')
        dir_path = f'output/{date_str}'

        # check if day dir exists, else create
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # check if country dir exists, else create
        if not os.path.exists(f'{dir_path}/{row["Country"]}'):
            os.makedirs(f'{dir_path}/{row["Country"]}')

def parse_df_into_country(df):
    country_found = reset_countries_found()

    cur_date = df.iloc[0]['Date']

    for _, row in df.iterrows():
        date_str = row['Date'].replace('/', '-')
        dir_path = f'output/{date_str}'

        csv_file = open(f'{dir_path}/{row["Country"]}/data.csv', 'a', newline='')
        csv_writer = csv.writer(csv_file)

        if row['Date'] != cur_date:
            cur_date = row['Date']
            country_found = reset_countries_found()

        if not country_found[row['Country']]:
            csv_writer.writerow(['Date', 'Time', 'Country', 'Sentiment', 'Event_Title', 'Actual', 'Forecast', 'Previous'])
            country_found[row['Country']] = True

        date = row['Date']
        time = row['Time']
        country = row['Country']
        sentiment = row['Sentiment']
        event_title = row['Event_Title']
        actual = row['Actual']
        forecast = row['Forecast']
        prev = row['Previous']
        csv_writer.writerow([date, time, country, sentiment, event_title, actual, forecast, prev])

        csv_file.close()

# driver
days_ago = 10
today_dt = datetime.datime.today()

cur_file_path = os.getcwd()
mation_output_dir = os.path.join(
    cur_file_path,
    f'../../mation-out/{today_dt.year}-{today_dt.month}-{today_dt.day}_{days_ago}-days_ago/output.csv'
    )
print(f'\n\nmation output dir: {mation_output_dir}')
mation_output_path = os.path.abspath(mation_output_dir)


df = pd.read_csv(mation_output_path)
parse_df_create_dirs(df)
parse_df_into_country(df)
