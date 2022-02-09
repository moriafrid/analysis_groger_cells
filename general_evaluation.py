import configuration_factory
from neuron_network import neuronal_model
import pickle
from typing import Iterable
import sklearn.metrics as skm
import dash
import numpy as np
import plotly.graph_objects as go
import torch
from dash import dcc,callback_context
from dash import html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from tqdm import tqdm
from simulation_data_generator import SimulationDataGenerator
import neuron_network.node_network.recursive_neuronal_model as recursive_neuronal_model
from general_aid_function import *
from neuron_network import neuronal_model
import plotly.express as px
BUFFER_SIZE_IN_FILES_VALID = 1
import datetime

class ModelEvaluator():
    def __init__(self, data_to_evaluate):
        self.data = data_to_evaluate

    def __getitem__(self, index):
        return self.data[index]

    def display(self):
        app = dash.Dash()
        auc, fig = self.create_ROC_curve()
        app.layout = html.Div([
            dcc.Slider(
                id='my-slider',
                min=0,
                max=len(self.data) - 1,
                step=1,
                value=len(self.data) // 2,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Div(id='slider-output-container', style={'height': '2vh'}),
            html.Div([
            html.Button('-50', id='btn-m50', n_clicks=0, style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('-10', id='btn-m10', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('-5', id='btn-m5', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('-1', id='btn-m1', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('+1', id='btn-p1', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('+5', id='btn-p5', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('+10', id='btn-p10', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            html.Button('+50', id='btn-p50', n_clicks=0,style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',"margin-left": "10px"}),
            ], style={'width':'100vw','margin': '1', 'border-style': 'solid', 'align': 'center', 'vertical-align': 'middle'}),
            html.Div([
                dcc.Graph(id='evaluation-graph', figure=go.Figure(),
                          style={'height': '95vh', 'margin': '0', 'border-style': 'solid', 'align': 'center'})],
                style={'height': '95vh', 'margin': '0', 'border-style': 'solid', 'align': 'center'}),
        ])

        @app.callback(
            Output('my-slider', 'value'),
            Output('slider-output-container', 'value'),
            Output('evaluation-graph', 'figure'),
            [Input('my-slider', 'value'),
             Input('btn-m50','n_clicks'),
             Input('btn-m10','n_clicks'),
             Input('btn-m5','n_clicks'),
             Input('btn-m1','n_clicks'),
             Input('btn-p1','n_clicks'),
             Input('btn-p5','n_clicks'),
             Input('btn-p10','n_clicks'),
             Input('btn-p50','n_clicks')
             ])
        def update_output(value,btnm50,btnm10,btnm5,btnm1,btnp1,btnp5,btnp10,btnp50):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0][:-len(".n_clicks")]
            value=int(value)

            if 'btn-m' in changed_id:
                value-=int(changed_id[len('btn-m'):])
            elif 'btn-p' in changed_id:
                value +=int(changed_id[len('btn-m'):])
            value= max(0,value)
            value=min(value,len(self.data))
            fig = self.display_window(value)
            return value,'You have selected "{}"'.format(value), fig

        app.run_server(debug=True, use_reloader=False)


    def display_window(self, index): #TODO: you need to re write this function
        tr = self[index]
        fig = make_subplots(rows=1, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.1, start_cell='top-left',
                            subplot_titles=("voltage", "spike probability"), row_heights=[0.7, 0.3])
        x_axis = np.arange(v.shape[0])

        # fig.add_trace(go.Scatter(x=x_axis, y=np.convolve(v,np.full((self.config.input_window_size//2,),1./(self.config.input_window_size//2))), name="avg_voltage"), row=1, col=1)
        fig.add_trace(go.Scatter(x=x_axis, y=tr, name="voltage"), row=1, col=1)
        fig.update_layout(  # height=600, width=600,
            title_text="index %d" % (index))
        return fig


if __name__ == '__main__':
    # ModelEvaluator.build_and_save(r"C:\Users\ninit\Documents\university\Idan_Lab\dendritic tree project\models\NMDA\heavy_AdamW_NMDA_Tree_TCN__2022-01-27__17_58__ID_40048\heavy_AdamW_NMDA_Tree_TCN__2022-01-27__17_58__ID_40048")
    eval = ModelEvaluator(data)
    # eval.data.flatten_batch_dimensions()
    # eval.save()
    eval.display()
#