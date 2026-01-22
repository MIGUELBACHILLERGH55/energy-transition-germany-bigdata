from src.config.loader import spark_session
from src.gold.datasets.renewables_by_technology.pipeline import RenewablesByTechnology


if __name__ == "__main__":
    renewables_by_technology = RenewablesByTechnology(spark_session)
    renewables_by_technology.run()
