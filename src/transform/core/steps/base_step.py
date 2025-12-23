from pyspark.sql import DataFrame
from pyspark.sql import functions as sf


def remove_cols(df: DataFrame, cols_to_remove: list[str]):
    df = df.drop(*cols_to_remove)
    return df


def change_order_cols(df: DataFrame, cols_new_order: list[str]):
    df = df.select(*cols_new_order)
    return df


def strip_prefix_before_delimiter(df: DataFrame, col_name: str, delimiter="-"):
    pattern = f"^.*?\\{delimiter}\\s*"
    df = df.withColumn(
        col_name,
        sf.regexp_replace(
            col_name,
            pattern,
            "",
        ),
    )
    return df


def rename_cols(df: DataFrame, cols_map: dict[str, str]):
    df = df.withColumnsRenamed(cols_map)
    return df


def add_mapped_column(df, new_col_name, source_col, value_map):
    mapping_expr = sf.create_map(
        *[x for kv in value_map.items() for x in map(sf.lit, kv)]
    )
    return df.withColumn(
        new_col_name,
        sf.coalesce(
            mapping_expr[sf.col(source_col)], sf.col(source_col)
        ),  # sf.col(source_col) is used as a fallback
    )


def null_counts_by_column(df):
    return df.select(
        [sf.sum(sf.col(c).isNull().cast("int")).alias(c) for c in df.columns]
    )


def show_null_counts(df):
    null_counts_by_column(df).show()
