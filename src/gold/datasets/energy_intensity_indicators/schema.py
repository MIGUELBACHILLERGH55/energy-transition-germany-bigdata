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
        StructField("dimension", StringType(), False),
        StructField("unit", StringType(), False),
        StructField("value", DoubleType(), False),

        # metadata / enrichment
        StructField("table_id", StringType(), False),
        StructField("dataset", StringType(), False),

        # semantic columns for BI
        StructField("indicator_label", StringType(), False),
        StructField("indicator_group", StringType(), False),
        StructField("indicator_scope", StringType(), False),
    ]
)
