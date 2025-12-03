# energy-transition-germany-bigdata/src/extract/exploration/smard/smard_indices_exploration.py

# ============ SMARD Inidice Enpoint Exploration ===========

from extract.exploration.smard.constants import (
    resolutions_to_explore,
    filters_to_explore,
)
from extract.exploration.smard.indices.helpers import smard_indices_exploration


smard_indices_exploration(resolutions_to_explore, filters_to_explore, save=True)
