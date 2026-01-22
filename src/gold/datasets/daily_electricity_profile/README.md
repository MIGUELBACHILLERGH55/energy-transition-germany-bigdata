# daily_electricity_metrics

## Description

Daily electricity demand and renewable generation metrics in long format.

This dataset provides a normalized, BI-friendly daily view of electricity demand,
renewable generation, and renewable penetration indicators. Each observation
represents a single metric–value pair with an explicit unit, enabling flexible
visualization and comparison in BI tools such as Power BI.

## Sources

- OPSD (Open Power System Data)
  - Dataset: `timeseries_hourly`
  - Original frequency: hourly
  - Aggregation: daily (sum for energy, ratio for shares)

## Purpose

- Analyze daily electricity demand trends
- Study renewable generation patterns (solar, wind, total renewables)
- Track renewable penetration over time
- Enable flexible, metric-driven BI dashboards
- Support seasonal and calendar-based analysis

## Data Model

The dataset follows a **long (tidy) format**, where each row represents one metric
for one day.

This design:
- simplifies Power BI modeling
- avoids duplicated measures
- allows scalable addition of new metrics without schema changes

## Units

- **MWh** — daily energy totals (demand and generation)
- **ratio** — renewable shares expressed as values between 0 and 1  
  (can be formatted as percentages in BI tools)

## Visualizations

- Daily time series by metric
- Energy vs renewable share dual-axis charts
- Seasonal patterns by month
- Renewable penetration trends
- Weekday vs weekend comparisons
- Metric-driven dashboards using slicers

## Columns

| Column        | Description |
|--------------|-------------|
| date         | Calendar date |
| year         | Year |
| month        | Month number (1–12) |
| month_name   | Month name |
| day_of_week  | Day of week name |
| is_weekend   | Weekend indicator (true/false) |
| metric       | Metric name (e.g. load, solar, wind, renewables, shares) |
| value        | Metric value |
| unit         | Unit of measurement (MWh or ratio) |
| dataset      | Gold dataset name (`daily_electricity_metrics`) |

