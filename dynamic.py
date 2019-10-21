import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
df = pd.read_excel("main.xlsx",sheet_name="main")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        [
            html.Div(
        [
            html.Div(
        [
            html.H5("Calorific Value", style={'text-align': 'right'}),
            dcc.Input(
                id="calorific-value",
                placeholder="Enter Calorific Value",
                value=42700,
                type="number",
                debounce=True,
                required=True
                
            )
        ],
        className="Calorific Value",
        style={},
    ),
        ],
        id='calorific-filter-container',
        style={'display': 'flex', 'justify-content': 'flex-end', 'margin-bottom': '2rem'},
    ),
    html.Div(
        [
        html.H5("Wind Scale Dropdown", style={'text-align': 'right'}),
        dcc.Dropdown(
            id='wind-dropdown',
            options = [
                {'label':'1','value':1},
                {'label':'2','value':2},
                {'label':'3','value':3},
                {'label':'4','value':4},
                {'label':'5','value':5},
                {'label':'6','value':6},
                {'label':'7','value':7},
                {'label':'8','value':8},
            ],
            value=['1','2','3','4','5','6','7','8'],
            multi=True,
        ),
        ],
        id='wind-dropdown-container',
        style={'display': 'flex', 'flex-direction': 'column', 'margin-bottom': '2rem'},
    ),
    html.Div(
        [
        html.H5("Sea Scale Slider", style={'text-align': 'right'}),
        dcc.Dropdown(
            id='sea-dropdown',
            options = [
                {'label':'0', 'value':0},
                {'label':'1', 'value':1},
                {'label':'2', 'value':2},
                {'label':'3', 'value':3},
                {'label':'4', 'value':4},
                {'label':'5', 'value':5},
                {'label':'6', 'value':6},
                {'label':'7', 'value':7},
                {'label':'8', 'value':8},
                {'label':'9', 'value':9},
            ],
            value=['1','2','3','4','5','6','7','8','9'],
            multi=True,
        ),
        ],
        id='sea-scale-dropdown-container',
        style={'display': 'flex', 'flex-direction': 'column', 'margin-bottom': '2rem'},
    ),
        html.Div(
        [
        html.H5("Min Speed Value", style={'text-align': 'left'}),
        dcc.Input(
            id="min-speed-value",
            type="number",
            placeholder="0",
            debounce=True,
            required=True,
            value=0
        ),
        html.H5("Max Speed Value", style={'text-align': 'left'}),
        dcc.Input(
            id="max-speed-value",
            type="number",
            placeholder="22",
            debounce=True,
            required=True,
            value=100
        )
        ],
        className = "Average Scale Slider",
        style={"margin-left": "auto", "margin-right": "auto"}
        ),
        ],
        style={'order': '1', 'flex-basis': '28%'}
    ),
        dcc.Graph(id="my-graph"),
], className="", style={'display': 'flex', 'justify-content': 'space-between', 'padding-right': '1.5rem'})

@app.callback(
    dash.dependencies.Output('my-graph','figure'),
    [dash.dependencies.Input('wind-dropdown','value'),
    dash.dependencies.Input('sea-dropdown','value'),
    dash.dependencies.Input('min-speed-value','value'),
    dash.dependencies.Input('max-speed-value','value'),
    dash.dependencies.Input('calorific-value','value')])
def update_graph(wind_value, sea_value, min_speed_value,max_speed_value,calorific_value):
    # print(min_speed_value)
    # print(max_speed_value)
    windScale = df[df['Wind Scale'].isin(wind_value)]
    seaScale = windScale[windScale['Sea'].isin(sea_value)]
    speedScale = seaScale[seaScale['Speedvalue'].isin(np.around(np.arange(min_speed_value, max_speed_value, 0.1), decimals=1))]
    # dff = df[df['Wind Scale']>=wind_value[0]]
    # dff = df[df['Sea']>=sea_value[0]]

    # Add new "GREEN" column
    speedScale['Caloriphic Consumption'] = speedScale['Reference Consumption'] * int(calorific_value) / 10000
    speedScale['Caloriphic Consumption'] = (42700/ calorific_value) * speedScale['Reference Consumption']

    trace1 = go.Bar(x=speedScale['Date'], y=speedScale['Actual Consumption'], name="Actual Consumption", text=df['Actual Consumption'] - df['Reference Consumption'])
    trace2 = go.Bar(x=speedScale['Date'], y=speedScale['Reference Consumption'], name="Reference Consumption")
    trace3 = go.Bar(x=speedScale['Date'], y=speedScale['Caloriphic Consumption'], name="Caloriphic Consumption")
    # print("Calorific Value is {}".format(calorific_value))
    return {
        'data': [trace1, trace2, trace3],
        'layout': go.Layout(title="<span style='font-size: 20px'>Actual Engine Consumption vs Charter Party Reference Consumption</span>",
        width=1250,
        height=650,
                        hovermode="closest",
                        xaxis={'title': "Date", 'titlefont': {'color': 'black', 'size': 14},'zeroline':False,'ticks':"inside",'nticks':20,
                                   'tickfont': {'size': 9, 'color': 'black'}},
                        yaxis={'title': "Consumption", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}}
                        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)