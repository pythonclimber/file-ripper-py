from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json, LetterCase
from dataclasses_json.stringcase import snakecase

import file_ripper.fileconstants as fc


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FieldDefinition:
    field_name: str
    file_type: str
    start_position: int
    field_length: int
    xml_node_name: str
    position_in_row: int

    def __init__(
        self,
        field_name: str,
        file_type: str,
        start_position: int = None,
        field_length: int = None,
        xml_node_name: str = "",
        position_in_row: int = None,
    ):
        self._validate(file_type, field_name, start_position, field_length, position_in_row)
        self.file_type = file_type
        self.field_name = field_name
        self.start_position = start_position
        self.field_length = field_length
        self.position_in_row = position_in_row
        self.xml_node_name = xml_node_name if xml_node_name else field_name

    @classmethod
    def create_from_dict(cls, file_type, field_definition: dict):
        field_def_copy = {snakecase(k): v for k, v in field_definition.items()}
        return cls(file_type=file_type, **field_def_copy)

    @staticmethod
    def _validate(file_type, field_name, start_position, field_length, position_in_row):
        if not field_name:
            raise ValueError("field_name is required")

        if not file_type:
            raise ValueError("file_type is required")

        if file_type == fc.FIXED and (start_position is None or field_length is None):
            raise ValueError("start_position and field_length are required for a fixed position field")

        if file_type == fc.DELIMITED and position_in_row is None:
            raise ValueError("position_in_row is required for delimited files")

        # if file_type == fc.XML and not xml_node_name:
        #     raise ValueError('xml_node_name is required for a field in xml')


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FileDefinition:
    file_type: str
    field_definitions: List[FieldDefinition]
    has_header: bool = field(default=False)
    delimiter: str = field(default="")
    record_xml_element: str = field(default="")
    input_directory: str = field(default="")
    completed_directory: str = field(default="")
    file_mask: str = field(default="")

    def __init__(
        self,
        file_type,
        field_definitions,
        has_header=False,
        delimiter="",
        record_xml_element="",
        input_directory="",
        completed_directory="",
        file_mask="",
    ):
        self._validate(file_type, field_definitions, delimiter, record_xml_element)
        self.file_type = file_type
        self.field_definitions = field_definitions
        self.has_header = has_header
        self.delimiter = delimiter
        self.record_xml_element = record_xml_element
        self.input_directory = input_directory
        self.completed_directory = completed_directory
        self.file_mask = file_mask

    @classmethod
    def create_from_dict(cls, json_data: dict):
        json_copy = {snakecase(k): v for k, v in json_data.items()}
        json_copy[fc.FIELD_DEFINITIONS] = [
            FieldDefinition.create_from_dict(json_copy[fc.FILE_TYPE], obj) for obj in json_copy[fc.FIELD_DEFINITIONS]
        ]
        return cls(**json_copy)

    @staticmethod
    def _validate(file_type, field_definitions, delimiter, record_element_name):
        if not file_type:
            raise ValueError("file_type is required")

        if not field_definitions:
            raise ValueError("field_definitions is required")

        if file_type == fc.DELIMITED and not delimiter:
            raise ValueError("delimiter is required for delimited files")

        if file_type == fc.XML and not record_element_name:
            raise ValueError("record_element_name is required for xml files")
