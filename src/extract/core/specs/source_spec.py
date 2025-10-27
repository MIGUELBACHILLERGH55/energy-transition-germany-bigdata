# SourceSpec represents the configuration of a single *data source* as defined in the YAML.
#
# - It receives the YAML section under `sources.<source_name>`.
# - It stores and validates the fields that apply to the entire source (e.g. base_url, enabled, etc.).
# - It must hold a list of DatasetSpec instances — one for each dataset defined under this source.
# - Extractors will receive SourceSpec instead of raw YAML dictionaries.
#
# This class does NOT execute anything — it is only a configuration model.
from typing import Optional


class SourceSpec:
    def __init__(self, 
                 name: str, 
                 enabled: str, 
                 kind: bool, 
                 base_url: Optional[str] = None, 
                 headers: Optional[dict] = None, 
                 retry: Optional[int] = None, 
                 timeout_s: Optional[int] = None
                 ):
        
        self.name = name 
        self.enabled = enabled
        self.kind = kind 
        self.base_url = base_url
        self.headers = headers 
        self.retry = retry 
        self.timeout_s = timeout_s


    @property 
    def name(self):
        return self._name 

    @name.setter 
    def name(self, value):
        # TODO: Validations 
        self._name = value

    
