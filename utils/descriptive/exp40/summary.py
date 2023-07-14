
import pandas as pd
from utils.descriptive.exp40 import preprocess40
from dash import dash_table


def create_summary_table(street):
    df_N = preprocess40.df_N
    df_N_street = df_N[df_N['description'] == street]

    # Define the order of weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    # Calculate the average noise values by weekday
    average_noise = df_N_street.groupby('weekday')['laf50_per_hour'].mean().reset_index()

    # Filter the dataset for the specific description and night hours
    filtered_data_night = df_N_street[((df_N_street['hour'] >= 22) | (df_N_street['hour'] < 6))]

    # Calculate the average noise values by weekday
    average_noise_night = filtered_data_night.groupby('weekday')['laf50_per_hour'].mean().reset_index()

    # Filter the dataset for the specific description and day hours
    filtered_data_day = df_N_street[((df_N_street['hour'] >= 6) & (df_N_street['hour'] < 22))]

    # Calculate the average noise values by weekday
    average_noise_day = filtered_data_day.groupby('weekday')['laf50_per_hour'].mean().reset_index()

    # Merge the average noise dataframes
    merged_data = average_noise.merge(average_noise_night, on='weekday', suffixes=('_day', '_night'))
    merged_data = merged_data.merge(average_noise_day, on='weekday')

    # Rename the columns
    merged_data.columns = ['Weekday', 'Average Noise (Day)', 'Average Noise (Night)', 'Average Noise (Daytime)']
    merged_data['Weekday'] = weekday_order

    # Set the Weekday column as a categorical variable with the specified order
    merged_data['Weekday'] = pd.Categorical(merged_data['Weekday'], categories=weekday_order, ordered=True)

    # Sort the dataframe by the weekday order
    merged_data.sort_values('Weekday', inplace=True)

    # Set the Weekday column as the index
    merged_data.set_index('Weekday', inplace=False)

    # Calculate the maximum values for each numeric column
    numeric_columns = merged_data.select_dtypes(include=[float, int]).columns
    max_values = merged_data[numeric_columns].max()

    # Create DashTable
    dashtable_summary = dash_table.DataTable(
        merged_data.to_dict('records'), [{"name": i, "id": i} for i in merged_data.columns],
        style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        },
        style_data_conditional=[
        {
            'if': {
                'filter_query': f"{{{column}}} = {max_value}",
                'column_id': column
            },
            'backgroundColor': '#FFDDC1',  # Specify the highlight color
            'color': 'black'  # Specify the text color
        }
        for column, max_value in max_values.items()
    ],
        tooltip_data=[{
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in merged_data.to_dict('records')
        ],
        tooltip_duration=None
    )
    return dashtable_summary