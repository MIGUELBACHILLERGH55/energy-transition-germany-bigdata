# --------- Template class to Extract data ----------
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """
    BaseExtractor defines the extraction lifecycle using the Template Method pattern.
    Subclasses only override the hooks; the high-level flow lives here. 
    """

    def __init__(self, source_name, source_spec, *, context=None) -> None:
        self.source_name = source_name # e.g. "smard"
        self.source_spec = source_spec # SourceSpec object 
        self.datasets = source_spec.datasets # list[DatasetSpec]
        self.context = context # logger, tz, policies, etc
    
    # TODO:  finish this, might add a verbose option.
    def run(self):
        """
        Orchestrates the entire extraction process in the correct order: 
        1. prepare()
        2. plan()
        3. fetch() per PlanItem
        4. parse() each RawResponse
        5. persist_landing() each ParsedBatch
        6. report() for observability and metrics

        Returns a summary (dict or None) - e.g., written paths, row counts, timings.
        Should not be overriden.
        """
        pass
    

    def prepare(self):
        """
        Prepare the extraction environment:
        - Initialize the HTTPS session (if API)
        - Apply headers, retry/timeout defaults or rate-limiters
        - Resolve landing paths, create folders if needed
        - Set timezone or source-level configurations

        No network I/O should be performed here. Just the set up.
        """
        pass 

    def plan(self):
        """
        Produce a list of PlanItem objects (one unit of work per dataset/time window).
        Each PlanItem must contain all necessary parameters (endopoint, file_path, etc.)

        Returns: List[PlanItem]
        """
        pass 

    def fetch(self, plan_item):
        """
        Execute one PlanItem:
        - If access=api -> make request with retry, timeout, rate limit
        - If access=file -> read file from filesystem
        - If access=other -> handle accordingly.

        Returns a RawResponse (raw payload + metadata)
        """
        pass 

    def parse(self, raw_response, plan_item):
        """
        Convert raw response to a minimally normalized structure:
        - Decode CSV/JSON/bytes -> structured records
        - Parse timestamps, enforce correct timezone
        - Validate required columns / schema for landing 

        Returns a ParsedBatch (clean, ready for landing)
        """
        
        pass 

    def persist_landing(self, parsed_batch, plan_item):
        """
        Persist parsed data into the landing layer idempotently:
        - Use file_naming template (e.g., {yyyy}-{mm}-{dd}.csv)
        - Create directories if missing.
        - Avoid duplicates (overwrites deterministically or skip existing)

        Returns a summary dict -> e.g. {"path": "...", "rows": 123}.
        """
        pass 

    def report(self, summary):
        """
        Emit structured logs / metrics:
        - row counts , file sizes, timings, error rates
        - tags such as source_name, dataset_id, date window

        This method should not raise any exceptions - best-effor observability.
        """
        pass


    



