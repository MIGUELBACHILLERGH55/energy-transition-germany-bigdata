from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
)

RENEWABLES_BY_TECHNOLOGY_SCHEMA = StructType(
    [
        # core dimensions
        StructField("year", IntegerType(), False),
        StructField("technology", StringType(), False),
        # measures
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),
        # technical metadata
        StructField("dataset", StringType(), False),
    ]
)
