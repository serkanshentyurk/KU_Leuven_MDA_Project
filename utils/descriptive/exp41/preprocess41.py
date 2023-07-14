import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from utils import paths

def gather_exp41(folder_path):
    exp41_data_path = [folder_path + '/csv_results_41_255439_mp-01-naamsestraat-35-maxim.csv',
                       folder_path + '/csv_results_41_255440_mp-02-naamsestraat-57-xior.csv',
                       folder_path + '/csv_results_41_255441_mp-03-naamsestraat-62-taste.csv',
                       folder_path + '/csv_results_41_255442_mp-05-calvariekapel-ku-leuven.csv',
                       folder_path + '/csv_results_41_255443_mp-06-parkstraat-2-la-filosovia.csv',
                       folder_path + '/csv_results_41_255444_mp-07-naamsestraat-81.csv',
                       folder_path + '/csv_results_41_255445_mp-08-kiosk-stadspark.csv',
                       folder_path + '/csv_results_41_280324_mp08bis---vrijthof.csv',
                       folder_path + '/csv_results_41_303910_mp-04-his-hears.csv']
    exp41_data = []
    
    for i in exp41_data_path:
        exp41_data.append(pd.read_csv(i, sep = ';'))
    return exp41_data


def divide_timestamp(df):
    df_final = df.copy()
    df_final['result_timestamp'] = df.result_timestamp.str[:19]
    df_final['year'] = df.result_timestamp.str[6:10].astype('int32')
    df_final['month'] = df.result_timestamp.str[3:5].astype('int32')
    df_final['day'] = df.result_timestamp.str[0:2].astype('int32')
    df_final['hour'] = df.result_timestamp.str[11:13].astype('int32')
    df_final['minute'] = df.result_timestamp.str[14:16].astype('int32')
    df_final['second'] = df.result_timestamp.str[17:19].astype('int32')
    return df_final


def drop_modify_exp41(df, first=True):
    final = []
    description_mapping = {
        'MP 01: Naamsestraat 35  Maxim': 'Naamsestraat 35',
        'MP 02: Naamsestraat 57 Xior': 'Naamsestraat 57',
        'MP 03: Naamsestraat 62 Taste': 'Naamsestraat 62',
        'MP 05: Calvariekapel KU Leuven': 'Calvariekapel KU Leuven',
        'MP 06: Parkstraat 2 La Filosovia': 'Parkstraat 2',
        'MP 07: Naamsestraat 81': 'Naamsestraat 81',
        'MP08bis - Vrijthof': 'Vrijthof'
    }
    
    for data in df:
        data_nan = data.dropna(subset=['noise_event_laeq_primary_detected_certainty'])
        data_nan_drop = data_nan.drop(['noise_event_laeq_model_id_unit', 'noise_event_laeq_primary_detected_certainty_unit', 'noise_event_laeq_primary_detected_class_unit'], axis=1)
        data_nan_drop_uncertain75 = data_nan_drop[data_nan_drop['noise_event_laeq_primary_detected_certainty'] > 75]
        data_final = divide_timestamp(data_nan_drop_uncertain75)
        data_final['description'] = data_final['description'].replace(description_mapping)
        
        if first:
            le = LabelEncoder()
            data_final['noise_event_class'] = le.fit_transform(data_final['noise_event_laeq_primary_detected_class'])
            first = False
        else:
            data_final['noise_event_class'] = le.transform(data_final['noise_event_laeq_primary_detected_class'])
        
        final.append(data_final)
    
    return final

def initial_preprocessing_exp41(folder_path, first = True):
    exp41_data = gather_exp41(folder_path)
    exp41_final = drop_modify_exp41(exp41_data)
    return exp41_final


[df1_E, df2_E, df3_E, df4_E, df5_E, df6_E, df7_E, df8_E, df9_E] = initial_preprocessing_exp41(paths.path_exp41)
df_E = pd.concat([df1_E,df2_E,df3_E,df4_E,df5_E,df6_E,df7_E,df8_E,df9_E], ignore_index=True)