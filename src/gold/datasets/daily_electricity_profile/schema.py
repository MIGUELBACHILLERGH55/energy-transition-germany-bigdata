from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    BooleanType,
    DateType,
)

DAILY_ELECTRICITY_METRICS_SCHEMA = StructType(
    [
        # temporal dimensions
        StructField("date", DateType(), False),
        StructField("year", IntegerType(), False),
        StructField("month", IntegerType(), False),
        StructField("month_name", StringType(), False),
        StructField("day_of_week", StringType(), False),
        StructField("is_weekend", BooleanType(), False),
        # metric dimensions
        StructField("metric", StringType(), False),
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),
        # metadata
        StructField("dataset", StringType(), False),
    ]
)
