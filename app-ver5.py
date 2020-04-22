import os
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bio
import dash_table
import pandas as pd
from dash_bio_utils.xyz_reader import read_xyz
from six import PY3
from dash.dependencies import Input,Output,State
import dash_bootstrap_components as dbc

# Path to datasource. Using os.path,join to get the absolute path to data source
# the name 'data' is the folder contain all the .xyz files
DATAPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')

#structure = set(df['Metal_Oxides'])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_bootstrap = ['https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/sandstone/bootstrap.min.css']
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX,
# MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI

app = dash.Dash(external_stylesheets=dash_bootstrap)
app.scripts.config.serve_locally = True
app.config["suppress_callback_exceptions"] = True
server = app.server
# ------------------------------
# Defaults slider
# User can use the slider to adjust the atom size, color, brightness, ect. of a structure.
# Source of code = open source from Dash-Speck
default_sliders = [
    html.Div(className='app-controls-block', children=[
        html.Div(
            "Atom radius",
            className='app-controls-name'
        ),
        dcc.Slider(
            id='speck-atom-radius',
            className='control-slider',
            max=1,
            step=0.01,
            value=0.6,
            updatemode='drag'
        ),
    ]),
    html.Div(className='app-controls-block', children=[
        html.Div(
            "Relative atom radius",
            className='app-controls-name'
        ),
        dcc.Slider(
            id='speck-relative-atom-radius',
            className='control-slider',
            max=1,
            step=0.01,
            value=1.0,
            updatemode='drag'
        ),
    ]),

    html.Div(className='app-controls-block', children=[
        html.Div(
            "Brightness",
            className='app-controls-name'
        ),
        dcc.Slider(
            id='speck-brightness',
            className='control-slider',
            max=1,
            step=0.01,
            value=0.5,
            updatemode='drag'
        )
    ]),

    html.Hr(),
    dcc.Checklist(
        id='speck-show-hide-bonds',
        options=[
            {'label': 'Show bonds',
             'value': 'True'}
        ],
        value=[]
    ),
    html.Div(className='app-controls-block', children=[
        html.Div(
            'Bond scale',
            className='app-controls-name'
        ),
        dcc.Slider(
            id='speck-bond-scale',
            className='control-slider',
            max=1,
            step=0.01,
            value=0.5,
            updatemode='drag'
        )
    ])

]
# --------------------------------------------------------
# PAGE LAYOUT & CONTENTS
# In an effort to clean up the code, and easily to go back and make some adjustments for the future
# I decided to break it apart into sections.
# LEFT-COLUMN is the info about the view, which contain TABS, like 'about', 'structure',..
# RIGHT-COLUMN is the viewing area. Future work, there will be three columns. One is the info, one is the
# structure before and one is the structure after. For now, just work on one
# By breaking this into sections, it will be easy to find the right spot to add to or change without having
# to count too many brackets.
# ----------------------------------------------------------
LOGO = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    #dbc.Col(html.Img(src='dash-logo.png',height='30px')),
                    dbc.Col(
                        dbc.NavbarBrand('Surface SLABView',className='label')),
                ],
                align = 'center',
                no_gutters = True,
            ),
        )
    ],
    color='dark',
    dark=True,
    sticky='top',
)


MOL_LOADING= html.Div(id='speck-body',
                      className='app-body',
                      children=[
                          dcc.Loading(className='dashbio-loading',
                                      children=html.Div(
                                          id='speck-container',
                                          children=[
                                              dash_bio.Speck(
                                                  id='speck',
                                                  view={'resolution':600, 'zoom':0.1},
                                                  scrollZoom=True
                                              )
                                          ]),
                                      )
                      ]
)

