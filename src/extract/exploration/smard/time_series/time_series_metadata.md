# SMARD Time Series Metadata  
**Source:** https://www.smard.de/en  
**Scope:** German electricity system operational data (bidding zone: DE-LU)

## Description
Time series data retrieved from the SMARD platform. This dataset includes:
- Electricity generation by technology (coal, gas, nuclear, wind, solar, biomass…)
- Electricity consumption (total and industrial load where available)
- Market clearing prices (day-ahead, intraday)
- Cross-border flows (depends on selected data)
- Data provided in 15-minute or hourly resolution

## Temporal coverage
Historical data available from ~2015 onward
(Exact start depends on each variable/category)

## Geographic coverage
Germany (DE-LU bidding zone)  
Some categories may include control areas if requested

## File format / Structure
- JSON payloads converted to CSV in project code
- `utc_timestamp` as primary time index
- All numeric values in MW or €/MWh (prices)

## Processing notes
- Data retrieved via SMARD public API
- Cleaning and transformation performed in project code (`helpers.py`)
- Conversions to consistent UTC time base ensured

## License / Attribution
Data © SMARD / Bundesnetzagentur  
Publicly accessible for research and non-commercial use; check conditions for redistribution.
