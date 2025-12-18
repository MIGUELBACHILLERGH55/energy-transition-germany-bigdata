from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as sf
from src.transform.core.pipelines.batch_transformer import BatchTransformerPipeline


class OpsdTransformerPipeline(BatchTransformerPipeline):
    def apply_steps(self, ds_name: str, df: DataFrame, verbose=True) -> DataFrame:
        if verbose:
            print("1. Raw dataframe:")
            df.show(n=5, truncate=False)

        cols_mapping = {
            "utc_timestamp": "utc_timestamp",
            "cet_cest_timestamp": "cet_cest_timestamp",
            "DE_load_actual_entsoe_transparency": "load_actual",
            "DE_load_forecast_entsoe_transparency": "load_forecast",
            "DE_solar_capacity": "solar_capacity",
            "DE_solar_generation_actual": "solar_generation_actual",
            "DE_wind_capacity": "wind_capacity",
            "DE_wind_generation_actual": "wind_generation_actual",
        }

        df = df.select(*[sf.col(c).alias(cols_mapping.get(c, c)) for c in df.columns])

        if verbose:
            print("2. Changing the columns names: ")
            df.show(n=5, truncate=False)

        df = (
            df.withColumn("event_ts_utc", sf.col("utc_timestamp").cast("timestamp"))
            .withColumn("event_date_utc", sf.to_date("event_ts_utc"))
            .drop("utc_timestamp")
        )

        if verbose:
            print("3. Showing dataset with event_date and formatted event timestamp")
            df.select(
                "event_date_utc",
                sf.date_format("event_ts_utc", "HH:mm:ss").alias("events_ts"),
                *[c for c in df.columns if c not in {"event_date_utc", "event_ts_utc"}],
            ).show(truncate=False)

        df = df.orderBy("event_ts_utc")

        if verbose:
            print("4. Sorting the dataset by evetn_ts: ")
            df.select(
                "event_date_utc",
                sf.date_format("event_ts_utc", "yyyy-MM-dd HH:mm:ss").alias(
                    "events_ts"
                ),
                *[c for c in df.columns if c not in {"event_date_utc", "event_ts_utc"}],
            ).show(truncate=False)

        if verbose:
            print("5. Are there any nulls? Where?")
            df.select(
                [sf.sum(sf.col(c).isNull().cast("int")).alias(c) for c in df.columns]
            ).show()
            print(
                "Null handling strategy (Silver layer):\n"
                "- Solar generation nulls are assumed to be nighttime values and set to 0.\n"
                "- Wind generation nulls are kept as null (no strong assumption).\n"
                "- Load actual / forecast nulls are kept (very few values).\n"
                "- Capacity columns are left unchanged for now and reviewed later.\n"
                "- No rows are dropped at this stage."
            )

        if verbose:
            print(
                "6. Handling solar_generation_actual nulls:\n"
                "- Assumption: null solar generation values correspond to nighttime hours.\n"
                "- Action: replace nulls with 0 (no row drops).\n"
                "- This transformation is applied only to solar generation."
            )

        df = df.withColumn(
            "solar_generation_actual",
            sf.when(sf.col("solar_generation_actual").isNull(), sf.lit(0)).otherwise(
                sf.col("solar_generation_actual")
            ),
        )

        if verbose:
            print("Solar generation after null handling (sample):")
            df.select(
                "event_date_utc",
                sf.date_format("event_ts_utc", "yyyy-MM-dd HH:mm:ss").alias(
                    "event_ts_utc"
                ),
                "solar_generation_actual",
            ).orderBy("event_ts_utc").show(20, truncate=False)

        if verbose:
            print("Transformed DataFrame")
            df.select(
                "event_date_utc",
                sf.date_format("event_ts_utc", "HH:mm:ss").alias("events_ts"),
                *[c for c in df.columns if c not in {"event_date_utc", "event_ts_utc"}],
            ).show(truncate=False)

        return df


if __name__ == "__main__":
    from src.extract.core.extractors.file_extractor import FileExtractor
    from src.config.loader import config
    from pyspark.sql import SparkSession

    spark_session = SparkSession.builder.getOrCreate()
    opsd_source = config.sources["opsd"]
    opsd_fe = FileExtractor(config.project_config, opsd_source, spark_session)
    opsd_fe.run()

    OpsdTransformerPipeline(spark_session, config.project_config, opsd_source).run()
