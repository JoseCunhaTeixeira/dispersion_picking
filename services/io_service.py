from pathlib import Path

import h5py
import numpy as np


def load_h5_dispersion(filepath):
    """
    Load dispersion image from HDF5.
    """

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(filepath)

    with h5py.File(filepath, "r") as f:
        fv_map = f["fv_map"][:]
        fs = f["fs"][:]
        vs = f["vs"][:]

    return fv_map, fs, vs


def save_picked_curve(output_path, frequencies, velocities, name=None):

    arr = np.column_stack([frequencies, velocities])

    if name is None:
        header = "frequency_Hz,phase_velocity_m/s"
    else:
        header = f"name: {name}\nfrequency_Hz,phase_velocity_m/s"
    np.savetxt(
        output_path,
        arr,
        header=header,
        delimiter=",",
        fmt="%.6f",
    )


def load_picked_curve(path):

    data = np.loadtxt(path)

    if data.ndim == 1:
        data = data.reshape(1, -1)

    return data
