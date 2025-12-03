# SMARD Data Index Metadata  
**Source:** https://www.smard.de/en  
**Scope:** Indexing and catalog files for SMARD time series data

## Description
This directory contains index files providing:
- Available dataset categories (electricity generation, consumption, market prices, grid)**  
- Mapping between SMARD identifiers and specific time series  
- Endpoint references to download data for selected regions, technologies or markets

These index files are fundamental for programmatically discovering and retrieving data from SMARD.

## Data characteristics
- Contains metadata only — no numeric time series values
- Underlying time series cover Germany and market zones (e.g. DE, LU bidding zone)
- Time resolution depends on category (typically 15-minute or hourly)

## Use in project
Used for:
- Querying available datasets
- Constructing SMARD API URLs
- Filtering to relevant sources (e.g. Germany only)

## Licensing
SMARD data is publicly accessible; check SMARD terms for redistribution requirements.
