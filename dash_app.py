import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
import sqlite3
import time

from storage import convert_data_to_df

app = dash.Dash()

def legs_plot(id=1, secs = [0,10]):
    
    pd = get_user_data_by_secs(id, secs)
    datetime = np.array(pd["datetimes"])
    values = np.array(pd["values"])
    anomalies = np.array(pd["anomalies"])
    sensor_list = ["L0", "L1", "L2", "R0", "R1", "R2"]

    color_list = ["brown", "blue", "green", "gray", "pink", "black"]

    fig = go.Figure()
    fig.update_xaxes(title="Measurements time")
    fig.update_yaxes(title="Pressure in % (100% = 1023)")
    for idx, sensor in enumerate(sensor_list):
        fig.add_trace(go.Scatter(x=datetime, y=values[:,idx], name=sensor, legendgrouptitle_text="Sensors", legendgroup="sensors", line=dict(color=color_list[idx])))
        fig.add_trace(go.Scatter(x=datetime, y=values[:,idx][anomalies[:,idx] == "True"], name=sensor, line=dict(color="#FF0000"), legendgrouptitle_text="Anomalies", legendgroup="anomalies"))

    return fig

def create_layout():
    app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'Tesla visualizer', style = {'textAlign': 'center',\
            'marginTop': 40, 'marginBottom': 40}), \
        html.Div(
        [
            dcc.Dropdown( 
                id='person-dropdown',
                options=[
                    {'label': 'Janek Grzegorczyk', 'value': 1},
                    {'label': 'Elbieta Kochalska', 'value': 2},
                    {'label': 'Albert Lisowski', 'value': 3},
                    {'label': 'Ewelina Nosowska', 'value': 4},
                    {'label': 'Piotr Fokalski', 'value': 5},
                    {'label': 'Bartosz Moskalski', 'value': 6}
                ],
                value=1
        ),
        ],style = {'width': '50%'}),\
        html.Div(
        [
            dcc.RangeSlider(
                id = 'seconds',
                count = 1,
                min = 0,
                max = 600,
                step = 1,
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": True},
                value = [0, 10]
        )],style = {'width': '80%'}),\
        
        html.Div(id='output-container-range-slider'),
        html.Center("Graphical visualization of measurements for monitoring walking habbits and patterns"), \
        dcc.Graph(id = 'the_plot', figure = legs_plot(1, [0,10]),style = {'width': '100%'}), \
        dcc.Interval(id = 'interval', interval = 1000, n_intervals = 0)
    ],style = {'width': '100%', 'display': 'flex','flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})

@app.callback(
    Output(component_id='the_plot', component_property='figure'),
    Input(component_id='interval', component_property='n_intervals'),
    Input('person-dropdown', 'value'),
    Input('seconds', 'value'))
def graph_update(n_intervals, person_value, secs):
    print(n_intervals)
    return legs_plot(person_value, secs)


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('seconds', 'value')])
def update_output(value):
    return 'Showing the plot between last {} seconds and last {} seconds'.format(value[0], value[1])


def get_user_data_by_secs(patient_id, secs):
    _conn = sqlite3.connect('patients.db')
    c = _conn.cursor()
    ts = time.time()
    c.execute("SELECT * FROM USERS WHERE patient_id=? AND end_time<? AND end_time>?", (patient_id,ts-secs[0], ts-secs[1]))
    users = c.fetchall()
    return convert_data_to_df(users)