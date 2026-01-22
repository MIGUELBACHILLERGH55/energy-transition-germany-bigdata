from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)

FINAL_ENERGY_CONSUMPTION_BY_SECTOR_SCHEMA = StructType(
    [
        # core dimensions
        StructField("year", IntegerType(), False),
        StructField("sector", StringType(), False),
        StructField("energy_source", StringType(), False),
        # metric definition
        StructField("metric", StringType(), False),  # energy | share
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),  # PJ | ratio
        # metadata
        StructField("dataset", StringType(), False),
    ]
)
