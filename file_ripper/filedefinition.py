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


class ExportDefinition:
    def __init__(self, file_data):
        if fc.EXPORT_TYPE not in file_data:
            raise ValueError(f'{fc.EXPORT_TYPE} is a required property')

        if file_data[fc.EXPORT_TYPE] == fc.API_EXPORT and fc.API_URL not in file_data:
            raise ValueError(f'{fc.API_URL} is a required property for an {fc.EXPORT_TYPE} of {fc.API_EXPORT}')

        if file_data[fc.EXPORT_TYPE] == fc.DATABASE_EXPORT and fc.DB_CONNECTION_STRING not in file_data:
            raise ValueError(f'{fc.DB_CONNECTION_STRING} is a required property for {fc.EXPORT_TYPE} '
                             f'of {fc.DATABASE_EXPORT}')

        if file_data[fc.EXPORT_TYPE] == fc.FILE_EXPORT and fc.OUTPUT_FILE_PATH not in file_data:
            raise ValueError(f'{fc.OUTPUT_FILE_PATH} is required for {fc.EXPORT_TYPE} of {fc.FILE_EXPORT}')

        self.export_type = file_data[fc.EXPORT_TYPE]
        self.api_url = file_data[fc.API_URL] if fc.API_URL in file_data else ''
        self.db_connection_string = file_data[fc.DB_CONNECTION_STRING] if fc.DB_CONNECTION_STRING in file_data else ''
        self.output_file_path = file_data[fc.OUTPUT_FILE_PATH] if fc.OUTPUT_FILE_PATH in file_data else ''
        self.http_headers = file_data[fc.HTTP_HEADERS] if fc.HTTP_HEADERS in file_data else {}
        self.collection_name = file_data[fc.COLLECTION_NAME] if fc.COLLECTION_NAME in file_data else ''
        self.database_name = file_data[fc.DATABASE_NAME] if fc.DATABASE_NAME in file_data else ''


@dataclass
class FileDefinition:
    file_type: str
    field_definitions: List[FieldDefinition]
    has_header: bool = field(default=False)
    delimiter: str = field(default='')
    record_element_name: str = field(default='')
    # input_directory: str = field(default='')
    # completed_directory: str = field(default='')
    # export_definition: ExportDefinition = field(default=None)
    # file_mask: str = field(default='')

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
