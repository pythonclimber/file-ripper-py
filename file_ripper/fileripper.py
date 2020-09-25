from typing import IO, List

from file_ripper.filedefinition import FileDefinition
from file_ripper.fileservice import FileService


class FileRipper:
    def rip_file(self, file: IO, file_definition: FileDefinition):
        file_service = FileService.create_file_service(file_definition)
        return file_service.process(file)

    def rip_files(self, files: List[IO], file_definition: FileDefinition):
        return [self.rip_file(f, file_definition) for f in files]
