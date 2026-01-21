from pyspark.sql import DataFrame
from pyspark.sql import functions as sf
from pyspark.sql.types import DateType, DoubleType
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline
from src.transform.core.steps.base_step import (
    remove_cols,
    change_order_cols,
    strip_prefix_before_delimiter,
    rename_cols,
    add_mapped_column,
)


class EurostatTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame, verbose=False) -> DataFrame:
        # Column rename map
        cols_map = {
            "observation_date": "date",
            "ENRGY0DEM086NEST": "value",
        }

        if verbose:
            print("1. Raw dataframe")
            df.show(n=5, truncate=False)

        # Rename columns
        df = rename_cols(df, cols_map)

        if verbose:
            print("2. Renaming columns")
            df.show(n=5, truncate=False)

        # Explicit typing
        df = df.withColumn("date", sf.col("date").cast(DateType())).withColumn(
            "value", sf.col("value").cast(DoubleType())
        )

        if verbose:
            print("3. Casting columns to proper types")
            df.printSchema()
            df.show(n=5, truncate=False)

        # Optional: sort for deterministic output (safe, no semantics added)
        df = df.sort(sf.col("date"))

        if verbose:
            print("4. Final Silver dataframe")
            df.show(n=20, truncate=False)

        return df
