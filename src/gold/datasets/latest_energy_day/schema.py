from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    TimestampType,
    DateType,
)

LATEST_ENERGY_DAY_SCHEMA = StructType(
    [
        StructField("timestamp", TimestampType(), False),
        StructField("run_date", DateType(), False),
        StructField("metric", StringType(), False),  # load | price
        StructField("value", DoubleType(), False),
        StructField("unit", StringType(), False),  # MW | EUR/MWh
        StructField("dataset", StringType(), False),
    ]
)
