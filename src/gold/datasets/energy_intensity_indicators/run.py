from src.config.loader import spark_session
from src.gold.datasets.energy_intensity_indicators.pipeline import (
    EnergyIntensityIndicators,
)


if __name__ == "__main__":
    energy_intensity_indicators = EnergyIntensityIndicators(spark_session)
    energy_intensity_indicators.run()
