"""Forecast backends.

Two implementations behind one interface:

* ``BaselineBackend`` -- pure NumPy seasonal-naive + linear trend. No heavy deps,
  runs instantly. This is what makes the server usable in 30 seconds.
* ``TimesFMBackend`` -- wraps Google's TimesFM 2.5 foundation model. Loaded lazily.
  Uses the user's own ``timesfm`` install if present; otherwise falls back to the
  vendored copy bundled in ``timesfm_mcp._timesfm`` (Apache-2.0, Google LLC).
  Either way, requires ``torch`` — install via ``pip install "timesfm-mcp[timesfm]"``.

The server auto-selects TimesFM when available and falls back to the baseline,
so the tool always returns *something* useful.
"""

from __future__ import annotations

import math
from typing import Protocol

import numpy as np

from .models import ForecastPoint, ForecastResult, SeriesContext

# Z-scores for common symmetric quantile bands.
_Z = {0.80: 1.2816, 0.90: 1.6449, 0.95: 1.9600}


def _detect_season_length(values: np.ndarray) -> int:
    """Cheap autocorrelation-based season detection. Returns 1 if none stands out."""
    n = len(values)
    if n < 8:
        return 1
    x = values - values.mean()
    best_lag, best_corr = 1, 0.0
    for lag in range(2, min(n // 2, 60) + 1):
        a, b = x[:-lag], x[lag:]
        denom = np.sqrt((a**2).sum() * (b**2).sum())
        if denom == 0:
            continue
        corr = float((a * b).sum() / denom)
        if corr > best_corr:
            best_lag, best_corr = lag, corr
    return best_lag if best_corr > 0.35 else 1


def _build_context(values: np.ndarray, season: int, resid_std: float) -> SeriesContext:
    n = len(values)
    idx = np.arange(n)
    slope = float(np.polyfit(idx, values, 1)[0]) if n >= 2 else 0.0
    mean = float(values.mean()) or 1e-9
    pct = slope / abs(mean) * 100
    trend = "rising" if pct > 0.5 else "falling" if pct < -0.5 else "flat"
    return SeriesContext(
        n_observations=n,
        detected_season_length=season,
        trend=trend,
        trend_pct_per_step=round(pct, 3),
        last_value=float(values[-1]),
        mean=round(mean, 4),
        volatility=round(resid_std, 4),
    )


class Backend(Protocol):
    name: str

    def forecast(
        self, values: list[float], horizon: int, quantiles: list[float], season_length: int | None
    ) -> ForecastResult: ...


class BaselineBackend:
    """Seasonal-naive + linear trend with residual-based uncertainty bands."""

    name = "baseline"

    def forecast(self, values, horizon, quantiles, season_length):
        v = np.asarray(values, dtype=float)
        if len(v) < 3:
            raise ValueError("Need at least 3 observations to forecast.")

        season = season_length or _detect_season_length(v)
        idx = np.arange(len(v))
        slope, intercept = (np.polyfit(idx, v, 1) if len(v) >= 2 else (0.0, v[-1]))
        detrended = v - (slope * idx + intercept)

        # In-sample residuals to size the uncertainty bands.
        resid_std = float(detrended.std()) if len(v) > 2 else 0.0

        points: list[ForecastPoint] = []
        for h in range(1, horizon + 1):
            t = len(v) - 1 + h
            trend_part = slope * t + intercept
            if season > 1:
                season_part = detrended[-season + ((h - 1) % season)]
            else:
                season_part = 0.0
            mean = float(trend_part + season_part)
            # Bands widen with the forecast horizon.
            spread = resid_std * math.sqrt(h)
            z = _Z.get(max(quantiles), 1.6449) if quantiles else 0.0
            points.append(
                ForecastPoint(
                    step=h,
                    value=round(mean, 6),
                    lower=round(mean - z * spread, 6) if quantiles else None,
                    upper=round(mean + z * spread, 6) if quantiles else None,
                )
            )

        return ForecastResult(
            backend=self.name,
            horizon=horizon,
            points=points,
            context=_build_context(v, season, resid_std),
            notes=["Statistical baseline (seasonal-naive + trend). Install the 'timesfm' extra for the foundation model."],
        )


def _load_timesfm_module():
    """Return a timesfm-2.5-compatible module, or None if torch is absent.

    Priority: user's own ``import timesfm`` (if it has the 2.5 API) →
    vendored ``timesfm_mcp._timesfm`` → None.
    """
    # 1. User's own install takes priority.
    try:
        import timesfm as _tfm
        if hasattr(_tfm, "TimesFM_2p5_200M_torch") or hasattr(_tfm, "TimesFM_2p5_200M_flax"):
            return _tfm
    except Exception:
        pass
    # 2. Bundled vendored copy (requires torch from the [timesfm] extra).
    try:
        from timesfm_mcp import _timesfm as _tfm
        if hasattr(_tfm, "TimesFM_2p5_200M_torch") or hasattr(_tfm, "TimesFM_2p5_200M_flax"):
            return _tfm
    except Exception:
        pass
    return None


class TimesFMBackend:
    """Wraps TimesFM 2.5. Model is loaded once, lazily, on first call."""

    name = "timesfm"

    def __init__(self) -> None:
        self._model = None

    def _load(self):
        if self._model is not None:
            return self._model
        tfm = _load_timesfm_module()
        if tfm is None:
            raise ImportError("TimesFM 2.5 requires torch. Install with: pip install 'timesfm-mcp[timesfm]'")

        self._model = tfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
        self._model.compile(
            tfm.ForecastConfig(
                max_context=1024,
                max_horizon=256,
                normalize_inputs=True,
                use_continuous_quantile_head=True,
                force_flip_invariance=True,
                infer_is_positive=True,
                fix_quantile_crossing=True,
            )
        )
        return self._model

    def forecast(self, values, horizon, quantiles, season_length):
        v = np.asarray(values, dtype=float)
        if len(v) < 3:
            raise ValueError("Need at least 3 observations to forecast.")

        if len(v) > 1024:
            v = v[-1024:]

        season = season_length or _detect_season_length(v)
        idx = np.arange(len(v))
        slope, intercept = (np.polyfit(idx, v, 1) if len(v) >= 2 else (0.0, v[-1]))
        detrended = v - (slope * idx + intercept)
        resid_std = float(detrended.std()) if len(v) > 2 else 0.0

        model = self._load()
        point_forecast, quantile_forecast = model.forecast(
            horizon=horizon,
            inputs=[v],
        )

        pts = point_forecast[0]
        qts = quantile_forecast[0] if quantile_forecast is not None else None

        points: list[ForecastPoint] = []
        for h in range(horizon):
            mean_val = float(pts[h])
            lower_val = None
            upper_val = None
            if quantiles and qts is not None:
                q_levels = np.linspace(0.1, 0.9, 9)
                target = max(quantiles)
                lower_pct = (1.0 - target) / 2.0
                upper_pct = 1.0 - lower_pct
                lower_val = float(np.interp(lower_pct, q_levels, qts[h][1:10]))
                upper_val = float(np.interp(upper_pct, q_levels, qts[h][1:10]))

            points.append(
                ForecastPoint(
                    step=h + 1,
                    value=round(mean_val, 6),
                    lower=round(lower_val, 6) if lower_val is not None else None,
                    upper=round(upper_val, 6) if upper_val is not None else None,
                )
            )

        notes = ["Used TimesFM 2.5 foundation model."]
        if quantiles:
            notes.append("Note: Quantile bands were linearly interpolated from the model's 10th-90th deciles.")

        return ForecastResult(
            backend=self.name,
            horizon=horizon,
            points=points,
            context=_build_context(v, season, resid_std),
            notes=notes,
        )


def select_backend(prefer_timesfm: bool = True) -> Backend:
    if prefer_timesfm and _load_timesfm_module() is not None:
        return TimesFMBackend()
    return BaselineBackend()
