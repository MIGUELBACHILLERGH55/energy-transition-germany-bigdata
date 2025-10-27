# DatasetSpec represents the configuration of a single *dataset* inside a source.
#
# - It receives the YAML fields under something like `sources.<source>.datasets.<dataset>`.
# - It stores and validates request parameters, storage rules, metadata, schedule, etc.
# - It is agnostic to how the data is fetched (API, FTP, local files, etc.).
# - The Extractor will iterate over DatasetSpec instances to plan/fetch/parse/persist.
#
# This is also only a configuration model — not executable logic.
