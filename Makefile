.PHONY: \
	extract-ageb extract-eea extract-opsd extract-eurostat \
	extract-smard-indices extract-all-smard \
	clean-smard-indices refresh-smard-indices \
	bronze clean-bronze refresh-bronze \
	transform-ageb transform-eea transform-opsd transform-smard transform-eurostat \
	silver clean-silver refresh-silver

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

bronze: extract-ageb extract-eea extract-opsd refresh-smard-indices extract-all-smard extract-eurostat

clean-bronze:
	rm -rf data/bronze

refresh-bronze: clean-bronze bronze

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

clean-silver:
	rm -rf data/silver

silver: bronze transform-ageb transform-eea transform-opsd transform-smard transform-eurostat

refresh-silver: clean-silver silver


