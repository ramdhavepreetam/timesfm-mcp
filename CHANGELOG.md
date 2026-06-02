# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] - 2026-06-01
### Fixed
- `list_backends` no longer shows the "install extra" hint when TimesFM is already active — hint now only appears when the baseline is running.
- `backtest` renamed internal variable `timesfm` → `tfm_backend` to avoid shadowing the module name.
- Removed redundant inline comment and trailing whitespace from `TimesFMBackend.forecast()`.

### Changed
- System requirements made explicit and prominent across all docs:
  - README: two-tier requirements table (baseline = any machine; TimesFM = ≥16 GB RAM + ~800 MB disk) with "Start with the baseline" recommendation.
  - `getting-started.md`: requirements table at the top of the page; warning callout before TimesFM install tab.
  - `limitations.md`: blockquote requirement notice at the top of the TimesFM section.
  - `client-setup.md`: warning callout with explicit RAM/disk figures before TimesFM config.
- Baseline consistently described as "recommended for most users / production-ready on any hardware."
- `list_backends` hint includes RAM requirement so agents can surface it to users.

## [0.1.5] - 2026-06-01
### Added
- TimesFM 2.5 Python source vendored inside the package (`timesfm_mcp/_timesfm/`, Apache-2.0, Google LLC). `pip install "timesfm-mcp[timesfm]"` now works without a separate git clone. The `[timesfm]` extra pulls in `torch`, `huggingface_hub`, and `safetensors`; model weights (~800 MB) still download from HuggingFace on first use.
- `_load_timesfm_module()` helper: tries the user's own `timesfm` install first (if it has the 2.5 API), then falls back to the vendored copy. User installs always take priority.
- `VENDOR.md` attribution file documenting the vendored source and linking to the upstream PyPI issue (google-research/timesfm#432).

### Changed
- All docs updated: `pip install "timesfm-mcp[timesfm]"` is the one-liner again everywhere (README, getting-started, client-setup, self-hosting, tool-reference, how-it-works, limitations).
- `select_backend()` simplified — delegates availability check to `_load_timesfm_module()`.

### Notes
- Vendoring is a temporary measure. When Google publishes TimesFM 2.5 to PyPI (tracked in https://github.com/google-research/timesfm/issues/432), `_timesfm/` will be removed and replaced with a real `timesfm>=2.5` dependency.

## [0.1.4] - 2026-06-01
### Fixed
- Removed unresolvable `timesfm>=2.5` PyPI dependency from `pyproject.toml` — TimesFM 2.5 is not on PyPI and the constraint could never be satisfied. The `[timesfm]` extra is gone; install instructions now point to the Google Research GitHub source.
- Corrected RAM requirement for TimesFM from ~2 GB / ~4 GB to ~16 GB (per upstream repo recommendation) across `limitations.md`, `getting-started.md`, `client-setup.md`, `self-hosting.md`, and `how-it-works.md`.
- All `pip install "timesfm-mcp[timesfm]"` references replaced with the correct from-source install path throughout docs, examples, and the `list_backends` hint returned by the server at runtime.
- Docker "With TimesFM" example now clones and installs from source instead of using the PyPI extra.

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
