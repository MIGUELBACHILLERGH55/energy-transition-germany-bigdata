from src.config.loader import spark_session
from src.gold.datasets.final_energy_consumption_by_sector.pipeline import (
    FinalEnergyConsumptionBySector,
)


if __name__ == "__main__":
    final_energy_consumption_by_sector = FinalEnergyConsumptionBySector(spark_session)
    final_energy_consumption_by_sector.run()
