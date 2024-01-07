from dataclasses import dataclass
from typing import List, Dict

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileRow:
    fields: Dict[str, str]

    def __contains__(self, item):
        return item in self.fields

    def __len__(self):
        return len(self.fields)

    def __iter__(self):
        return iter(self.fields)

    def __getitem__(self, item):
        return self.fields[item]

    def __reversed__(self):
        return reversed(self.fields)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileInstance:
    file_name: str
    file_rows: List[FileRow]

    def __contains__(self, item):
        return item in self.file_rows

    def __len__(self):
        return len(self.file_rows)

    def __iter__(self):
        return iter(self.file_rows)

    def __getitem__(self, item):
        return self.file_rows[item]
