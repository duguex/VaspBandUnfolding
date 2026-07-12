import numpy as np
from spline import splcof


def test_splcof_returns_callable():
    """splcof returns a callable cubic spline evaluator."""
    x = np.linspace(0, 1, 11)
    y = x ** 2
    spline_fn = splcof(x, y)
    assert callable(spline_fn)

    # The returned cubicspline requires x0.size > x.size (assertion inside)
    x0 = np.linspace(0, 1, 101)
    result = spline_fn(x0)
    assert result is not None
    assert len(result) == len(x0)
    assert np.all(np.isfinite(result))
