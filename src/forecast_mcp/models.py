"""Typed request/response models shared across backends and the MCP layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ForecastPoint(BaseModel):
    step: int = Field(..., description="Steps ahead from the end of the input series (1-indexed).")
    value: float = Field(..., description="Point (median) forecast for this step.")
    lower: float | None = Field(None, description="Lower quantile bound, if requested.")
    upper: float | None = Field(None, description="Upper quantile bound, if requested.")


class SeriesContext(BaseModel):
    """Compact, machine-readable summary the calling agent uses to write its own explanation."""

    n_observations: int
    detected_season_length: int = Field(..., description="1 means no seasonality detected.")
    trend: str = Field(..., description="One of: rising, falling, flat.")
    trend_pct_per_step: float = Field(..., description="Approx. percent change per step from the fitted trend.")
    last_value: float
    mean: float
    volatility: float = Field(..., description="Std of recent residuals; higher = wider, less certain bands.")


class ForecastResult(BaseModel):
    backend: str = Field(..., description="Which engine produced this: 'timesfm' or 'baseline'.")
    horizon: int
    points: list[ForecastPoint]
    context: SeriesContext
    notes: list[str] = Field(default_factory=list)
