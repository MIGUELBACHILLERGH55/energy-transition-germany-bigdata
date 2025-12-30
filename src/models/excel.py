from dataclasses import dataclass


@dataclass
class ExcelReadTask:
    sheet: str
    section: str
    header_row: int
    row_start: int
    row_end: int
