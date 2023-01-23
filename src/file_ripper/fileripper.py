import glob
import os
from typing import IO, List

from file_ripper.filedefinition import FileDefinition
from file_ripper.fileinstance import FileInstance
from file_ripper.fileservice import create_file_service


def validate_file_definition(file_definition: FileDefinition):
    if not file_definition.input_directory:
        raise ValueError("input_directory is required")

    if not file_definition.file_mask:
        raise ValueError("file_mask is required")

    if file_definition.completed_directory and not os.path.exists(file_definition.completed_directory):
        os.mkdir(file_definition.completed_directory)


def move_file_if_needed(file_name: str, file_definition: FileDefinition):
    if file_definition.completed_directory:
        os.rename(
            f"{file_definition.input_directory}/{os.path.split(file_name)[-1]}",
            f"{file_definition.completed_directory}/{os.path.split(file_name)[-1]}",
        )


def rip_file(file: IO, file_definition: FileDefinition) -> FileInstance:
    file_service = create_file_service(file_definition)
    return file_service.process(file)


def rip_files(files: List[IO], file_definition: FileDefinition) -> List[FileInstance]:
    return [rip_file(f, file_definition) for f in files]


def find_and_rip_files(file_definition: FileDefinition) -> List[FileInstance]:
    validate_file_definition(file_definition)
    file_output_list = []

    for file_name in glob.glob(f"{file_definition.input_directory}/{file_definition.file_mask}"):
        with open(file_name, "r") as file:
            file_output_list.append(rip_file(file, file_definition))

        move_file_if_needed(file_name, file_definition)

    return file_output_list
