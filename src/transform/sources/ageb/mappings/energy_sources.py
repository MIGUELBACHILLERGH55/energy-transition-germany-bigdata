ENERGY_SOURCE_MAP = {
    "Hard coal": "hard_coal",
    "Lignite": "lignite",
    "Petroleum": "petroleum",
    "Gases": "gases",
    "Natural gas, Petroleum gas": "natural_gas",
    "Renewable Energy Sources": "renewables",
    "Other energy sources": "other_sources",
    "Electricity": "electricity",
    "District heat": "district_heat",
    "Nuclear energy": "nuclear",
    "Net import of electricity": "net_import_electricity",
}

STRUCTURE_ENERGY_CONS_MAP = {
    "Indigenous energy production": "indigenous_energy_production",
    "Primary energy consumption": "primary_energy_consumption",
    "Transformation input": "transformation_input",
    "Transformation output": "transformation_output",
    "Cons., losses in energy sector": "energy_sector_losses",
    "Non-energy consumption": "non_energy_consumption",
    "Final energy consumption": "final_energy_consumption",
    "Mining, quarrying, manufact.": "mining_quarrying_manufacturing",
    "Transport": "transport",
    "Private households": "private_households",
    "Services": "services",
}

RENEWABLE_TYPE_MAP = {
    "Hydropower": "hydropower",
    "Wind energy": "wind",
    "Photovoltaics": "solar_pv",
    "Solarthermal energy": "solar_thermal",
    "Geothermal energy": "geothermal",
    "Ambient heat": "ambient_heat",
    "Biomass": "biomass",
    "Renewable waste": "renewable_waste",
    "Liquid Biofuels": "liquid_biofuels",
}

TRANSPORT_FEC_MAP = {
    "Rail transport": "rail",
    "Road transport": "road",
    "Aviation transport": "aviation",
    "Coastal and inland shipping": "shipping",
    "Jet fuel / kerosene": "jet_fuel_kerosene",
    "Diesel oil": "diesel_oil",
    "Electricity": "electricity",
}


EFFICIENCY_INDICATOR_MAP = {
    "PEC / residents": "pec_per_resident",
    "PEC / GDP": "pec_per_gdp",
    "FEC / residents": "fec_per_resident",
    "FEC / GDP": "fec_per_gdp",
    "FEC Industry / GPV": "fec_industry_per_gpv",
    "FEC TCS / GVA": "fec_tcs_per_gva",
    "FEC Households / residents": "fec_households_per_resident",
    "FEC Households / Living space": "fec_households_per_living_space",
    "FEC Transport / GDP": "fec_transport_per_gdp",
    "FEC Transport / Transport perf.": "fec_transport_per_transport_performance",
}


CHP_5_1_TWH_METRIC_MAP = {
    "Power plant own use (EB)": "power_plant_own_use",
    "CHP net electr. generation": "chp_net_electricity_generation",
    "CHP net heat generation": "chp_net_heat_generation",
}


CHP_5_1_PJ_METRIC_MAP = {
    "Transformation input electr. (EB)": "transformation_input_electricity",
    "Transformation input CHP electr.": "transformation_input_chp_electricity",
    "Transformation input CHP heat": "transformation_input_chp_heat",
}
