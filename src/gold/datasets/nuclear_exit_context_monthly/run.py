from src.config.loader import spark_session
from src.gold.datasets.nuclear_exit_context_monthly.pipeline import (
    NuclearExitContextMonthly,
)


if __name__ == "__main__":
    nuclear_exit_context_monthly = NuclearExitContextMonthly(spark_session)
    nuclear_exit_context_monthly.run()
