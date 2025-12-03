# extract/exploration/smard/prototypes/smard_prototype_extractor.py

from ..indices.smard_indices_exploration import smard_indices_exploration
from ..time_series.smard_time_series_exploration import (
    smard_time_series_exploration,
)
from ..constants import resolutions_to_explore, filters_to_explore
from pathlib import Path


CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[5]
LANDING_SMARD_DIR = PROJECT_ROOT / "data" / "landing" / "smard"


class SmardExtractor:
    """
    Prototipo inicial de extractor de datos SMARD.
    Encapsula la lógica de exploración de índices y
    extracción de series temporales reales.

    Attributes
    ----------
    filters : dict
        Diccionario {nombre: código API}
    resolutions : list
        Lista de resoluciones a explorar (ej. ["hour"])
    verbose : bool
        Mostrar información en consola
    save : bool
        Guardar los outputs en disco
    """

    def __init__(self, filters=None, resolutions=None, verbose=True, save=True):
        self.filters = filters or filters_to_explore
        self.resolutions = resolutions or resolutions_to_explore
        self.verbose = verbose
        self.save = save

    def run_indices(self):
        """
        Ejecuta la exploración de índices SMARD (timestamps disponibles).
        """
        print("\n➡ [SmardExtractor] Explorando índices...\n")
        print("Saving at: ", LANDING_SMARD_DIR / "indices_metadata_summaries")
        smard_indices_exploration(
            resolutions_to_explore=self.resolutions,
            filters_to_explore=self.filters,
            include_or_list=True,
            verbose=self.verbose,
            save=self.save,
            output_dir=LANDING_SMARD_DIR / "indices_metadata_summaries",
        )

    def run_time_series(self):
        """
        Ejecuta la extracción de una muestra real de valores de las time-series.
        """
        print("\n➡ [SmardExtractor] Explorando time-series...\n")
        print("Saving at: ", LANDING_SMARD_DIR / "time_series_metadata_summaries")
        smard_time_series_exploration(
            resolutions_to_explore=self.resolutions,
            filters_to_explore=self.filters,
            verbose=self.verbose,
            save=self.save,
            output_dir=LANDING_SMARD_DIR / "time_series_metadata_summaries",
        )

    def run_all(self):
        """
        Ejecuta todo el proceso de extracción:
        primero índices → luego time-series.
        """
        print("\n=== SMARD EXTRACTOR PROTOTYPE ===\n")
        self.run_indices()
        self.run_time_series()
        print("\n=== FIN EXTRACCIÓN SMARD ===\n")


if __name__ == "__main__":
    extractor = SmardExtractor()
    extractor.run_all()
