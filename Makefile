.PHONY: \
	# extract
	extract-ageb extract-eea extract-opsd extract-eurostat \
	extract-smard-indices extract-all-smard \
	clean-smard-indices refresh-smard-indices \
	# bronze
	bronze clean-bronze refresh-bronze \
	# silver
	transform-ageb transform-eea transform-opsd transform-smard transform-eurostat \
	silver clean-silver refresh-silver \
	# gold datasets
	gold-energy-mix-total \
	gold-energy-intensity-indicators \
	gold-final-energy-consumption-by-sector \
	gold-renewables-by-technology \
	gold-daily-electricity-profile \
	gold-latest-energy-day \
	gold-electricity-price-trends-monthly \
	gold-nuclear-exit-context-monthly \
	# gold orchestration
	gold clean-gold refresh-gold \
	# full pipelines
	refresh-silver-gold refresh-all


# =========================
# EXTRACT
# =========================

extract-ageb:
	python -m src.extract.sources.ageb.run

extract-eea:
	python -m src.extract.sources.eea.run

extract-opsd:
	python -m src.extract.sources.opsd.run

extract-eurostat:
	python -m src.extract.sources.eurostat.run

extract-smard-indices:
	python -m src.extract.sources.smard.run.indices

clean-smard-indices:
	rm -rf data/landing/smard

refresh-smard-indices: clean-smard-indices extract-smard-indices

extract-all-smard:
	python -m src.extract.sources.smard.run.timeseries


# =========================
# BRONZE
# =========================

bronze: \
	extract-ageb \
	extract-eea \
	extract-opsd \
	refresh-smard-indices \
	extract-all-smard \
	extract-eurostat

clean-bronze:
	rm -rf data/bronze

refresh-bronze: clean-bronze bronze


# =========================
# SILVER
# =========================

transform-ageb:
	python -m src.transform.sources.ageb.run

transform-eea:
	python -m src.transform.sources.eea.run

transform-opsd:
	python -m src.transform.sources.opsd.run

transform-smard:
	python -m src.transform.sources.smard.run

transform-eurostat:
	python -m src.transform.sources.eurostat.run

silver: bronze \
	transform-ageb \
	transform-eea \
	transform-opsd \
	transform-smard \
	transform-eurostat

clean-silver:
	rm -rf data/silver

refresh-silver: clean-silver silver


# =========================
# GOLD DATASETS
# =========================

gold-energy-mix-total:
	python -m src.gold.datasets.energy_mix_total.run

gold-energy-intensity-indicators:
	python -m src.gold.datasets.energy_intensity_indicators.run

gold-final-energy-consumption-by-sector:
	python -m src.gold.datasets.final_energy_consumption_by_sector.run

gold-renewables-by-technology:
	python -m src.gold.datasets.renewables_by_technology.run

gold-daily-electricity-profile:
	python -m src.gold.datasets.daily_electricity_profile.run

gold-latest-energy-day:
	python -m src.gold.datasets.latest_energy_day.run

gold-electricity-price-trends-monthly:
	python -m src.gold.datasets.electricity_price_trends_monthly.run

gold-nuclear-exit-context-monthly:
	python -m src.gold.datasets.nuclear_exit_context_monthly.run


# =========================
# GOLD ORCHESTRATION
# =========================

gold: \
	gold-energy-mix-total \
	gold-energy-intensity-indicators \
	gold-final-energy-consumption-by-sector \
	gold-renewables-by-technology \
	gold-daily-electricity-profile \
	gold-latest-energy-day \
	gold-electricity-price-trends-monthly \
	gold-nuclear-exit-context-monthly

clean-gold:
	rm -rf data/gold

refresh-gold: clean-gold gold


# =========================
# FULL PIPELINES
# =========================

# From silver upwards
refresh-silver-gold: clean-silver clean-gold silver gold

# Full rebuild from scratch
refresh-all: clean-bronze clean-silver clean-gold bronze silver gold
