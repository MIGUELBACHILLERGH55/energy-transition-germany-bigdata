# nuclear_exit_context_monthly

## Description

Contextual dataset capturing the phase-out of nuclear energy in Germany
and its impact on the electricity generation mix.

Provides a clean monthly time series of nuclear electricity generation,
explicitly labeled for pre- and post-nuclear-exit analysis.

## Sources

- SMARD (Statistisches Marktstammdatenregister)
  - Nuclear electricity generation
  - Original resolution: daily
  - Aggregated to: monthly

## Purpose

- Track the decline and final exit of nuclear electricity generation
- Support before / after comparisons (pre-2022 vs post-2023)
- Provide policy-relevant context for energy transition analysis
- Enable comparison with electricity prices and generation mix datasets

## Visualizations

- Nuclear generation time series
- Before–after nuclear exit comparisons
- Overlay with electricity price trends
- Event markers (nuclear shutdown milestones)

## Columns

| Column            | Description                          |
|------------------|--------------------------------------|
| date             | Month reference date                 |
| year             | Year                                 |
| technology       | Generation technology (`nuclear`)    |
| generation_value | Monthly electricity generation       |
| unit             | MWh                                  |
| period           | `pre_exit` / `post_exit`             |
| dataset          | Gold dataset name                    |
