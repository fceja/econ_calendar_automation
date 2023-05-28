import csv
import math
import os
import re

import pandas as pd

# TODO - need to consider oil for CAD

CONVERSION = {
    None : 1,
    '': 1,
    '%': 1,
    'K': 10**3, # thousand
    'M': 10**6, # million
    'B': 10**9, # billion
    'T': 10**12 # trillion
}

def is_all_nan(actual, forcast, previous, df, index):
    try:
        if all(math.isnan(x) for x in [actual, forcast, previous]):
            df.at[index, 'Strength'] = 'Neutral'
            return True

    except TypeError:
        return False

def is_any_nan(list):
    if any(math.isnan(x) for x in list):
        return True

    return False

def is_all_str(actual, forcast, previous):
    try:
        if all(str(x) for x in [actual, forcast, previous]):
            return True

    except TypeError:
        return False

def convert_to_float(nums):
    nums_float = []
    for num in nums:
        match = re.match(r"([-+]?\d+(?:,\d{3})*(?:\.\d+)?)([A-Z%]+)?", num)
        num_str = match.group(1)
        num_ltr = match.group(2)

        num_str = num_str.replace(',', '')

        result = float(num_str) * float(CONVERSION[num_ltr])

        nums_float.append(round(result, 2))

    return nums_float

def calc_strength_num_actual_forecast_previous_pmi(actual, forecast, previous):
    # if actual > 50:
    if actual > 50 and actual > forecast and actual > previous and previous > forecast:
        return 1 # shockingly strong
    elif actual > previous and actual > forecast:
        return .80 # strong
    elif actual > previous and actual == forecast:
        return .60 # mild strong
    elif actual > previous and actual < forecast:
        return .40 # mixed strong

    # elif actual == 50:
    elif actual > 50 and actual < previous and actual > forecast:
        return .20 # mixed weak

    elif actual == 50 and actual == previous and actual > forecast:
        return .20 # low strong
    elif actual == previous and actual == forecast:
        return 0 # neutral
    elif actual == previous and actual < forecast:
        return -.20 # low weak

    # elif actual < 50:
    elif actual < 50 and actual < previous and actual > forecast:
        return -.40 # mixed weak
    elif actual < previous and actual == forecast:
        return -.60 # mixed weak
    elif actual < previous and actual < forecast:
        return -.80 # weak
    elif previous < forecast and actual < previous:
        return -1 # shockingly weak

    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}, forecast: {forecast}')

def calc_strength_num_actual_previous_pmi(actual, previous):
    if actual > 50 and actual > previous:
        return 1 # shockingly strong
    elif actual > 50 and actual == previous:
        return .75 # strong
    elif actual > 50 and actual < previous:
        return .50 # mild strong

    elif actual == 50 and actual > previous:
        return .25 # low strong
    elif actual == 50 and actual == previous:
        return 0 # neutral
    elif actual == 50 and actual < previous:
        return -.25 # low weak

    elif actual < 50 and actual > previous:
        return -.50 # mixed weak
    elif actual < 50 and  actual == previous:
        return -.75 # mixed weak
    elif actual < 50 and actual < previous:
        return -1 # weak
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}')

def calc_strength_num_actual_previous_unemployment(actual, previous):
    if actual > previous:
        return 1
    elif actual == previous:
        return 0
    elif actual < previous:
        return -1
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}')

def calc_strength_num_actual_forecast_previous_unemployment(actual, forecast, previous):
    print(f'actual: {actual}, forecast:{forecast}, prev: {previous}')
    # orig
    # if actual > forecast and previous > forecast:
    if actual > forecast and actual > previous and previous > forecast:
        print(f' in here actual: {actual}, forecast:{forecast}, prev: {previous}')
        return -1 # shockingly strong
    elif actual > previous and actual > forecast:
        return -.80 # strong
    elif actual > previous and actual == forecast:
        return -.60 # mild strong
    elif actual > previous and actual < forecast:
        return -.40 # mixed strong

    elif actual == previous and actual > forecast:
        return -.20 # low strong
    elif actual == previous and actual == forecast:
        return 1 # neutral
    elif actual == previous and actual < forecast:
        return .20 # low weak

    elif actual < previous and actual > forecast:
        return .40 # mixed weak
    elif actual < previous and actual == forecast:
        print(f'we want actual: {actual}, forecast:{forecast}, prev: {previous}')
        return .60 # mixed weak
    elif actual < previous and actual < forecast:
        return .80 # weak
    elif previous < forecast and actual < previous:
        return 1 # shockingly weak
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}, forecast: {forecast}')

def calc_strength_num_actual_forecast_previous_oil(actual, forecast, previous):
    # orig
    # if actual > forecast and previous > forecast:
    if actual > forecast and actual > previous and previous > forecast:
        return -1 # shockingly strong
    elif actual > previous and actual > forecast:
        return -.80 # strong
    elif actual > previous and actual == forecast:
        return -.60 # mild strong
    elif actual > previous and actual < forecast:
        return -.40 # mixed strong

    elif actual == previous and actual > forecast:
        return -.20 # low strong
    elif actual == previous and actual == forecast:
        return 0 # neutral
    elif actual == previous and actual < forecast:
        return .20 # low weak

    elif actual < previous and actual > forecast:
        return .40 # mixed weak
    elif actual < previous and actual == forecast:
        return .60 # mixed weak
    elif actual < previous and actual < forecast:
        return .80 # weak
    elif previous < forecast and actual < previous:
        return 1 # shockingly weak
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}, forecast: {forecast}')

