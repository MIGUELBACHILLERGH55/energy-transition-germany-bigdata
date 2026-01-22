# final_energy_consumption_by_sector

## Description

Final energy consumption in Germany broken down by **economic sector** and
**energy source**, provided in a normalized long format.

The dataset includes both:
- **absolute final energy consumption** values, and
- **relative shares** of each energy source within a sector and year.

Each row represents a single metric for a given year, sector, and energy source,
with an explicit unit, making the dataset fully BI-friendly.

## Sources

- AGEB (Arbeitsgemeinschaft Energiebilanzen)
  - Tables: 6.1, 6.2, 6.3, 6.4, 6.6
  - Frequency: yearly
  - Original unit: PJ (Petajoules)

### Sector mapping

| AGEB Table | Sector |
|-----------:|--------|
| 6.1 | Total economy |
| 6.2 | Industry (Mining & Manufacturing) |
| 6.3 | Private households |
| 6.4 | Trade, commerce and services (TCS) |
| 6.6 | Transport |

## Purpose

- Analyze how final energy consumption is distributed across sectors
- Compare sectoral energy consumption patterns over time
- Study changes in the energy mix within sectors
- Support sector-level energy transition analysis
- Enable absolute vs relative (share) comparisons in BI tools

## Data Model

The dataset follows a **long (tidy) format**:

- one row = one metric
- metrics are explicitly identified
- units are unambiguous

Two metric types are provided:
- `energy` — absolute final energy consumption
- `share` — share of each energy source within the sector and year

This structure:
- simplifies Power BI modeling
- avoids duplicated measures
- supports scalable addition of new metrics

## Units

- **PJ** — absolute final energy consumption
- **ratio** — share of total sectoral consumption (values between 0 and 1)  
  (can be formatted as percentages in BI tools)

## Visualizations

- Stacked area charts of final energy consumption by sector and energy source
- Sectoral energy mix composition (% share)
- Line charts comparing sectoral consumption over time
- Cross-sector comparisons for a given year

## Columns

| Column | Description |
|--------|-------------|
| year | Calendar year |
| sector | Economic sector (e.g. households, industry, transport) |
| energy_source | Energy source (e.g. electricity, gas, renewables) |
| metric | Metric type (`energy` or `share`) |
| value | Metric value |
| unit | Measurement unit (`PJ` or `ratio`) |
| dataset | Gold dataset name (`final_energy_consumption_by_sector`) |

