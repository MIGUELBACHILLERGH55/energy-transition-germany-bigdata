# energy_intensity_indicators

## Description

Energy efficiency and intensity indicators for Germany over time.

This dataset provides a curated set of energy intensity and efficiency indicators,
designed to analyze how energy consumption evolves relative to economic activity
and sectoral output. Indicators are modeled in a BI-friendly format with explicit
units and rich semantic metadata.

Each row represents a single indicator observation for a given year.

## Sources

- AGEB (Arbeitsgemeinschaft Energiebilanzen)
  - Table: 7.1
  - Frequency: yearly

## Purpose

- Measure long-term energy efficiency and intensity trends
- Analyze energy–economy decoupling
- Compare efficiency developments across sectors
- Support macro-level energy transition analysis

## Data Model

The dataset follows a **long, indicator-based format**, where:
- one row corresponds to one indicator and one year
- the indicator definition is separated into code, label, group, and scope

This structure:
- simplifies Power BI modeling
- enables flexible slicing and filtering
- avoids duplicated measures
- keeps units explicit and unambiguous

## Units

Units depend on the indicator and are provided explicitly in the dataset, e.g.:
- **MJ/100Pkm** — energy intensity in transport
- **GJ/1000 €** — energy intensity relative to economic output

Units should be interpreted directly on the visualization axis.

## Visualizations

- Line charts for energy intensity indicators over time
- Sectoral comparisons of efficiency trends
- Economy-wide vs sector-specific indicators
- Indicator dashboards with hierarchical slicers (scope → group → indicator)

## Columns

| Column             | Description |
|--------------------|-------------|
| year               | Reference year |
| indicator_scope    | High-level scope of the indicator (e.g. Economy-wide, Transport) |
| indicator_group    | Sector or thematic group (e.g. Final energy, Transport) |
| indicator_code     | Stable technical indicator identifier |
| indicator_label    | Human-readable indicator name |
| value              | Indicator value |
| unit               | Measurement unit (e.g. MJ/100Pkm, GJ/1000 €) |
| dataset            | Gold dataset name (`energy_intensity_indicators`) |


