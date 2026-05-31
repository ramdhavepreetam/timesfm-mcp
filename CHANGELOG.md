# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-05-30
### Fixed
- `select_backend()` now checks for `timesfm.TimesFM_2p5_200M_torch` presence rather than a bare `import timesfm`, so the baseline fallback works correctly when PyTorch is absent.
- `ForecastConfig` corrected to `max_context=1024, max_horizon=256` (was 16384/1000 which exceeded the model's total context limit and raised `ValueError` on every call).
- Context truncation guard updated to match: histories > 1,024 points are now truncated correctly.
- All remaining `forecast-mcp` references renamed to `timesfm-mcp` across docs, examples, and `mcp.json`.

### Changed
- TimesFM 2.5 backend verified end-to-end with PyTorch. Documentation updated to reflect that TimesFM is production-ready (not experimental) when installed.
- Context cap in docs corrected from 16,384 to 1,024 points.
- PyTorch install size corrected to ~84 MB (not ~2 GB).

## [0.1.2] - 2026-05-30
### Fixed
- Replaced all `github.io` documentation links with direct `github.com` repo links (GitHub Pages was not activated).
- Added `Documentation` URL to `pyproject.toml` pointing to `docs/` folder on GitHub.

## [0.1.1] - 2026-05-29
### Fixed
- Corrected GitHub URLs in `pyproject.toml` (`preetam` → `ramdhavepreetam`).
- Fixed CI badge URL in `README.md`.
- Excluded `timesfm-master/`, `timesfm.zip`, and development artifacts from the sdist; wheel is now ~12 kB and sdist is lean.

### Added
- MkDocs Material documentation site with full coverage (getting started, client setup, tool reference, cookbook, how-it-works, limitations, self-hosting).
- GitHub Actions workflow to build and deploy docs to GitHub Pages on push to `main`.
- Four cookbook example scenarios (`examples/cookbook/`) with realistic sample data and exact agent prompts.
- `examples/python_quickstart.py` for direct library usage without an agent.
- Forecast chart PNG embedded in README for quick visual orientation.
- `docs` optional dependency group (`mkdocs`, `mkdocs-material`).

## [0.1.0] - 2026-05-30
### Added
- Initial release of `timesfm-mcp`.
- Statistical `BaselineBackend` with seasonal-naive and linear trend forecasting.
- Support for `TimesFMBackend` wrapping Google's TimesFM 2.5 foundation model (requires `timesfm` extra).
- `forecast` tool to predict future values with uncertainty bands.
- `list_backends` tool to check which backend is active.
- `backtest` tool to compare Baseline and TimesFM backends using holdout sets and sMAPE calculation.