LEFT_COLUMN =dbc.Jumbotron(
    [
        html.Div(id='speck-control-tabs',
                 className='control-tabs',
                 children=[
                     dcc.Tabs(id='speck-tabs',
                              value='what-is',
                              children=[
                                  dcc.Tab(
                                      label='Structure',
                                      value='datasets',
                                      children=[
                                          html.Div(className='control-tab',
                                                   children=[
                                                       html.Div(
                                                           className='app-controls-block',
                                                           children=[
                                                               html.Div(className='app-controls-name',
                                                                        children=[html.H4('Structure')]),
                                                               dcc.Dropdown(id='speck-molecule-dropdown',
                                                                            className='speck-dropdown',
                                                                            options=[
                                                                                {'label': 'Fe2O3-H2O-P1',
                                                                                 'value': os.path.join(DATAPATH, 'Fe2O3_H2O_P1.xyz')},
                                                                                {'label': 'Fe2O3-H2O-P2',
                                                                                 'value': os.path.join(DATAPATH,'Fe2O3_H2O_P2.xyz')},
                                                                                {'label': 'Fe2O3-H2O-P3',
                                                                                 'value': os.path.join(DATAPATH,'Fe2O3_H2O_P3.xyz')},
                                                                                {'label': 'Al2O3-H2O-P1',
                                                                                 'value': os.path.join(DATAPATH,'Al2O3_H2O_P1.xyz')},
                                                                                {'label': 'Al2O3-H2O-P2',
                                                                                 'value': os.path.join(DATAPATH,'Al2O3_H2O_P2.xyz')},
                                                                                {'label': 'Al2O3-H2O-P3',
                                                                                 'value': os.path.join(DATAPATH,'Al2O3_H2O_P3.xyz')},
                                                                                {'label': 'Cr2O3-CO-P1',
                                                                                 'value': os.path.join(DATAPATH, 'Cr2O3_CO_P1.xyz')},
                                                                                {'label': 'Cr2O3-CO-P2',
                                                                                 'value': os.path.join(DATAPATH,'Cr2O3_CO_P2.xyz')},
                                                                                {'label': 'Cr2O3-CO-P3',
                                                                                 'value': os.path.join(DATAPATH,'Cr2O3_CO_P3.xyz')},
                                                                                {'label': 'Al2O3',
                                                                                 'value': os.path.join(DATAPATH, 'Al2O3.xyz')},
                                                                                {'label': 'Fe2O3',
                                                                                 'value': os.path.join(DATAPATH, 'Fe2O3.xyz')},
                                                                                {'label': 'Cr2O3',
                                                                                 'value': os.path.join(DATAPATH, 'Cr2O3.xyz')}
                                                                                ],
                                                                            value=os.path.join(DATAPATH, 'Fe2O3.xyz')
                                                               )
                                                            ]),
                                                       html.Div(id='speck-preloaded-oploaded-alert'),
                                                       dcc.Upload(id='speck-file-upload',
                                                                  className='control-upload',
                                                                  children= html.Div(['Drag and drop .xyz files here ']),
                                                                  style={
                                                                      'width': '100%',
                                                                      'height': '60px',
                                                                      'lineHeight': '60px',
                                                                      'borderWidth': '1px',
                                                                      'borderStyle': 'dashed',
                                                                      'borderRadius': '5px',
                                                                      'textAlign': 'center',
                                                                      'margin': '10px'
                                                                  }
                                                                  ),
                                                       html.A(
                                                           html.Button(
                                                               'Download sample .xyz data',
                                                               id='speck-file-download',
                                                               className='control-download'
                                                           ),
                                                           href=os.path.join(DATAPATH,'Fe2O3.xyz'),
                                                           download='Fe2O3.xyz'
                                                           )
                                                       ])
                                  ]),
                                  dcc.Tab(
                                      label='Render',
                                      value='view-options',
                                      children=html.Div(className='control-tab',
                                                        children=[
                                                            dcc.Checklist(
                                                                id='speck-enable-presets',
                                                                options=[{'label': 'Use presets', 'value': 'True'}],
                                                                value=[]
                                                            ),
                                                            html.Hr(),
                                                            html.Div(id='speck-controls-detailed', children=default_sliders),
                                                            html.Div(
                                                                id='speck-controls-preset',
                                                                className='speck-controls',
                                                                children=[
                                                                    html.Div(className='app-controls-block',
                                                                             children=[
                                                                                 html.Div(className='app-controls-name',
                                                                                          children='Rendering style'),
                                                                                 dcc.Dropdown(
                                                                                     id='speck-preset-rendering-dropdown',
                                                                                     className='speck-dropdown',
                                                                                     options=[
                                                                                         {'label':'Default',
                                                                                          'value':'default'},
                                                                                         {'label': 'Toon',
                                                                                          'value': 'toon'},
                                                                                     ],
                                                                                     value='default'
                                                                                     )
                                                                                 ]),
                                                                    html.Div(className='app-controls-block',
                                                                             children=[
                                                                                 html.Div(className='app-controls-name',
                                                                                          children='Atom style'),
                                                                                 dcc.Dropdown(
                                                                                     id='speck-preset-atom-style-dropdown',
                                                                                     className='speck-dropdown',
                                                                                     options=[
                                                                                         {'label':'Ball-and-stick',
                                                                                          'value':'stickball'},
                                                                                         {'label': 'Licorice',
                                                                                          'value': 'licorice'},
                                                                                     ],
                                                                                     value='stickball'
                                                                                 )
                                                                             ])
                                                                    ])
                                                            ])),
                                  dcc.Tab(
                                      label='About',
                                      value='what-is',
                                      children=html.Div(className='control-tab',
                                                        children=[
                                                            html.H4(className='what-is',
                                                                    children='What is SLABView?'),
                                                            html.P('SLABView is a Web-GL based molecule renderer.'
                                                                   "It's a web-based dashboard which were built on Dash-"
                                                                   "Speck component using ambient occlusion so that when you"
                                                                   "zoom in, the rendering does not suffer."
                                                                   ),
                                                            html.P('"Structure" tab - provides molecule slab structure. '),
                                                            html.P('"Render" tab - allows user to control parameters related'
                                                                   'to the appearance of the molecule.'),
                                                            html.P('These can be controlled using the provided sliders'
                                                                   'or preset view can be used when viewing the structure.'),
                                                            #html.P('I')
                                                        ])
                                  ),

                              ])
                     ]),
        dcc.Store(
            id='speck-store-preset-rendering',
            data= None
            ),
        dcc.Store(
            id='speck-store-preset-atom-style',
            data=None
            ),
])
# Adding DATA_TABLE
df = pd.read_csv(os.path.join(DATAPATH, 'results_table.csv'))

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
}
available_metaloxides = df['Metal_Oxides'].unique()

