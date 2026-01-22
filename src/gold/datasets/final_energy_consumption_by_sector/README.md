# final_energy_consumption_by_sector

## Description

Final energy consumption broken down by **economic sector** and **energy source** over time.

Each record represents the total final energy consumption for a given:
- year
- economic sector
- energy source

Values are expressed in petajoules (PJ).

## Sources 

- AGEB
  - Tables: 6.1, 6.2, 6.3, 6.4, 6.6
  - Unit: PJ

### Sector mapping

| Table | Sector |
|------:|--------|
| 6.1 | Total economy |
| 6.2 | Industry (Mining & Manufacturing) |
| 6.3 | Private households |
| 6.4 | Trade, commerce and services (TCS) |
| 6.6 | Transport |

## Purpose

- Analyze how final energy consumption is distributed across sectors
- Compare sectoral energy consumption patterns over time
- Support sector-level energy transition analysis
- Serve as a base dataset for share and mix calculations

## Visualizations 

- Stacked area charts by sector and energy source
- Line charts comparing sectoral consumption over time
- Bar charts for cross-sector comparison by year

## Columns

| Column | Description |
|-------|-------------|
| year | Calendar year |
| sector | Economic sector |
| energy_source | Energy source (e.g. electricity, gas, renewables) |
| value | Final energy consumption |
| unit | Measurement unit (PJ) |
| table_id | Original AGEB table identifier |
| dataset | Gold dataset identifier |


