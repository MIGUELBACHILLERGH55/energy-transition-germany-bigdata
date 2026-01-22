# renewables_by_technology

## Description

Yearly energy production from renewable sources in Germany, broken down by
**renewable technology** (e.g. wind, solar PV, biomass, hydropower).

Each record represents the total annual renewable energy production for a given
technology and year.

Values are expressed in petajoules (PJ).

## Sources

- **AGEB**
  - Tables: 3.1
  - Unit: PJ

## Purpose

- Analyze the evolution of renewable technologies over time
- Compare growth patterns between renewable sources
- Support renewable transition analysis at technology level
- Serve as a base dataset for technology-level mix and share analysis

## Granularity

- **Temporal**: yearly
- **Geographic**: national (Germany)
- **Technology**: renewable source level

## Columns

| Column      | Description |
|------------|-------------|
| year        | Calendar year |
| technology  | Renewable technology (e.g. wind, solar_pv, biomass) |
| value       | Annual energy production |
| unit        | Measurement unit (PJ) |
| table_id    | Original AGEB table identifier |
| dataset     | Gold dataset identifier |

## Visualizations

- Line charts by renewable technology
- Stacked area charts of renewable production
- Technology growth comparison over time

## Notes

- Dataset is designed to complement energy mix and sectoral consumption datasets
- Shares can be computed downstream if needed (e.g. technology share of total renewables)
