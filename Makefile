.PHONY: extract-ageb extract-eea extract-opsd bronze clean-bronze refresh-bronze

extract-ageb:
	python -m src.extract.sources.ageb.run

extract-eea:
	python -m src.extract.sources.eea.run

extract-opsd:
	python -m src.extract.sources.opsd.run

extract-smard-indices:
	python -m src.extract.sources.smard.run.indices

clean-smard-indices:
	rm -rf data/landing/smard

refresh-smard-indices: clean-smard-indices extract-smard-indices

extract-smard-last-available-ts:
	python -m src.extract.sources.smard.run.timeseries

bronze: extract-ageb extract-eea extract-opsd extract-smard-last-available-ts

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

clean-silver:
	rm -rf data/silver

silver: bronze transform-ageb transform-eea transform-opsd transform-smard

refresh-silver: clean-silver silver


