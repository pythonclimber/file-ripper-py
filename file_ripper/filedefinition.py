from dataclasses import dataclass, field
from typing import List

import file_ripper.fileconstants as fc


@dataclass
class FieldDefinition:
    field_name: str
    start_position: int = field(default=None)
    field_length: int = field(default=None)
    xml_node_name: str = field(default='')

    @classmethod
    def create_from_json(cls, file_type, json_data):
        cls.validate_json(file_type, json_data)
        return cls(**json_data)

    @staticmethod
    def validate_json(file_type, json_data):
        if fc.FIELD_NAME not in json_data:
            raise ValueError('field_name is required for a valid FieldDefinition')

        if file_type == fc.FIXED and (fc.START_POSITION not in json_data or fc.FIELD_LENGTH not in json_data):
            raise ValueError('start_position and field_length are required for a fixed position file')


@dataclass
class FileDefinition:
    file_type: str
    field_definitions: List[FieldDefinition]
    has_header: bool = field(default=False)
    delimiter: str = field(default='')
    record_element_name: str = field(default='')
    input_directory: str = field(default='')
    completed_directory: str = field(default='')
    file_mask: str = field(default='')
    # export_definition: ExportDefinition = field(default=None)

    @classmethod
    def create_from_json(cls, json_data: dict):
        json_copy = json_data.copy()
        cls.validate_json(json_copy)
        json_copy[fc.FIELD_DEFINITIONS] = [FieldDefinition.create_from_json(json_copy[fc.FILE_TYPE], obj)
                                           for obj in json_copy[fc.FIELD_DEFINITIONS]]
        return cls(**json_copy)

    @staticmethod
    def validate_json(json_data):
        if fc.FILE_TYPE not in json_data:
            raise ValueError(f'{fc.FILE_TYPE} is a required property')

        if fc.FIELD_DEFINITIONS not in json_data:
            raise ValueError(f'{fc.FIELD_DEFINITIONS} is a required property')

        if json_data[fc.FILE_TYPE] == fc.DELIMITED and fc.DELIMITER not in json_data:
            raise ValueError(f'{fc.DELIMITER} is a required property for delimited files')

        if json_data[fc.FILE_TYPE] == fc.XML and fc.RECORD_ELEMENT_NAME not in json_data:
            raise ValueError(f'{fc.RECORD_ELEMENT_NAME} is a required property for xml files')
