from abc import abstractmethod
import requests
from dataclasses import dataclass
from datetime import date
from src.extract.core.planning.task import ExtractionTask


@dataclass
class BaseDownloader:
    session: requests.Session
    base_url: str
    timeout_s: int
    retry: int
    run_date: date

    @abstractmethod
    def prepare(self, task: ExtractionTask):
        pass

    @abstractmethod
    def download(self):
        pass

    def fetch(self, task: ExtractionTask):
        self.prepare(task)
        self.download()
