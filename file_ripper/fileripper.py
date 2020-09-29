from typing import IO, List, Tuple

from file_ripper.filedefinition import FileDefinition
from file_ripper.fileservice import FileService


def rip_file(file: IO, file_definition: FileDefinition) -> Tuple[str, dict]:
    file_service = FileService.create_file_service(file_definition)
    return file_service.process(file)


def rip_files(files: List[IO], file_definition: FileDefinition) -> List[Tuple[str, dict]]:
    return [rip_file(f, file_definition) for f in files]
