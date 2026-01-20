from typing import Mapping, Sequence
from pyspark.sql import DataFrame
from pyspark.sql import functions as sf
from src.transform.core.steps.base_step import remove_cols, rename_cols
from src.transform.sources.ageb.steps.melt import melt_df


def normalize_and_melt(
    table_id: str,
    df: DataFrame,
    *,
    drop_cols: Sequence[str] = (),
    value_col: str,
    replace_map: dict[str, str],
    filter_total: bool = True,
    verbose: bool = True,
) -> DataFrame:
    if drop_cols:
        df = remove_cols(df, list(drop_cols))
        if verbose:
            print("1. Dropped columns:", drop_cols)

    if value_col == "energy_source":
        df = rename_cols(df, {"Energy source": "dimension", "Units": "units"})
    elif value_col == "indicator":
        df = rename_cols(df, {"Indicator": "dimension", "Units": "units"})

    if verbose:
        print("2. Renamed columns.")

    if filter_total:
        df = df.filter(~df["dimension"].contains("Total"))
        if verbose:
            print("3. Filtered aggregation rows.")

    if replace_map:
        df = df.replace(to_replace=replace_map, subset=["dimension"])
        if verbose:
            print("4. Normalized values using mapping.")

    df = melt_df(df)
    if verbose:
        print("5. Melted dataframe.")

    df = df.withColumn("table_id", sf.lit(table_id))
    if verbose:
        print("6. Added table_id.")

    df = df.filter(sf.col("value").isNotNull())
    df = df.filter(~sf.col("value").isNaN())
    if verbose:
        print("7. Dropping Null & Nan values.")

    if verbose:
        df.show(10)

    return df
