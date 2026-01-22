# daily_electricity_profile

## Description

Daily aggregated electricity demand and renewable generation profile.

This dataset provides a clean daily view of electricity demand, solar generation,
wind generation, and derived renewable shares, designed for analytical use and BI tools.

## Sources 

- OPSD (Open Power System Data)
  - Dataset: `timeseries_hourly`
  - Frequency: hourly (aggregated to daily)

## Purpose

- Analyze daily electricity demand trends
- Study renewable generation patterns
- Evaluate renewable penetration over time
- Enable seasonal and calendar-based analysis

## Visualizations 

- Daily time series (demand & generation)
- Seasonal patterns by month
- Renewable penetration trends
- Weekday vs weekend comparisons

## Columns

| Column                 | Description |
|------------------------|-------------|
| date                   | Calendar date |
| year                   | Year |
| month                  | Month number (1–12) |
| month_name             | Month name |
| day_of_week            | Day of week name |
| is_weekend             | Weekend indicator (true/false) |
| load_act_daily         | Total daily electricity demand |
| solar_gen_daily        | Total daily solar generation |
| wind_gen_daily         | Total daily wind generation |
| renewables_gen_daily  | Total daily renewable generation (solar + wind) |
| renewables_share      | Renewable generation share of total demand |
| solar_share            | Solar generation share of total demand |
| wind_share             | Wind generation share of total demand |
| dataset                | Gold dataset name |
