from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    BooleanType,
    DateType,
)

DAILY_ELECTRICITY_PROFILE_SCHEMA = StructType(
    [
        # temporal dimensions
        StructField("date", DateType(), False),
        StructField("year", IntegerType(), False),
        StructField("month", IntegerType(), False),
        StructField("month_name", StringType(), False),
        StructField("day_of_week", StringType(), False),
        StructField("is_weekend", BooleanType(), False),
        # core metrics
        StructField("load_act_daily", DoubleType(), False),
        StructField("solar_gen_daily", DoubleType(), False),
        StructField("wind_gen_daily", DoubleType(), False),
        StructField("renewables_gen_daily", DoubleType(), False),
        # derived metrics (shares)
        StructField("renewables_share", DoubleType(), False),
        StructField("solar_share", DoubleType(), False),
        StructField("wind_share", DoubleType(), False),
        # metadata
        StructField("dataset", StringType(), False),
    ]
)
