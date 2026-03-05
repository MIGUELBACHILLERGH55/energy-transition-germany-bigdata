<p align="center">
  <img src="assets/logo.png" width="900">
</p>

<p align="center">
  Germany Energy Transition — Data Engineering Pipeline
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue">
  <img src="https://img.shields.io/badge/Apache_Spark-ETL-orange">
  <img src="https://img.shields.io/badge/Architecture-Lakehouse-green">
</p>

---

## Overview

This project analyzes the German energy transition using official public datasets.

A complete **ETL pipeline with Apache Spark** was implemented to transform heterogeneous energy data into structured analytical datasets suitable for analysis and business intelligence.

The system follows a **lakehouse architecture**, ensuring reproducibility, traceability and a clear separation between raw data, transformations and analytical outputs.

The resulting datasets enable the exploration of:

- the evolution of Germany’s energy mix
- renewable expansion by technology
- electricity market price dynamics
- nuclear phase-out context
- energy consumption by sector

---

## Architecture

The project follows a lakehouse architecture separating raw ingestion, transformation and analytical layers.

```mermaid
flowchart LR
A[Landing<br>Raw Sources] --> B[Bronze<br>Raw Parquet]
B --> C[Silver<br>Clean & Structured]
C --> D[Gold<br>Analytical Datasets]
D --> E[Analysis & BI]
```

---

## Data Sources

| Source   | Type | Content                                                 |
| -------- | ---- | ------------------------------------------------------- |
| SMARD    | API  | German electricity generation, demand and market prices |
| AGEB     | File | German energy balances and structural indicators        |
| Eurostat | File | European energy price indicators                        |
| OPSD     | File | Historical electricity generation and demand            |
| EEA      | File | National greenhouse gas emissions                       |

All sources are official European or German institutions, ensuring data reliability and traceability.

---

## Project Structure

```
data/
├── landing/          # Raw data from sources
├── bronze/           # Raw datasets materialized in Parquet
├── silver/           # Cleaned and normalized datasets
└── gold/             # Analytical datasets ready for analysis
```

---

## Analytical Datasets (Gold Layer)

| Dataset                            | Source           | Frequency       | Description                                          |
| ---------------------------------- | ---------------- | --------------- | ---------------------------------------------------- |
| energy_mix_total                   | AGEB             | Annual          | Total German energy mix and relative share by source |
| energy_intensity_indicators        | AGEB             | Annual          | Aggregated energy efficiency indicators              |
| final_energy_consumption_by_sector | AGEB             | Annual          | Final energy consumption by sector                   |
| renewables_by_technology           | AGEB             | Annual          | Renewable production by technology                   |
| daily_electricity_profile          | OPSD             | Daily           | Electricity load and renewable share                 |
| latest_energy_day                  | SMARD            | Hourly snapshot | Latest full day of electricity system data           |
| electricity_price_trends_monthly   | SMARD / Eurostat | Monthly         | Electricity price trends                             |
| nuclear_exit_context_monthly       | SMARD            | Monthly         | Nuclear phase-out context                            |

All datasets are stored in **long format with consistent temporal typing and explicit units**.

---

## Analytical Insights

### Energy Mix Evolution

![Energy mix](assets/graphs/energy_mix.jpg)

Renewables have steadily expanded since the early 2000s, progressively replacing coal and nuclear generation in Germany’s energy system.

---

### Electricity Market Prices

![Electricity prices](assets/graphs/electricity_price.jpg)

Electricity prices remained relatively stable for many years before experiencing strong volatility during the European energy crisis.

---

### Renewable Generation by Technology

![Renewables by technology](assets/graphs/renewables_tech.jpg)

Wind power dominates renewable electricity generation, followed by biomass and solar, illustrating the technological composition of Germany’s renewable expansion.

---

## Reproducibility

The entire ETL pipeline can be reproduced using the provided **Makefile**.

Example workflow:

```
make bronze
make silver
make gold
```

To rebuild the entire pipeline:

```
make refresh-all
```

---

## Authors

|                                                                |                                                                     |
| :------------------------------------------------------------: | :-----------------------------------------------------------------: |
| <img src="https://github.com/Tomasmoralessp.png" width="140"/> | <img src="https://github.com/MIGUELBACHILLERGH55.png" width="140"/> |
|                    **Tomás Morales Galván**                    |                    **Miguel Bachiller Segovia**                     |
|      [@Tomasmoralessp](https://github.com/Tomasmoralessp)      |   [@MIGUELBACHILLERGH55](https://github.com/MIGUELBACHILLERGH55)    |
