from dataclasses import dataclass
from typing import List, Dict


@dataclass
class FileRow:
    fields: Dict[str, str]

    def __iter__(self):
        return self.fields.__iter__()

    def __getitem__(self, item):
        return self.fields[item]


@dataclass
class FileInstance:
    file_name: str
    file_rows: List[FileRow]

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.file_rows):
            raise StopIteration
        row, self.i = self.file_rows[self.i], self.i + 1
        return row

    def __getitem__(self, item):
        return self.file_rows[item]
