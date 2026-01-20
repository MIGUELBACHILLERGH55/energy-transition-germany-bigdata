from pyspark.sql import DataFrame


def melt_df(df: DataFrame) -> DataFrame:
    years = [c for c in df.columns if c.isdigit()]

    return df.melt(
        ids=["dimension", "unit"],
        values=years,
        variableColumnName="year",
        valueColumnName="value",
    )
