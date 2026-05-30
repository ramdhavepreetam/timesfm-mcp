# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
