from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)

ENERGY_MIX_TOTAL_SCHEMA = StructType(
    [
        StructField("year", IntegerType(), False),
        StructField("dimension", StringType(), False),  # energy source
        StructField("metric", StringType(), False),  # energy | share
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),  # PJ | ratio
        StructField("dataset", StringType(), False),
    ]
)
