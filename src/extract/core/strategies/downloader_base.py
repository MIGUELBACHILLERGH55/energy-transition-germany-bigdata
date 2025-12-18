from abc import abstractmethod
import requests
from dataclasses import dataclass


@dataclass
class BaseDownloader:
    session: requests.Session
    base_url: str
    timeout_s: int
    retry: int

    @abstractmethod
    def download(self, plan_item):
        pass
