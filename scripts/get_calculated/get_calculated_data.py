import os
import pandas as pd



total_df= pd.DataFrame()

countries = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD']
for country in countries:
    cur_file_path = os.getcwd()
    # mation_output_dir = os.path.join(cur_file_path, f'../calculate_strength/output/{country}/data.csv')
    mation_output_dir = os.path.join(cur_file_path, f'scripts/calculate_strength/output/{country}/data.csv')
    mation_output_path = os.path.abspath(mation_output_dir)


    df = pd.read_csv(mation_output_path, index_col=0)
    total_df = pd.concat([total_df, df])

    # dir_path = f'output/{country}'
    dir_path = f'scripts/get_calculated/output/{country}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    df.to_csv(f'{dir_path}/data.csv')


dir_path = f'scripts/get_calculated/output/z_total'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

total_df.to_csv(f'{dir_path}/data.csv')
