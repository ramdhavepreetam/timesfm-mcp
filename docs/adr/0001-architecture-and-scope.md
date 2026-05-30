# ADR 0001 — Architecture and Scope

**Status:** Accepted · **Date:** 2026-05-29

## Context
We want an open-source tool that gives any MCP-compatible AI agent (Claude Code,
Claude Desktop, Cursor, VS Code) the ability to forecast time series, powered by
Google's TimesFM 2.5 foundation model. The goal is fast adoption in the developer
community, which later funnels into a hosted API and consulting.

## Decisions

1. **Transport: MCP via FastMCP (3.x).** FastMCP is the de-facto standard and
   powers the majority of MCP servers; decorator-based tools keep boilerplate low.
   Default transport is stdio (for local agents); HTTP is available for hosting.

2. **Distribution: `uvx`-runnable, zero-config.** Adoption dies on setup friction.
   A user must be able to add one line to their agent config and have it work.

3. **The agent is the LLM.** The server returns *numbers + a compact context
   summary* (trend, seasonality, volatility). The calling agent writes the
   natural-language explanation and recommendation. We do **not** bundle an LLM in
   the core. This keeps dependencies light, which is what lets the tool spread.

4. **Two backends behind one interface.** A pure-NumPy `BaselineBackend` runs
   instantly with no heavy deps; the `TimesFMBackend` (optional `timesfm` extra) is
   loaded lazily. The server auto-selects TimesFM when present, else the baseline.
   The tool always returns something useful.

5. **Local Ollama LLM = optional offline mode, not core.** A small local model is
   only useful when there is *no* agent in the loop (e.g. CLI use). Deferred to a
   later phase as an opt-in `explain` tool.

## Consequences
- Anyone can try the server in ~30 seconds; the foundation model is a power-up,
  not a prerequisite.
- TimesFM 2.5's inference API differs from 1.x/2.0, so `TimesFMBackend` ships as a
  stub that delegates to the baseline until wired in Phase 2.
- The same forecasting core is reusable inside a future Shopify app (idea A).