RESULTS= html.Div([
    html.Div([
        html.Div([
            dcc.Graph(
                id='results-graph',
                #hoverData={'points':[{'customdata':'Al2O3'}]}
            )
            ],#style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
        )
    ]),
    html.Div(
        html.Div(className='row',
                      children=[
                          dbc.Card(dbc.CardBody([
                              dcc.Store(id='results-output'),
                              html.Div(className='columns results-table',
                                       children=[
                                           dbc.Table.from_dataframe(df,
                                                                striped=True,
                                                                bordered=True,
                                                                hover=True),
                                           ]),
                              ]),
                         #className='w-50',
                          )
                      ])

        )
    ])

# DATA_TABLE = html.Div(className='row',
#                       children=[
#                           dbc.Card(dbc.CardBody([
#                               dcc.Store(id='results-output'),
#                               html.Div(className='columns-results-table',
#                                        children=[html.Div(dash_table.DataTable(id='table',
#                                                                                columns=['name': i, for i in df.columns]
#                                        ))])
#
#                                            # dbc.Table.from_dataframe(df,
#                                            #                      # striped=True,
#                                            #                      # bordered=True,
#                                            #                      # hover=True),
#                                            #]),
#                               ]),
#                          #className='w-50',
#                           )
#                       ])

# ------------------------------------------------------------------------------------------
# callback functions
def callbacks(_app):
    @_app.callback(
        Output('speck-controls-detailed', 'style'),
        [Input('speck-enable-presets', 'value')]
    )
    def show_hide_detailed_controls(presets_enable):
        if len(presets_enable) > 0:
            return {'display': 'none'}
        return {'display': 'inline-block'}

    @_app.callback(
        Output('speck-controls-preset', 'style'),
        [Input('speck-enable-presets', 'value')]
    )
    def show_hide_preset_controls(presets_enable):
        if len(presets_enable) == 0:
            return {'display': 'none'}
        return {'display': 'inline-block'}

    @_app.callback(
        Output('speck-molecule-dropdown', 'value'),
        [Input('speck-file-upload', 'contents')],
        state=[State('speck-molecule-dropdown', 'value')]
    )
    def clear_preloaded_on_upload(upload_contents, current):
        if upload_contents is not None:
            return None
        return current

    @_app.callback(
        Output('speck-preloaded-uploaded-alert', 'children'),
        [Input('speck-molecule-dropdown', 'value'),
         Input('speck-file-upload', 'contents')],
        state=[State('speck-file-upload', 'filename')]
    )
    def alert_preloaded_and_uploaded(molecule_fname, upload_contents, upload_fname):
        if molecule_fname is not None and upload_contents is not None:
            return 'Warning: you have uploaded a dataset ({}). To view the \
	            dataset, please ensure that the "Preloaded" dropdown has \
	            been cleared.'.format(upload_fname)
        return ''

    @_app.callback(
        Output('speck', 'data'),
        [Input('speck-molecule-dropdown', 'value'),
         Input('speck-file-upload', 'contents')]
    )
    def update_molecule(molecule_fname, upload_contents):
        data = {}
        if upload_contents is not None and molecule_fname is None:
            try:
                content_type, content_string = upload_contents.split(',')
                data = base64.b64decode(content_string).decode('UTF-8')
            except AttributeError:
                pass
            data = read_xyz(data, is_datafile=False)
        elif molecule_fname is not None:
            data = read_xyz(molecule_fname)
        return data
