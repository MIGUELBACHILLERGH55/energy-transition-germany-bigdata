from src.config.loader import spark_session
from src.gold.datasets.latest_energy_day.pipeline import LatestEnergyDay


if __name__ == "__main__":
    latest_energy_day = LatestEnergyDay(spark_session)
    latest_energy_day.run()
