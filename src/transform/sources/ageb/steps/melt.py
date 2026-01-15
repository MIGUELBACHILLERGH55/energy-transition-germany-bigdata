def melt_df(df):
    years = [
        col
        for col in df.columns
        if col.isdigit() and col not in ("energy_source", "unit", "indicator")
    ]

    if "energy_source" in df.columns:
        df = df.melt(
            ids=["energy_source", "unit"],
            values=years,
            variableColumnName="year",
            valueColumnName="value",
        )

    elif "indicator" in df.columns:
        df = df.melt(
            ids=["indicator", "unit"],
            values=years,
            variableColumnName="year",
            valueColumnName="value",
        )

    return df
