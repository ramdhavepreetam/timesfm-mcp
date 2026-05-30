"""Smoke tests for the baseline forecaster — keeps the repo green pre-TimesFM."""

import numpy as np

from forecast_mcp.backends import BaselineBackend, select_backend


def _seasonal_series(n=48, season=12):
    t = np.arange(n)
    return list(10 + 0.5 * t + 5 * np.sin(2 * np.pi * t / season))


def test_forecast_shape():
    res = BaselineBackend().forecast(_seasonal_series(), horizon=6, quantiles=[0.9], season_length=None)
    assert res.horizon == 6
    assert len(res.points) == 6
    assert all(p.lower is not None and p.upper is not None for p in res.points)


def test_bands_widen_with_horizon():
    res = BaselineBackend().forecast(_seasonal_series(), horizon=10, quantiles=[0.9], season_length=12)
    widths = [p.upper - p.lower for p in res.points]
    assert widths[-1] >= widths[0]  # uncertainty grows further out


def test_detects_rising_trend():
    res = BaselineBackend().forecast(_seasonal_series(), horizon=3, quantiles=[], season_length=12)
    assert res.context.trend == "rising"


def test_too_short_raises():
    try:
        BaselineBackend().forecast([1.0, 2.0], horizon=3, quantiles=[], season_length=None)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_select_backend_falls_back():
    # No timesfm installed in CI -> baseline.
    assert select_backend(prefer_timesfm=True).name in {"baseline", "timesfm"}
