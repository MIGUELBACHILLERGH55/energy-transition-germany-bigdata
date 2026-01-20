from src.config.loader import spark_session
from src.gold.datasets.energy_mix_total.pipeline import EnergyMixTotal


if __name__ == "__main__":
    energy_mix_total = EnergyMixTotal(spark_session)
    energy_mix_total.run()
