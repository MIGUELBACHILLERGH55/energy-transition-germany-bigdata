from extract.core.specs.source_spec import SourceSpec
from extract.core.base import BaseExtractor

class ExtractorFactory:
    """ Decides which Extractor to use based on the source_name input. """
    

    def create(self, source_name: str, source_spec: SourceSpec, *, context=None) -> BaseExtractor:
        # TODO: document this appropiately.
        """ Creates the appropiate Extractor Class for the source name,
        and passes the source specs. 
        """
        pass
