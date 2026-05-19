from pathlib import Path

import numpy as np
from dash import Input, Output, State, no_update

from plotting import create_dispersion_figure
from services.dispersion_service import (
    extract_curve_from_polygon,
)
from services.io_service import load_h5_dispersion, save_picked_curve


def register_callbacks(app):

    @app.callback(
        Output("dispersion-graph", "figure"),
        Output("dispersion-store", "data"),
        Input("load-btn", "n_clicks"),
        State("h5-path", "value"),
        prevent_initial_call=True,
    )
    def load_dispersion(_, h5_path):

        fv_map, fs, vs = load_h5_dispersion(h5_path)

        fig = create_dispersion_figure(fv_map, fs, vs)

        data = {
            "fv_map": fv_map.tolist(),
            "fs": fs.tolist(),
            "vs": vs.tolist(),
            "path": h5_path,
        }

        return fig, data

    @app.callback(
        Output("picked-store", "data"),
        Output("dispersion-graph", "figure", allow_duplicate=True),
        Input("dispersion-graph", "selectedData"),
        State("dispersion-store", "data"),
        prevent_initial_call=True,
    )
    def pick_curve(selected_data, stored_data):

        if selected_data is None:
            return no_update, no_update

        if "lassoPoints" not in selected_data:
            return no_update, no_update

        polygon = np.column_stack(
            [selected_data["lassoPoints"]["x"], selected_data["lassoPoints"]["y"]]
        )
        fv_map = np.asarray(stored_data["fv_map"])

        fs = np.asarray(stored_data["fs"])

        vs = np.asarray(stored_data["vs"])

        f_pick, v_pick = extract_curve_from_polygon(fv_map, fs, vs, polygon)

        picked_curve = np.column_stack([f_pick, v_pick])

        fig = create_dispersion_figure(fv_map, fs, vs, picked_curve)

        return picked_curve.tolist(), fig

    @app.callback(
        Output("status", "children"),
        Input("save-btn", "n_clicks"),
        State("picked-name", "value"),
        State("picked-store", "data"),
        State("dispersion-store", "data"),
        prevent_initial_call=True,
    )
    def save_curve(n_clicks, picked_name, picked_data, dispersion_data):

        if picked_data is None:
            return "No picked curve."

        picked = np.asarray(picked_data)

        p = Path(dispersion_data["path"])

        if picked_name is None:
            output_path = p.with_name(p.name.replace("disp", "S0")).with_suffix(".csv")
        else:
            output_path = p.with_name(
                f"{p.stem.replace('disp', 'S0')}_{picked_name}"
            ).with_suffix(".csv")

        save_picked_curve(
            output_path,
            picked[:, 0],
            picked[:, 1],
            picked_name,
        )

        return f"Saved: {output_path}"
