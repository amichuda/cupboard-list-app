import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

from spice_list import spice_list
from updated_list import updated_list
import pickle

if updated_list:
    the_list = updated_list
else:
    the_list = spice_list

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1(children='The Cupboard List'),
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


if __name__=='__main__':

    app.run_server(port=8050, debug=True)