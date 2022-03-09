import os
from glob import glob
import dash
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from dash import dcc, callback_context
from dash import html
from dash.dependencies import Input, Output
import dash_daq as daq
import shutil

class moriaFSystems():
    def __init__(self):
        self.files=[]
        self.files_to_save=[]
    def load_all_files_to_list(self,master_folder,suffix):
        result = [y for x in os.walk(master_folder) for y in glob(os.path.join(x[0], '*%s'%suffix))]
        self.files=result
        self.current_value=None
        self.files_to_save=[False]*len(self.files)
    def display(self,port=7080):
        app = dash.Dash()
        main_div = html.Div(id='main_div',children=[
            html.Div(id='slider_bar',children=
            dcc.Slider(
                id='my-slider',
                min=0,
                max=len(self.files) - 1,
                step=1,
                value=len(self.files) // 2,
                tooltip={"placement": "bottom", "always_visible": True}
            ),style={'height': '5vh'}),
            html.Div(id='slider-output-container', style={'height': '2vh'}),
            html.Div([
                html.Button('-50', id='btn-m50', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('-10', id='btn-m10', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('-5', id='btn-m5', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('-1', id='btn-m1', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('+1', id='btn-p1', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('+5', id='btn-p5', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('+10', id='btn-p10', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Button('+50', id='btn-p50', n_clicks=0,
                            style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}),
                html.Div(id='bool_switch',children=
               daq.BooleanSwitch(id="is_save_switch",label="save", on=False, color="red",
                                 style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"}))
            ], style={'width': '100vw', 'margin': '1', 'border-style': 'solid', 'align': 'center',
                      'vertical-align': 'middle','display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='show_image_section', figure=go.Figure(),
                          style={'height': '90vh', 'margin': '0', 'border-style': 'solid', 'align': 'center'})],
                style={'height': '95vh', 'margin': '0', 'border-style': 'solid', 'align': 'center'})])

        app.layout=html.Div(['base path:', dcc.Input(
            id="base_path_input",
            type='text',
            debounce=True,
            placeholder="I dont know to quarry"
        )," suffix:", dcc.Input(
            id="suffix_input",
            type='text',
            debounce=True,
            placeholder="I dont know to quarry",

        ),html.Div(id="content"),main_div," file name:", dcc.Input(
            id="file_name_tag",
            type='text',
            debounce=True,
            placeholder="I dont know to quarry"
        ),html.Button('save_files', id='btn-save_all', n_clicks=0),html.Div(id='placeholder',children='', style={'display':'none'}) ,html.Div(id='placeholder2',children='', style={'display':'none'})])

        @app.callback(Output('placeholder2','children'),[Input('file_name_tag','value'),Input('btn-save_all','n_clicks')])
        def save_file_names(value,btn):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0][:-len(".n_clicks")]
            if 'btn-save_all' in changed_id:
                files=''
                if not value in os.listdir(os.getcwd()):
                    os.mkdir(value)
                for i,f_name in enumerate(self.files):
                    if self.files_to_save[i]:
                        files+=f_name+'\n'
                        newPath = shutil.copy(f_name, value)
                # with open('%s.txt'%value, 'w') as f:
                #     f.write(files)

        @app.callback(Output('placeholder','children'),[Input('is_save_switch','on')])
        def save_image(is_save):
            if self.current_value is not None and self.current_value<len(self.files_to_save):
                self.files_to_save[self.current_value]=is_save
            return ''



        @app.callback(
            Output('my-slider', 'value'),
            Output('bool_switch', 'children'),
            Output('slider-output-container', "children"),
            Output('show_image_section', 'figure'),
            [
             Input('my-slider', 'value'),
             Input('btn-m50', 'n_clicks'),
             Input('btn-m10', 'n_clicks'),
             Input('btn-m5', 'n_clicks'),
             Input('btn-m1', 'n_clicks'),
             Input('btn-p1', 'n_clicks'),
             Input('btn-p5', 'n_clicks'),
             Input('btn-p10', 'n_clicks'),
             Input('btn-p50', 'n_clicks')
             ])
        def update_output(value, btnm50, btnm10, btnm5, btnm1, btnp1, btnp5, btnp10, btnp50):
            changed_id = [p['prop_id'] for p in callback_context.triggered][0][:-len(".n_clicks")]
            value = int(value)

            if 'btn-m' in changed_id:
                value -= int(changed_id[len('btn-m'):])
            elif 'btn-p' in changed_id:
                value += int(changed_id[len('btn-m'):])
            value = max(0, value)
            value = min(value, len(self.files))
            if len(self.files)>value:
                im = Image.open(self.files[value])
                fig = px.imshow(im)
                str_value=self.files[value]
                save_value=self.files_to_save[value]
            else:
                str_value=value
                fig=go.Figure()
                save_value=False
            self.current_value=value
            bool_switch= daq.BooleanSwitch(id="is_save_switch",label="save", on=save_value, color="red",
                                 style={'margin': '1', 'align': 'center', 'vertical-align': 'middle',
                                   "margin-left": "10px"})
            return value,bool_switch, 'You have selected "{}"'.format(str_value), fig
        @app.callback([Output('content', "children"),Output('main_div','style'),Output('slider_bar','children')],Input("base_path_input", "value"),Input("suffix_input", "value"))
        def insert_content(path,suffix):
            path=r"{}".format(path)
            suffix=r"{}".format(suffix)
            print(os.path.isdir(path))
            div,main_display ,input_values= self.display_images_div(path, suffix)
            return div,main_display,input_values
        app.run_server(debug=True, use_reloader=False,port=port)

    def display_images_div(self, base_path, suffix):
        slider=dcc.Slider(
                id='my-slider',
                min=0,
                max=-1,
                step=1,
                value=0,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        if not os.path.isdir(base_path):
            return html.Div(children='Not a valid directory path'),{'display':'none'},slider
        self.load_all_files_to_list(base_path, suffix)
        if len(self.files)==0:
            return html.Div(children='Are you sure about the suffix?'),{'display':'none'},slider
        return html.Div(children='good'),{'display':'inline'},dcc.Slider(
                id='my-slider',
                min=0,
                max=len(self.files) - 1,
                step=1,
                value=len(self.files) // 2,
                tooltip={"placement": "bottom", "always_visible": True}
            )

a=moriaFSystems()
a.display()
