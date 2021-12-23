import dash
from dash import dcc
from dash import html
from dash.dcc.Interval import Interval
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
from storage import get_storage

app = dash.Dash()

def legs_plot():
    if 2 in get_storage():
        pd = get_storage()[2]
        datetime = np.array(pd["datetimes"])
        values = np.array(pd["values"])
        anomalies = np.array(pd["anomalies"])
    else:
        datetime = np.array([0])
        values = np.array([[0,0,0,0,0,0]])
        anomalies = np.array([[0,0,0,0,0,0]])

    sensor_list = ["L0", "L1", "L2", "R0", "R1", "R2"]

    fig = go.Figure()
    for idx, sensor in enumerate(sensor_list):
        fig.add_trace(go.Scatter(x=datetime, y=values[:,idx], name=sensor, legendgrouptitle_text="Sensors", legendgroup="sensors"))
        fig.add_trace(go.Scatter(x=datetime, y=values[:,idx][anomalies[:,idx] == True], name=sensor, line=dict(color="#FF0000"), legendgrouptitle_text="Anomalies", legendgroup="anomalies"))

    return fig

def create_layout():
    app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Tesla visualizer', style = {'textAlign': 'center',\
            'marginTop': 40, 'marginBottom': 40}), \
                dcc.Graph(id = 'the_plot', figure = legs_plot()), \
                dcc.Interval(id = 'interval', interval = 1000, n_intervals = 0)
    ])

@app.callback(Output(component_id='the_plot', component_property='figure'),
[Input(component_id='interval', component_property='n_intervals')])
def graph_update(n_intervals):
    print(n_intervals)
    return legs_plot()