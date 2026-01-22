# latest_energy_day

## Description

Latest available hourly electricity load and market price for Germany,
covering the most recent complete day.

This dataset provides a concise, BI-friendly snapshot of the electricity
system state for the latest full day, with hourly resolution. It includes
both electricity load and wholesale market price, modeled in long format
with explicit units.

Each row represents one metric observation for one hour.

## Sources

- SMARD (Bundesnetzagentur)
  - Electricity load (hourly)
  - Market price DE/LU (hourly)

## Purpose

- Monitor the current state of the electricity system
- Analyze intraday load and price patterns
- Study the relationship between demand and price
- Support operational and near-real-time dashboards
- Enable daily volatility and peak/off-peak analysis

## Data Model

The dataset follows a **long (tidy) format**, where:
- one row = one metric
- each metric has a single, explicit unit
- all observations belong to the same (latest) full day

This structure is optimized for BI tools such as Power BI.

## Units

- **MW** — electricity load
- **EUR/MWh** — wholesale electricity market price

## Visualizations

- Hourly line charts (load and price)
- Dual-axis charts (MW vs EUR/MWh)
- Intraday volatility analysis
- Peak vs off-peak comparisons
- Daily system state dashboards

## Columns

| Column     | Description |
|------------|-------------|
| timestamp  | Hourly timestamp |
| run_date   | Pipeline execution date |
| metric     | Metric type (`load` or `price`) |
| value      | Metric value |
| unit       | Measurement unit (`MW` or `EUR/MWh`) |
| dataset    | Gold dataset name (`latest_energy_day`) |

## Notes

- The dataset always contains exactly 24 hourly observations per metric.
- Only the most recent complete day is included.
