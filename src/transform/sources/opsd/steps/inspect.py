from pyspark.sql import DataFrame
from pyspark.sql import functions as sf


def inspect_nulls_by_month_hour(df: DataFrame, col_name: str | None = None):
    if not col_name:
        cols = [
            col
            for col in df.columns
            if col
            not in ("cet_cest_timestamp", "event_date_utc", "event_ts", "event_ts_utc")
        ]
        agg_expressions = [
            sf.sum(sf.col(col_name).isNull().cast("int")).alias("null_" + col_name)
            for col_name in cols
        ]
    else:
        agg_expressions = [
            sf.sum(sf.col(col_name).isNull().cast("int")).alias("null_" + col_name)
        ]
    new_df = (
        df.groupBy(
            sf.month("cet_cest_timestamp").alias("month"),
            sf.hour("cet_cest_timestamp").alias("hour"),
        )
        .agg(sf.count("*").alias("total_rows"), *agg_expressions)
        .orderBy("month", "hour")
    )

    return new_df


def show_nulls_by_month_hour(df: DataFrame, col_name: str | None = None):
    df = inspect_nulls_by_month_hour(df, col_name)
    df.show()


def inspect_nulls_by_hour(df: DataFrame, col_name: str):
    new_df = df.groupBy(sf.hour("cet_cest_timestamp").alias("hour")).agg(
        sf.count("*").alias("total_rows"),
        sf.sum(sf.col(col_name).isNull().cast("int")).alias("null_" + col_name),
    )

    new_df = new_df.withColumn("ratio", sf.try_divide("null_" + col_name, "total_rows"))
    return new_df


def show_nulls_by_hour(df: DataFrame, col_name: str):
    df = inspect_nulls_by_hour(df, col_name)
    df.orderBy("hour").show(25)
