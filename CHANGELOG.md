# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-30
### Added
- Initial release of `forecast-mcp`.
- Statistical `BaselineBackend` with seasonal-naive and linear trend forecasting.
- Support for `TimesFMBackend` wrapping Google's TimesFM 2.5 foundation model (requires `timesfm` extra).
- `forecast` tool to predict future values with uncertainty bands.
- `list_backends` tool to check which backend is active.
- `backtest` tool to compare Baseline and TimesFM backends using holdout sets and sMAPE calculation.
