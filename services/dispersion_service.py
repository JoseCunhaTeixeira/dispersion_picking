import numpy as np
from matplotlib.path import Path
from scipy.signal import savgol_filter


def extract_curve_from_polygon(FV, fs, vs, poly_coords, smooth=True):
    """
    Extracts f-v dispersion curve from f-v dispersion diagram by aiming maximums

    args :
        FV (2D numpy array) : dispersion diagram
        fs (1D numpy array) : frequency axis
        vs (1D numpy array) : velocity axis
        start (tuple of floats) : starting coordinates (f,v) values
        end (tuple of floats) : ending coordinates (f,v) values

    returns :
        curve (1D numpy array[velocity]) : f-v dispersion curve
    """

    FV = np.copy(FV)
    for i in range(FV.shape[0]):
        FV[i, :] = FV[i, :] / np.max(FV[i, :])

    df = fs[1] - fs[0]
    dv = vs[1] - vs[0]
    idx = np.zeros((len(poly_coords), 2), dtype=int)
    for i, (f, v) in enumerate(poly_coords):
        idx[i][0] = int((f - fs[0]) / df)
        idx[i][1] = int((v - vs[0]) / dv)

    # Make the low frequency limit of the polygon vertical to avoid the picking to follow the polygon limit at low frequencies
    idx[-1][0] = idx[0][0]

    poly_path = Path(idx)
    x, y = np.mgrid[: FV.shape[0], : FV.shape[1]]
    coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))

    mask = poly_path.contains_points(coors)
    mask = mask.reshape(FV.shape)

    FV_masked = FV * mask

    f_picked = []
    v_picked = []

    f_start_i = np.min(idx[:, 0])
    f_end_i = np.max(idx[:, 0])
    v_start_i = np.min(idx[:, 1])
    v_end_i = np.max(idx[:, 1])

    FV_tmp = FV_masked[f_start_i:f_end_i, v_start_i + 1 : v_end_i]

    for i, FV_f in enumerate(
        FV_tmp
    ):  # FV_f is a vector of velocities for a frequency f
        v_max_i = np.where(FV_f == FV_f.max())[0][0]
        v_max = vs[v_max_i + v_start_i]
        if v_max_i + v_start_i == v_end_i - 1 and i != 0:
            v_picked.append(v_picked[-1])
        else:
            v_picked.append(v_max)
        f_picked.append(fs[i + f_start_i])

    f_picked = np.array(f_picked)
    v_picked = np.array(v_picked)

    if not smooth:
        return f_picked[1:], v_picked[1:]

    if (len(v_picked) / 2) % 2 == 0:
        wl = len(v_picked) // 2 + 1
    else:
        wl = len(v_picked) // 2
    v_picked = savgol_filter(v_picked, window_length=wl, polyorder=3)
    return f_picked[1:], v_picked[1:]
