from abc import abstractmethod
import requests
from dataclasses import dataclass
from datetime import date
from src.extract.core.planning.plan_item import PlanItem


@dataclass
class BaseDownloader:
    session: requests.Session
    base_url: str
    timeout_s: int
    retry: int
    run_date: date

    @abstractmethod
    def prepare(self, pi: PlanItem):
        pass

    @abstractmethod
    def download(self):
        pass

    def fetch(self, pi: PlanItem):
        self.prepare(pi)
        self.download()
