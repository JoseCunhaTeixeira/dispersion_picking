from dash import dcc, html


def create_layout():

    return html.Div(
        [
            html.H2("Dispersion Curve Picker"),
            html.Div(
                [
                    dcc.Input(
                        id="h5-path",
                        type="text",
                        placeholder="Path to disp_xxx.h5",
                        style={"width": "500px"},
                    ),
                    html.Button("Load", id="load-btn", n_clicks=0),
                ]
            ),
            html.Br(),
            dcc.Graph(
                id="dispersion-graph",
                config={"displayModeBar": True, "scrollZoom": True},
            ),
            html.Br(),
            html.Div(
                [
                    dcc.Input(
                        id="picked-name",
                        type="text",
                        placeholder="Name of picked curve",
                        style={"width": "500px"},
                    ),
                    html.Button("Save Pick", id="save-btn", n_clicks=0),
                ]
            ),
            # html.Button("Save Pick", id="save-btn"),
            html.Div(id="status"),
            dcc.Store(id="dispersion-store"),
            dcc.Store(id="picked-store"),
        ]
    )
