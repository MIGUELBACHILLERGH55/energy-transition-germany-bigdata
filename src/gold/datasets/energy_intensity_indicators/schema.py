from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)

ENERGY_INTENSITY_INDICATORS_SCHEMA = StructType(
    [
        StructField("year", IntegerType(), False),
        StructField("indicator_scope", StringType(), False),
        StructField("indicator_group", StringType(), False),
        StructField("indicator_code", StringType(), False),
        StructField("indicator_label", StringType(), False),
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),
        StructField("dataset", StringType(), False),
    ]
)
