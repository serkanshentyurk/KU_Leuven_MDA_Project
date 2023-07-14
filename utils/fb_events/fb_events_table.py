import pandas as pd
from dash import dash_table
from utils import paths

table_methods = pd.read_csv(paths.path_fb_table, sep='\t')
table_methods = pd.read_csv('/Users/Serkan/Desktop/KUL/2023 Spring/Modern Data Analytics/Project/MDABurundi/App/data/model_comparison.csv', sep='\t')

dashtable_methods = dash_table.DataTable(
        table_methods.to_dict('records'), [{"name": i, "id": i} for i in table_methods.columns],
        style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        },
        tooltip_data=[{
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in table_methods.to_dict('records')
        ],
        tooltip_duration=None
    )

