from typing import IO
from xml.etree.ElementTree import fromstring

import file_ripper.fileconstants as fc
from file_ripper.filedefinition import FileDefinition
from file_ripper.fileinstance import FileInstance, FileRow


class FileService:
    def __init__(self, file_definition):
        self.file_definition = file_definition

    def process(self, file: IO) -> FileInstance:
        records = self.process_file_records(file)
        return FileInstance(file.name, records)

    def process_file_records(self, file):
        raise NotImplementedError("Please use a valid implementation of FileService to read files")


class XmlFileService(FileService):
    def __init__(self, file_definition):
        super().__init__(file_definition)

    def process_file_records(self, file: IO):
        tree = fromstring("".join(file.readlines()))

        file_rows = []
        for item in tree.findall(f"./{self.file_definition.record_element_name}"):
            record = {}
            for field_def in self.file_definition.field_definitions:
                record[field_def.field_name] = item.find(f"{field_def.field_name}").text
            file_rows.append(FileRow(record))

        return file_rows


class FlatFileService(FileService):
    def __init__(self, file_definition: FileDefinition):
        super().__init__(file_definition)

    def process_file_records(self, file: IO):
        records = []
        lines = file.readlines()
        if self.file_definition.has_header:
            lines.pop(0)

        for line in lines:
            record = (
                self.process_delimited_line(line)
                if self.file_definition.file_type == fc.DELIMITED
                else self.process_fixed_line(line)
            )
            records.append(record)

        return records

    def process_delimited_line(self, line):
        fields = [field.rstrip() for field in line.split(self.file_definition.delimiter)]
        record = {}

        field_count = len(self.file_definition.field_definitions)
        if field_count != len(fields):
            raise OSError("File records do not match file definition")

        for i in range(0, field_count):
            record[self.file_definition.field_definitions[i].field_name] = fields[
                self.file_definition.field_definitions[i].position_in_row
            ]
        return FileRow(record)

    def process_fixed_line(self, line):
        record = {}
        for field_def in self.file_definition.field_definitions:
            end_position = field_def.start_position + field_def.field_length
            if end_position > len(line.rstrip()):
                raise IndexError(f"field {field_def.field_name} extends past the end of line")
            record[field_def.field_name] = line[field_def.start_position : end_position].rstrip()
        return FileRow(record)


def create_file_service(file_definition):
    if file_definition.file_type == fc.XML:
        return XmlFileService(file_definition)
    elif file_definition.file_type == fc.DELIMITED:
        return FlatFileService(file_definition)
    elif file_definition.file_type == fc.FIXED:
        return FlatFileService(file_definition)
    else:
        raise ValueError(f"file_definition is configured for unsupported file_type: {file_definition.file_type}")
