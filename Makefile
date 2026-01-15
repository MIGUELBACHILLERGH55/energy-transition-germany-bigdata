.PHONY: extract-ageb extract-eea extract-opsd bronze clean-bronze refresh-bronze

extract-ageb:
	python -m src.extract.sources.ageb.run

extract-eea:
	python -m src.extract.sources.eea.run

extract-opsd:
	python -m src.extract.sources.opsd.run

bronze: extract-ageb extract-eea extract-opsd

clean-bronze:
	rm -rf data/bronze

refresh-bronze: clean-bronze bronze

transform-ageb:
	python -m src.transform.sources.ageb.run

transform-eea:
	python -m src.transform.sources.eea.run

transform-opsd:
	python -m src.transform.sources.opsd.run

clean-silver:
	rm -rf data/silver

silver: bronze transform-ageb transform-eea transform-opsd

refresh-silver: clean-silver silver

