# Vendored: Google TimesFM 2.5

This directory contains a vendored copy of the TimesFM 2.5 Python source,
originally from https://github.com/google-research/timesfm.

**License:** Apache-2.0  
**Copyright:** 2025 Google LLC  
**Vendored because:** TimesFM 2.5 is not published to PyPI (tracked in
https://github.com/google-research/timesfm/issues/432). When Google publishes
2.5 to PyPI, this directory will be removed and replaced with a real dependency.

The vendored source is used only when the user has not installed their own
`timesfm` package. If `import timesfm` succeeds with a 2.5-compatible version,
the vendored copy is ignored.
