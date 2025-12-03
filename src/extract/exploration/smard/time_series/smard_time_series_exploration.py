# energy-transition-germany-bigdata/src/extract/exploration/smard/times_series/smard_time_series_exploration.py
from ..constants import filters_to_explore, resolutions_to_explore
from .helpers import smard_time_series_exploration

smard_time_series_exploration(
    resolutions_to_explore, filters_to_explore, verbose=True, save=True
)
