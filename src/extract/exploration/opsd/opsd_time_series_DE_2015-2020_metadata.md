# Open Power System Data – Time series (electricity load, generation and prices)  
**Version:** 2020-10-06 (latest)  
**DOI:** https://doi.org/10.25832/time_series/2020-10-06  

## Description
Time series data package for power system modelling, including electricity prices, electricity consumption (load), and wind and solar power generation and capacities.  
Data is aggregated by country, control area, or bidding zone. Geographical coverage: 32 European countries (EU and neighbouring countries).  
All variables are provided with hourly resolution; where original data is at higher resolution (15 or 30 minutes), separate files are provided.  
This version includes only data provided by TSOs and power exchanges via ENTSO-E Transparency and covers the period 2015–mid 2020. :contentReference[oaicite:0]{index=0}  

## Variables (high level)
- **Demand / load:** total load and day-ahead load forecasts (MW)  
- **Prices:** day-ahead spot prices (EUR or GBP, depending on bidding zone)  
- **Generation:** actual wind and solar generation (MW), including onshore/offshore where available  
- **Capacities & profiles:** installed capacities (MW) and generation profiles (capacity factors) for wind and solar in selected countries  

## Temporal coverage
Approx. **2015 – mid 2020**, hourly (plus separate 15-min and 30-min datasets). :contentReference[oaicite:1]{index=1}  

## Geographic coverage
32 European countries, including Germany, Austria, Belgium, Denmark, Spain, France, Italy, Netherlands, Nordic countries, UK, etc. :contentReference[oaicite:2]{index=2}  

## File formats & resources
- **Data package (zip):** `opsd-time_series-2020-10-06.zip`  
- **Tabular data:**  
  - `time_series_60min_singleindex.csv`  
  - `time_series_30min_singleindex.csv`  
  - `time_series_15min_singleindex.csv`  
  - `time_series.xlsx`  
- **Database:** `time_series.sqlite`  
- **Metadata:** `README.md`, `datapackage.json`  
- **Original input data:** separate archive / directory with raw ENTSO-E and other source files. :contentReference[oaicite:3]{index=3}  

## Processing & methodology
- Data collected from ENTSO-E Transparency and other official sources.  
- Processing, cleaning, aggregation and documentation implemented in Python/pandas.  
- Full methodology and script available as a Jupyter notebook on GitHub / nbviewer (linked from the package page). :contentReference[oaicite:4]{index=4}  

## License & attribution
- **Text:** licensed under a Creative Commons Attribution (CC-BY) license.  
- **Data:** republished by Open Power System Data; primary data originates from ENTSO-E Transparency and other providers (check original sources for detailed terms). :contentReference[oaicite:5]{index=5}  
- Recommended citation (Chicago author-date style, paraphrased):  
  > Open Power System Data. 2020. *Data Package Time Series*, version 2020-10-06. https://doi.org/10.25832/time_series/2020-10-06. Primary data from various sources (see URL for full list). :contentReference[oaicite:6]{index=6}  

## Publisher / contact
- **Platform:** Open Power System Data (OPSD)  
- **Website:** https://open-power-system-data.org/  
- **Project focus:** Open, well-documented datasets for electricity system modelling in Europe. :contentReference[oaicite:7]{index=7}  

## URL
Main data package page:  
https://data.open-power-system-data.org/time_series/2020-10-06  

## Project-specific note
For this project, only the **Germany-related columns** (e.g. `DE_*`, `DE_50hertz_*`, `DE_LU_*`, `DE_tennet_*`, `DE_amprion_*`, `DE_transnetbw_*`) have been downloaded and used.
