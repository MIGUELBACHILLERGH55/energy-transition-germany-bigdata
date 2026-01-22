from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    DateType,
)

ELECTRICITY_PRICE_TRENDS_MONTHLY_SCHEMA = StructType(
    [
        # temporal dimensions
        StructField("date", DateType(), False),  # YYYY-MM-01
        StructField("year", IntegerType(), False),
        # metric dimensions
        StructField("price_value", DoubleType(), False),
        StructField(
            "price_type",
            StringType(),
            False,  # market_price | consumer_price_index
        ),
        StructField(
            "unit",
            StringType(),
            False,  # EUR/MWh | index (2015=100)
        ),
        # source & resolution
        StructField(
            "source",
            StringType(),
            False,  # SMARD | Eurostat
        ),
        StructField(
            "resolution",
            StringType(),
            False,  # month
        ),
    ]
)
