import numpy as np
from sph_harm import sph_r


def test_sph_r_finite_values():
    """sph_r accepts Nx3 cartesian coords and returns finite values."""
    xyz = np.array([[0.0, 0.0, 1.0],
                     [1.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0]], dtype=float)
    # l=1 with m=None -> returns N x 3 real harmonics
    y = sph_r(xyz, l=1, m=None)
    assert y.shape == (3, 3)
    assert np.all(np.isfinite(y))

    # l=1 with specific m -> returns N-vector
    y_m = sph_r(xyz, l=1, m=0)
    assert y_m.shape == (3,)
    assert np.all(np.isfinite(y_m))
