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
            html.H5("Calorific Value"),
            dcc.Input(
                id="calorific-value",
                placeholder="Enter Calorific Value",
                value='43700'
            )
        ],
        className="Calorific Value",
        style={},
    ),
    html.Div(
        [
        html.H2("Wind Scale Dropdown"),
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
        className = "Wind Scale Dropdown",
        style={"width": "50%", 'left': '10px'}
        ),
        html.Div(
        [
        html.H2("Sea Scale Slider"),
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
        className = "Sea Scale Dropdown",
        style={"width": "60%","margin-left": "auto", "margin-right": "auto"} #"margin-left": "auto", "margin-right": "auto"
        ),
        html.Div(
        [
        html.H2("Average Speed Slider"),
        dcc.RangeSlider(
            id='speed-slider',
            min=min(df['Average Speed']),
            max=max(df['Average Speed']),
            step=1,
            # dots=True,
            marks = {
                min(df['Average Speed']): str(min(df['Average Speed'])),
                max(df['Average Speed']): str(max(df['Average Speed']))
                # 0: '0',
                # 1:'1'
            },
            # value=np.arange(0, 22, 0.1),
        ),
        ],
        className = "Average Scale Slider",
        style={'width':'30%',"margin-left": "auto", "margin-right": "auto"}
        ),
        dcc.Graph(id="my-graph"),
], className="container")

@app.callback(
    dash.dependencies.Output('my-graph','figure'),
    [dash.dependencies.Input('wind-dropdown','value'),
    dash.dependencies.Input('sea-dropdown','value'),
    dash.dependencies.Input('speed-slider','value'),
    dash.dependencies.Input('calorific-value','value')])
def update_graph(wind_value, sea_value, speed_value,calorific_value):

    windScale = df[df['Wind Scale'].isin(wind_value)]
    seaScale = windScale[windScale['Sea'].isin(sea_value)]
    # speedScale = seaScale[seaScale['Average Speed'].isin(np.arange(min(df['Average Speed']), max(df['Average Speed']), 0.1))]
    # dff = df[df['Wind Scale']>=wind_value[0]]
    # dff = df[df['Sea']>=sea_value[0]]
    trace1 = go.Bar(x=seaScale['Date'], y=seaScale['Actual Consumption'], name="Actual Consumption")
    trace2 = go.Bar(x=seaScale['Date'], y=seaScale['Reference Consumption'], name="Reference Consumption")
    print("Calorific Value is {}".format(calorific_value))
    return {
        'data': [trace1, trace2],
        'layout': go.Layout(title='Actual Engine Consumption vs Charter Party Reference Consumption',
        width=1250,
        height=650,
                        hovermode="closest",
                        xaxis={'title': "Date", 'titlefont': {'color': 'black', 'size': 14},
                                   'tickfont': {'size': 9, 'color': 'black'}},
                        yaxis={'title': "Consumption", 'titlefont': {'color': 'black', 'size': 14, },
                                   'tickfont': {'color': 'black'}}
                        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)