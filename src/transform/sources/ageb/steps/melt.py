from pyspark.sql import DataFrame


def melt_df(df: DataFrame, value_col: str) -> DataFrame:
    years = [c for c in df.columns if c.isdigit()]

    return df.melt(
        ids=[value_col, "unit"],
        values=years,
        variableColumnName="year",
        valueColumnName="value",
    )
