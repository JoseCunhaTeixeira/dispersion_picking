import numpy as np
import plotly.graph_objects as go


def create_dispersion_figure(fv_map, fs, vs, picked_curve=None):

    fig = go.Figure()

    fv_map = (fv_map - np.min(fv_map, axis=1, keepdims=True)) / (
        np.max(fv_map, axis=1, keepdims=True)
        - np.min(fv_map, axis=1, keepdims=True)
        + 1e-12
    )

    fig.add_trace(
        go.Heatmap(
            z=fv_map.T,
            x=fs,
            y=vs,
            colorscale="Turbo",
            zsmooth=False,
            colorbar=dict(title="Amplitude"),
        )
    )

    if picked_curve is not None:
        fig.add_trace(
            go.Scatter(
                x=picked_curve[:, 0],
                y=picked_curve[:, 1],
                mode="lines",
                name="Picked Curve",
                line=dict(color="white", width=3),
            )
        )

    fig.update_layout(
        dragmode="lasso",
        height=850,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Frequency [Hz]",
        yaxis_title="Velocity [m/s]",
    )

    return fig