# this callback use to set the view option, in "return", the '__'is thr list of views can be found in dash.Speck view
# When adding more viewing options, make sure to adjust the defaults sliders and update the change_view function
# and the return
    @_app.callback(
        Output('speck', 'view'),
        [Input('speck-enable-presets', 'value'),
         Input('speck-atom-radius', 'value'),
         Input('speck-relative-atom-radius', 'value'),
         Input('speck-show-hide-bonds', 'value'),
         Input('speck-bond-scale', 'value'),
         Input('speck-brightness', 'value'),
         ]
    )
    def change_view(
            presets_enabled,
            atom_radius,
            relative_atom_radius,
            show_bonds,
            bond_scale,
            brightness,
    ):
        return {
            'atomScale': atom_radius,
            'relativeAtomScale': relative_atom_radius,
            'bonds': bool(len(show_bonds) > 0),
            'bondScale': bond_scale,
            'brightness': brightness,
        }

    @_app.callback(
        Output('speck-store-preset-rendering', 'data'),
        [Input('speck-preset-rendering-dropdown', 'value')]
    )
    def update_rendering_option(render):
        return render

    @_app.callback(
        Output('speck-store-preset-atom-style', 'data'),
        [Input('speck-preset-atom-style-dropdown', 'value')]
    )
    def update_atomstyle_option(atomstyle):
        return atomstyle

    @_app.callback(
        Output('speck', 'presetView'),
        [Input('speck-store-preset-atom-style', 'modified_timestamp'),
         Input('speck-store-preset-rendering', 'modified_timestamp')],
        state=[State('speck-preset-rendering-dropdown', 'value'),
               State('speck-preset-atom-style-dropdown', 'value')]
    )
    def preset_callback(
            atomstyle_ts, render_ts,
            render, atomstyle
    ):
        preset = 'default'
        if atomstyle_ts is None and render_ts is None:
            return preset
        if atomstyle_ts is not None and render_ts is None:
            preset = atomstyle
        elif atomstyle_ts is None and render_ts is not None:
            preset = render
        else:
            if render_ts > atomstyle_ts or atomstyle is None:
                preset = render
            else:
                preset = atomstyle
        return preset

    @_app.callback(
        Output('speck-preset-atom-style-dropdown', 'value'),
        [Input('speck-preset-rendering-dropdown', 'value')],
        state=[State('speck-preset-atom-style-dropdown', 'value')]
    )
    def keep_atom_style(render, current):
        if render == 'stickball':
            return None
        return current
    # @_app.callback(
    #     [
    #         Output('results-graph','figure'),
    #         #Output('results-table','columns'),
    #         #Output('results-table','data'),
    #      ],
    #     [Input('speck-molecule-dropdown','value')],
    # )
    # def update_graph(xaxis_column_name,yaxis_column_name,):
    #     return {
    #         'data': [dict(
    #             x=df[df['Positions'] == xaxis_column_name],
    #             y=df[df['Adsorption_energy_eV'] == yaxis_column_name],
    #             mode='markers',
    #             marker={
    #             'size': 15,
    #             'opacity': 0.5,
    #             'line': {'width': 0.5, 'color': 'white'}
    #         }
    #     )],
    #         'layout': dict(
    #             xaxis={
    #             'title': xaxis_column_name,
    #         },
    #             yaxis={
    #             'title': yaxis_column_name,
    #         },
    #             margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
    #             height=450,
    #             hovermode='closest'
    #     )
    # }

# -------------------
# Adding callbacks for table and graph
#     @_app.callback(
#         [
#             Output('results-table','data'),
#             [Input('')]
#
#         ]
#     )
# ------------------------------------------------------------------------------------------

BODY =dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN,md=4),
                dbc.Col(MOL_LOADING,width='auto'),
            ],
            #style={'marginTop':30},
            no_gutters=True
        ),
        dbc.Row(RESULTS),
    ],
    fluid=True,
)

#(children=[LEFT_COLUMN,heading]) use this in the app.layout below after update the heading
app.layout = html.Div(children=[LOGO,BODY])
if __name__=='__main__':
    #app.layout = layout()
    callbacks(app)
    app.run_server(debug=True)