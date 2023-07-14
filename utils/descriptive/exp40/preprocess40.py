import pandas as pd
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
from utils import paths

def gather_exp40(folder_path):
    exp40_data_path = [folder_path + '/csv_results_40_255439_mp-01-naamsestraat-35-maxim.csv',
                       folder_path + '/csv_results_40_255440_mp-02-naamsestraat-57-xior.csv',
                       folder_path + '/csv_results_40_255441_mp-03-naamsestraat-62-taste.csv',
                       folder_path + '/csv_results_40_255442_mp-05-calvariekapel-ku-leuven.csv',
                       folder_path + '/csv_results_40_255443_mp-06-parkstraat-2-la-filosovia.csv',
                       folder_path + '/csv_results_40_255444_mp-07-naamsestraat-81.csv',
                       folder_path + '/csv_results_40_255445_mp-08-kiosk-stadspark.csv',
                       folder_path + '/csv_results_40_280324_mp08bis---vrijthof.csv',
                       folder_path + '/csv_results_40_303910_mp-04-his-hears.csv']
    exp40_data = []
    
    for i in exp40_data_path:
        exp40_data.append(pd.read_csv(i, sep = ';'))
    return exp40_data

def divide_timestamp(df):
    df_final = df.copy()
    df_final['result_timestamp'] = df_final['result_timestamp'].str[:19]
    df_final['month'] = df_final['result_timestamp'].str[3:5].astype('int32')
    df_final['day'] = df_final['result_timestamp'].str[0:2].astype('int32')
    df_final['hour'] = df_final['result_timestamp'].str[11:13].astype('int32')
    df_final['day_month'] = df_final['day'].astype(str) + '/' + df_final['month'].astype(str)
    dates = pd.to_datetime(df_final['result_timestamp'], dayfirst= True)
    df_final['weekday'] = dates.dt.weekday
    return df_final

def drop_modify_exp40(df, first=True):
    final = []
    description_mapping = {
        'MP 01: Naamsestraat 35  Maxim': 'Naamsestraat 35',
        'MP 02: Naamsestraat 57 Xior': 'Naamsestraat 57',
        'MP 03: Naamsestraat 62 Taste': 'Naamsestraat 62',
        'MP 04: His & Hears': 'Naamsestraat 76',
        'MP 05: Calvariekapel KU Leuven': 'Calvariekapel KU Leuven',
        'MP 06: Parkstraat 2 La Filosovia': 'Parkstraat 2',
        'MP 07: Naamsestraat 81': 'Naamsestraat 81',
        'MP08bis - Vrijthof': 'Vrijthof'
       
    }
    
    for data in df:
        datadrop = data.drop(["laf005_per_hour_unit", "laf01_per_hour_unit", "laf05_per_hour_unit", "laf10_per_hour_unit",
                   "laf25_per_hour_unit", "laf50_per_hour_unit", "laf75_per_hour_unit", "laf90_per_hour_unit",
                   "laf95_per_hour_unit", "laf98_per_hour_unit", "laf99_per_hour_unit", "laf995_per_hour_unit"],
                  axis=1).copy()
        data_final = divide_timestamp(datadrop)
        data_final['description'] = data_final['description'].replace(description_mapping)
        final.append(data_final)
    return final



def initial_preprocessing_exp40(folder_path, first = True):
    exp40_data = gather_exp40(folder_path)
    exp40_final = drop_modify_exp40(exp40_data)
    return exp40_final


[df1_N, df2_N, df3_N, df4_N, df5_N, df6_N, df7_N, df8_N, df9_N] = initial_preprocessing_exp40(paths.path_exp40)
df_N = pd.concat([df1_N, df2_N, df3_N, df4_N, df5_N, df6_N, df7_N, df8_N, df9_N], ignore_index=True)