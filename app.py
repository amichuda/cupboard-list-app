import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from spice_list import spice_list
import pickle
import os

if os.path.exists('the_list.pickle'):
    with open('this_list.pickle', 'wb') as f:
        pickle.load(f)
else:
    the_list = spice_list

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1(children='The Cupboard List'),
    dbc.Alert(id="alert-fade",
        dismissable=True,
        is_open=False,
        duration=4000
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label' : 'Spices', 'value' : 'spices'},
            {'label' : 'Oils/Vinegars/Syrups/Liq.', 'value' : 'oils_vinegar_syrups_liquids'},
            {'label' : 'Other', 'value' : 'other'}
        ],
        value='spices'
    ),
    dash_table.DataTable(
        id= 'table',
        columns=[{'name' : '', 'id' : 'list-name'}],
        data = [],
        row_deletable=True
    )
    ])

@app.callback(
    Output('table', 'data'),
    Input('dropdown', 'value')
)
def update_table(value):
    
    return [{'list-name' : i} for i in spice_list[value]]


@app.callback(
    Output('alert-fade', 'children'),
    Output('alert-fade', 'is_open'),
    Input('table', 'data_previous'),
    State('table', 'data')
)
def update_row_delete(previous, current):
    print("Previous:", previous)
    print("Current:", current)
    
    # Save data to pickle
    with open('the_list.pickle', 'wb') as f:
        pickle.dump(current, f)
    
    if previous is None:
        dash.exceptions.PreventUpdate()
    else:
        return (', '.join([f'Removed {row["list-name"]}' for row in previous if row not in current]), True)


if __name__=='__main__':

    app.run_server(port=8050, debug=True)