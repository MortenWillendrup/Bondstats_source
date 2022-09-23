# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#031333",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "padding": "2rem 1rem",
}

ROW_STYLE = {
    "align": "center",
    "style": {"margin-left": "4px",
              "margin-right": "4px"}
}

DROPDOWN_STYLE = {
    "style": {"border": "none"}
}

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

GRAPH_STYLE = dict(
    plot_bgcolor=app_color["graph_bg"],
    paper_bgcolor=app_color["graph_bg"],
    font={"color": "#fff"},
    # height="100%",
    xaxis={
        "title": "Time (UTC)",
        "showline": True,
        "zeroline": False,
        "fixedrange": True,
        "showgrid": True,
        "gridcolor": "#676565",
        "minor_griddash": "dot",
        "nticks": 8,
        # "showspikes": True
    },
    yaxis={
        "showgrid": True,
        "showline": True,
        # "fixedrange": True,
        "zeroline": False,
        "gridcolor": "#676565",
        "minor_griddash": "dot"
    },
    legend={
        "font": {"size": 10}
    }
)
