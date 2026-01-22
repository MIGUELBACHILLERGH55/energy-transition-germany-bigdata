# energy_mix_total

## Description

Total energy mix of Germany over time by energy source, provided in long format.

This dataset represents the annual total primary energy supply of Germany,
broken down by energy source. Each observation corresponds to a single
metric–value pair with an explicit unit, enabling consistent analysis and
visualization in BI tools such as Power BI.

Both absolute energy values and relative shares are included in a normalized
(long) structure.

## Sources

- AGEB (Arbeitsgemeinschaft Energiebilanzen)
  - Table: 6.1
  - Original unit: PJ (Petajoules)
  - Frequency: yearly

## Purpose

- Analyze the long-term energy transition in Germany
- Observe structural changes in the energy system
- Compare the evolution of fossil fuels vs renewables
- Enable energy mix analysis in absolute and relative terms

## Data Model

The dataset follows a **long (tidy) format**, where each row represents
one metric for one energy source and year.

This structure:
- supports flexible BI visualizations
- avoids duplicated measures
- ensures consistent handling of units
- scales easily when adding new energy sources or metrics

## Units

- **PJ** — annual total energy supply by source
- **ratio** — share of total annual energy supply (values between 0 and 1)  
  (can be formatted as percentages in BI tools)

## Visualizations

- Stacked area chart of energy sources over time (absolute values)
- Energy mix composition by year
- Share of renewables vs fossil fuels (%)
- Long-term transition trends by energy source

## Columns

| Column     | Description |
|------------|-------------|
| year       | Calendar year |
| dimension  | Energy source (e.g. coal, gas, renewables) |
| metric     | Metric type (`energy` or `share`) |
| value      | Metric value |
| unit       | Unit of measurement (`PJ` or `ratio`) |
| dataset    | Gold dataset name (`energy_mix_total`) |

