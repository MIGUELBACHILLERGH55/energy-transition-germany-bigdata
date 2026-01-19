from abc import abstractmethod, ABC
import requests
from dataclasses import dataclass
from datetime import date
from src.extract.core.planning.task import ExtractionTask
from typing import Generic, TypeVar

TTask = TypeVar("TTask", bound=ExtractionTask)


@dataclass
class BaseDownloader(ABC, Generic[TTask]):
    """
    Base class for all downloader strategies.

    A downloader is responsible for executing a concrete ExtractionTask.
    Each implementation is expected to support exactly one task subtype.
    """

    session: requests.Session
    base_url: str
    timeout_s: int
    retry: int
    run_date: date

    @abstractmethod
    def prepare(self, task: TTask) -> None:
        """
        Prepare the request based on the provided task.
        """
        pass

    @abstractmethod
    def download(self) -> None:
        """
        Execute the download once preparation is complete.
        """
        pass

    def fetch(self, task: TTask) -> None:
        """
        Template method: prepare + download.
        """
        self.prepare(task)
        self.download()