def calc_strength_num_actual_forecast_previous(actual, forecast, previous):
    # TODO update logic, not doing percentage math as expected
    # orig
    # if actual > forecast and previous > forecast:
    if actual > forecast and actual > previous and previous > forecast:
        return 1 # shockingly strong
    elif actual > previous and actual > forecast:
        return .80 # strong
    elif actual > previous and actual == forecast:
        return .60 # mild strong
    elif actual > previous and actual < forecast:
        return .40 # mixed strong

    elif actual == previous and actual > forecast:
        return .20 # low strong
    elif actual == previous and actual == forecast:
        return 0 # neutral
    elif actual == previous and actual < forecast:
        return -.20 # low weak

    elif actual < previous and actual > forecast:
        return -.40 # mixed weak
    elif actual < previous and actual == forecast:
        return -.60 # mixed weak
    elif actual < previous and actual < forecast:
        return -.80 # weak
    elif previous < forecast and actual < previous:
        return -1 # shockingly weak
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}, forecast: {forecast}')

def calc_strength_num_actual_previous(actual, previous):
    # TODO may need to adjust
    if actual > previous:
        return 1
    elif actual == previous:
        return 0
    elif actual < previous:
        return -1
    else:
        raise Exception(f'Logic error -> actual: {actual}, previous: {previous}')

def calc_percent_diff(new, old):
    if old == 0:
        return round((new - old) / 1.0 * 100, 2)

    else:
        return round(((new - old) / abs(old)) * 100,2)

def calc_all_actual_forecast_previous(actual, forecast, previous, df, index):
    # TODO add percent diff
    # TODO consider > 50 <

    event = df.iloc[index]['Event_Title']

    actual, forecast, previous = convert_to_float([actual, forecast, previous])

    # df.at[index, 'Strength'] = calc_strength_num_actual_forecast_previous(actual, forecast, previous)
    if 'employment' in event.lower():
        df.at[index, 'Strength'] = calc_strength_num_actual_forecast_previous_unemployment(actual, forecast, previous)

    if 'oil' in event.lower():
        df.at[index, 'Strength'] = calc_strength_num_actual_forecast_previous_oil(actual, forecast, previous)

    elif 'pmi' in event.lower():
        df.at[index, 'Strength'] = calc_strength_num_actual_forecast_previous_pmi(actual, forecast, previous)

    else:
        df.at[index, 'Strength'] = calc_strength_num_actual_forecast_previous(actual, forecast, previous)

    df.at[index, 'Actual/Previous Diff'] = f'{calc_percent_diff(actual, previous)}%'
    df.at[index, 'Actual/Forecast Diff'] = f'{calc_percent_diff(actual, forecast)}%'

def calc_actual_previous(actual, previous, df, index):
    event = df.iloc[index]['Event_Title']

    actual, previous = convert_to_float([actual, previous])

    if 'pmi' in event.lower():
        df.at[index, 'Strength'] = calc_strength_num_actual_previous_pmi(actual, previous)

    elif 'employment' in event.lower():
        df.at[index, 'Strength'] = calc_strength_num_actual_previous_unemployment(actual, previous)
    else:
        df.at[index, 'Strength'] = calc_strength_num_actual_previous(actual, previous)


    df.at[index, 'Actual/Previous Diff'] = f'{calc_percent_diff(actual, previous)}%'

def is_val_nan(val):
    if type(val) is float and math.isnan(val):
        return True

    return False

def calc_strength(df):
    df['Strength'] = 'Unk'
    df['Actual/Previous Diff'] = 'Unk'
    df['Actual/Forecast Diff'] = 'Unk'



    for index, row in df.iterrows():
        # NOTE - we are entere proper nan values
        if is_all_nan(row['Actual'], row['Forecast'], row['Previous'], df, index):
            continue

        elif is_all_str(row['Actual'], row['Forecast'], row['Previous']) and not is_val_nan(row['Actual']) and not is_val_nan(row['Forecast']) and not is_val_nan(row['Previous']):
            calc_all_actual_forecast_previous(row['Actual'], row['Forecast'], row['Previous'], df, index)
            continue

        elif is_all_str(row['Actual'], row['Forecast'], row['Previous']) and is_val_nan(row['Actual']):
            # data not released yet
            continue

        elif is_all_str(row['Actual'], row['Forecast'], row['Previous']) and is_val_nan(row['Forecast']):
            calc_actual_previous(row['Actual'], row['Previous'], df, index)
            continue

        elif is_all_str(row['Actual'], row['Forecast'], row['Previous']) and is_val_nan(row['Previous']):
            # NOTE - leaving assertin for now, may not need? Data should not have nan Previous
            assert 1 == 2

        else:
            raise Exception(f'Logic error -> actual: {row["Actual"]}, previous: {row["Previous"]}, forecast: {row["Forecast"]}')

    dir_path = f'scripts/calculate_strength/output/{country}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    df.to_csv(f'{dir_path}/data.csv')


# driver
countries = ['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD']
for country in countries:
    cur_file_path = os.getcwd()
    mation_output_dir = os.path.join(cur_file_path, f'scripts/country/output/{country}/data.csv')
    mation_output_path = os.path.abspath(mation_output_dir)

    df = pd.read_csv(mation_output_path, index_col=0)

    calc_strength(df)
