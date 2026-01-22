from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    DateType,
)

NUCLEAR_EXIT_CONTEXT_MONTHLY_SCHEMA = StructType(
    [
        # temporal dimensions
        StructField("date", DateType(), False),  # YYYY-MM-01
        StructField("year", IntegerType(), False),
        # technology
        StructField(
            "technology",
            StringType(),
            False,  # nuclear
        ),
        # metric
        StructField(
            "generation_value",
            DoubleType(),
            False,  # monthly nuclear generation
        ),
        StructField(
            "unit",
            StringType(),
            False,  # MWh
        ),
        # contextual flag
        StructField(
            "period",
            StringType(),
            False,  # pre_exit | post_exit
        ),
        # dataset identifier
        StructField(
            "dataset",
            StringType(),
            False,  # nuclear_exit_context_monthly
        ),
    ]
)
