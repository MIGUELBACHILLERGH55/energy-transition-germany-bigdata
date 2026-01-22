from src.config.loader import spark_session
from src.gold.datasets.latest_energy_snapshot.pipeline import LatestEnergySnapshot


if __name__ == "__main__":
    latest_energy_snapshot = LatestEnergySnapshot(spark_session)
    latest_energy_snapshot.run()
