from . import styles
import dash_bootstrap_components as dbc
from dash import html, dcc


sidebar = html.Div(
    [
        html.I(className="app__header",
               style={'background-image': 'url(/assets/favicon.ico)',
                      'height': '16rem',
                      'background-size': '100%'}),
        html.H3("Bond stats", className='app__header'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Daily changes", href="/daily", active="exact"),
                dbc.NavLink("Historical changes", href="/historical", active="exact"),
                dbc.NavLink("About", href="/about", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id='sidebar',
    style=styles.SIDEBAR_STYLE,
    className='sidebar'
)

content = html.Div(id="page-content", style=styles.CONTENT_STYLE)
layout = html.Div(
    [
        html.Div(id='dummy1', style={'display': 'none'}),
        html.Div(id='dummy2', style={'display': 'none'}),
        dcc.Store(id='daily_store', data=None),
        dcc.Store(id='master_data', data=None),
        dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
        html.Div(id='date_range_div', style={'display': 'none'}),
        dcc.Loading(type="default", children=html.Div(id="loading-spinner-output1"), className='spinner'),
        dcc.Store(id='side_click'),
        dcc.Location(id="url", refresh=False),
        dbc.Button("Hide", outline=True, id="btn_sidebar", className='sidebar-btn'),
        sidebar,
        content
     ]
)
