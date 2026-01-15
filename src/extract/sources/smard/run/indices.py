from src.config.loader import config
from src.extract.sources.smard.extractors.indices_extractor import SmardIndicesExtractor


proj_config = config.project_config
smard_source = config.sources["smard"]

if __name__ == "__main__":
    smard_indices_extractor = SmardIndicesExtractor(
        proj_config,
        smard_source,
    )

    smard_indices_extractor.run()
