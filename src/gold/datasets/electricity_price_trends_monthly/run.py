from src.config.loader import spark_session
from src.gold.datasets.electricity_price_trends_monthly.pipeline import (
    ElectricityPriceTrendsMonthly,
)


if __name__ == "__main__":
    electricity_price_trends_monthly = ElectricityPriceTrendsMonthly(spark_session)
    electricity_price_trends_monthly.run()
