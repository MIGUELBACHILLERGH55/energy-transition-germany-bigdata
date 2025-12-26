from pyspark.sql import DataFrame
from pyspark.sql import functions as sf
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline

from src.transform.core.steps.base_step import (
    rename_cols,
)
from src.transform.sources.opsd.steps import show_nulls_month_hour_count


# TODO: refactor this using the new helpers
class OpsdTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame, verbose=True) -> DataFrame:
        # Cols naming map
        cols_map = {
            "utc_timestamp": "utc_timestamp",
            "cet_cest_timestamp": "cet_cest_timestamp",
            "DE_load_actual_entsoe_transparency": "load_act",
            "DE_load_forecast_entsoe_transparency": "load_for",
            "DE_solar_capacity": "solar_cap",
            "DE_solar_generation_actual": "solar_gen",
            "DE_wind_capacity": "wind_cap",
            "DE_wind_generation_actual": "wind_gen",
        }

        if verbose:
            print("1. Raw dataframe:")
            df.show(n=5, truncate=False)

        df = rename_cols(df, cols_map)

        if verbose:
            print("2. Change the columns names: ")
            df.show(n=5, truncate=False)

        # Normalize event time: cast raw UTC timestamp, derive date, and drop raw column
        df = (
            df.withColumn("event_ts_utc", sf.col("utc_timestamp").cast("timestamp"))
            .withColumn("event_date_utc", sf.to_date("event_ts_utc"))
            .drop("utc_timestamp")
        )

        if verbose:
            print(
                "3. Normalize event time: cast raw UTC timestamp, derive date, and drop raw column"
            )
            df.select(
                "event_date_utc",
                sf.date_format("event_ts_utc", "HH:mm:ss").alias("events_ts"),
                *[c for c in df.columns if c not in {"event_date_utc", "event_ts_utc"}],
            ).show(truncate=False)

        if verbose:
            print("4. Are there any nulls? Where?")
            show_nulls_month_hour_count(df, "solar_gen")

        # if verbose:
        #     print("5. Handle solar generation null values")
        #
        # if verbose:
        #     print("Transformed DataFrame")
        #     df.select(
        #         "event_date_utc",
        #         sf.date_format("event_ts_utc", "HH:mm:ss").alias("events_ts"),
        #         *[c for c in df.columns if c not in {"event_date_utc", "event_ts_utc"}],
        #     ).show(n=50, truncate=False)

        return df
