from credit_institute_scraper.dashapp.app import dash_app as app
from .pages import page_not_found, home, plots
from dash import Output, Input
from dash.exceptions import PreventUpdate
from ..database.sqlite_conn import query_db
import plotly.graph_objects as go
import datetime as dt
import pandas as pd
import inspect

date = dt.date(2022, 9, 16)
df = query_db("select * from prices where date(timestamp) = :date", params={'date': date})


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.home_page()
    elif pathname == "/Plots":
        return plots.plot_page()
    # If the user tries to reach a different page, return a 404 message
    return page_not_found.page_not_found(pathname)


@app.callback(Output("daily_plot", "figure"), [Input("select_institute_daily_plot", "value"),
                                               Input("select_coupon_daily_plot", "value"),
                                               Input("select_ytm_daily_plot", "value"),
                                               Input("select_max_io_daily_plot", "value")])
def update_daily_plot(institute, coupon_rate, years_to_maturity, max_interest_only_period):
    global df

    argspec = inspect.getargvalues(inspect.currentframe())
    sql = "select * from prices where date(timestamp) = :date"

    filters = []
    for arg in argspec.args:
        if argspec.locals[arg] is not None:
            sql += f" and {arg} = :{arg}"
        else:
            filters.append(arg)

    df = query_db(sql, params={**locals(), 'date': date})

    scatters = []
    groups = df.groupby(filters) if filters else [('', df)]
    for g, tmp_df in groups:
        g = g if isinstance(g, (list, tuple)) else [g]
        scatters.append(go.Scatter(x=tmp_df['timestamp'],
                                   y=tmp_df['spot_price'],
                                   line=dict(width=3),
                                   name='<br>'.join(f'{f}: {v}' for f, v in zip(filters, g)),
                                   line_shape='hv',
                                   showlegend=True
                                   ))
    fig = go.Figure(scatters)
    fig.update_layout(title=f'Daily spot prices',
                      xaxis_title='Timestamp',
                      yaxis_title='Spot price',
                      )
    return fig


@app.callback([Output('select_institute_daily_plot', 'options'),
               Output('select_coupon_daily_plot', 'options'),
               Output('select_ytm_daily_plot', 'options'),
               Output('select_max_io_daily_plot', 'options')],
              Input('daily_plot', 'figure')
)
def update_dropdowns(_):
    inst = [{'label': opt, 'value': opt} for opt in sorted(df['institute'].unique())]
    coup = [{'label': opt, 'value': opt} for opt in sorted(df['coupon_rate'].unique())]
    ytm = [{'label': opt, 'value': opt} for opt in sorted(df['years_to_maturity'].unique())]
    maxio = [{'label': opt, 'value': opt} for opt in sorted(df['max_interest_only_period'].unique())]
    return inst, coup, ytm, maxio


# @app.callback([Output('select_coupon_daily_plot', 'options'), Output('select_ytm_daily_plot', 'options'), Output('select_max_io_daily_plot', 'options')],
#               Input('select_institute_daily_plot', 'value'))
# def update_dropdowns1(n):
#     if n is None:
#         raise PreventUpdate
#     # inst = [{'label': opt, 'value': opt} for opt in sorted(df['institute'].unique())]
#     coup = [{'label': opt, 'value': opt} for opt in sorted(df['coupon_rate'].unique())]
#     ytm = [{'label': opt, 'value': opt} for opt in sorted(df['years_to_maturity'].unique())]
#     maxio = [{'label': opt, 'value': opt} for opt in sorted(df['max_interest_only_period'].unique())]
#     return coup, ytm, maxio

#
# @app.callback([Output('select_institute_daily_plot', 'options'), Output('select_ytm_daily_plot', 'options'), Output('select_max_io_daily_plot', 'options')],
#               Input('select_coupon_daily_plot', 'value'))
# def update_dropdowns2(_):
#     inst = [{'label': opt, 'value': opt} for opt in sorted(df['institute'].unique())]
#     # coup = [{'label': opt, 'value': opt} for opt in sorted(df['coupon_rate'].unique())]
#     ytm = [{'label': opt, 'value': opt} for opt in sorted(df['years_to_maturity'].unique())]
#     maxio = [{'label': opt, 'value': opt} for opt in sorted(df['max_interest_only_period'].unique())]
#     return inst, ytm, maxio
#
#
# @app.callback([Output('select_institute_daily_plot', 'options'), Output('select_coupon_daily_plot', 'options'), Output('select_max_io_daily_plot', 'options')],
#               Input('select_ytm_daily_plot', 'value'))
# def update_dropdowns3(_):
#     inst = [{'label': opt, 'value': opt} for opt in sorted(df['institute'].unique())]
#     coup = [{'label': opt, 'value': opt} for opt in sorted(df['coupon_rate'].unique())]
#     # ytm = [{'label': opt, 'value': opt} for opt in sorted(df['years_to_maturity'].unique())]
#     maxio = [{'label': opt, 'value': opt} for opt in sorted(df['max_interest_only_period'].unique())]
#     return inst, coup, maxio
#
#
# @app.callback([Output('select_institute_daily_plot', 'options'), Output('select_coupon_daily_plot', 'options'), Output('select_ytm_daily_plot', 'options')],
#               Input('select_max_io_daily_plot', 'value'))
# def update_dropdowns4(_):
#     inst = [{'label': opt, 'value': opt} for opt in sorted(df['institute'].unique())]
#     coup = [{'label': opt, 'value': opt} for opt in sorted(df['coupon_rate'].unique())]
#     ytm = [{'label': opt, 'value': opt} for opt in sorted(df['years_to_maturity'].unique())]
#     # maxio = [{'label': opt, 'value': opt} for opt in sorted(df['max_interest_only_period'].unique())]
#     return inst, coup, ytm
#
#
