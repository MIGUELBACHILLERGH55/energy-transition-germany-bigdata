## electricity_price_trends_monthly

## Description

Monthly evolution of electricity price-related indicators in Germany, combining
wholesale electricity market prices with consumer energy price indices.

This dataset provides economic and policy context for the German energy transition,
with a focus on long-term trends, price transmission mechanisms, and the
2021–2023 energy crisis.

It is designed specifically for visualization and BI tools (e.g. Power BI),
offering a clean, monthly, and comparable time series structure.

## Sources

### SMARD
- Indicator: Electricity market price (Germany / DE-LU)
- Original resolution: hourly
- Aggregated to: monthly average
- Unit: EUR/MWh

### Eurostat
- Indicator: Harmonized Index of Consumer Prices (HICP) – Energy
- Frequency: monthly
- Base year: 2015 = 100
- Unit: index (2015 = 100)

## Purpose

- Analyze long-term electricity price trends in Germany
- Contextualize the 2021–2023 energy crisis
- Compare wholesale market price dynamics with consumer price evolution
- Study price transmission, lag effects, and shock absorption
- Provide a BI-ready dataset for dashboards and storytelling

## Transformations

- Hourly SMARD prices aggregated to monthly averages
- Eurostat monthly indices aligned to calendar months
- Unified monthly time axis across sources
- Explicit separation of price semantics via price_type and unit
- Removal of mixed granularities to ensure BI compatibility

## Visualizations

- Monthly time series of electricity market prices
- Monthly consumer energy price index trends
- Normalized trend comparison (base 100)
- Pre- vs post-2021 crisis analysis
- Volatility (market) vs stability (consumer) comparison

## Columns

| Column        | Description |
|--------------|------------|
| date         | Reference month (YYYY-MM-01) |
| year         | Calendar year |
| price_value  | Monthly average price or index value |
| price_type   | market_price / consumer_price_index |
| unit         | EUR/MWh or index (2015 = 100) |
| source       | SMARD / Eurostat |
| resolution   | Fixed value: month |
