from src.config.loader import spark_session
from src.gold.datasets.daily_electricity_profile.pipeline import DailyElectricityProfile


if __name__ == "__main__":
    daily_electricity_profile = DailyElectricityProfile(spark_session)
    daily_electricity_profile.run()
