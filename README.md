# file-ripper

A small lightweight library to parse your flat files and deliver the data inside.

## Install

file-ripper is available on PyPI.

## FileDefinition and FieldDefinition

file-ripper provides multiple ways for you to parse your files.  Using file-ripper's FileDefinition and FieldDefinition contracts, you decide how to persist your file configurations:

FieldDefinition fields:
- field_name - str - required -  the name of the field in the result set
- start_position - int - required for fixed width files - the start position of the field in its row
- field_length - int - required for fixed width files - the length of the field
- xml_node_name - str - required for xml files - the xml node containing the data

FileDefinition fields:
- file_type - str - required - the type of the file.  DELIMITED, FIXED, and XML are currently supported
- field_definitions - List[FieldDefintion] - required - list of FieldDefinition objects to define data fields
- has_header - bool - optional - whether the file has a header row to skip or not
- delimiter - str - required for DELIMITED files - character or string of characters that delimit fields
- record_element_name - str - required for xml files - name of the xml node that represents a full record
- file_mask - str - required for finding files - a glob pattern to be used in matching file names for look up
- input_directory - str - required for finding files - the absolute path where the files reside
- completed_directory - str - optional - the absolute path to move files to once they are ripped


```python
from file_ripper import FieldDefinition, FileDefinition, file_constants as fc


def build_delimited_file_definition():
    field_definitions = [
        FieldDefinition('name'),
        FieldDefinition('age'),
        FieldDefinition('dob')
    ]
    
    return FileDefinition(fc.DELIMITED, field_definitions)


def build_fixed_file_definition():
    field_definitions = [
        FieldDefinition('name', start_position=0, field_length=20),
        FieldDefinition('age', start_position=20, field_length=5),
        FieldDefinition('dob', start_position=25, field_length=10)
    ]
    
    return FileDefinition(fc.FIXED, field_definitions)


def build_xml_file_definition():
    field_definitions = [
        FieldDefinition('name', xml_node_name='name'),
        FieldDefinition('age', xml_node_name='age'),
        FieldDefinition('dob', xml_node_name='dateOfBirth')
    ]

    return FileDefinition(fc.FIXED, field_definitions)

```


## Ripping Files

file-ripper provides easy access to your file data.  The rip_file function takes a file-like object and a FileDefinition.  It returns a tuple containing your file's name and your records as a list of dicts
 

```python
from file_ripper import rip_file, FileDefinition, FieldDefinition, file_constants as fc

field_definitions = [
    FieldDefinition('name'),
    FieldDefinition('age'),
    FieldDefinition('dob')
]
    
file_definition = FileDefinition(fc.DELIMITED, field_definitions)
with open('path/to/file.txt', 'r') as file:
    file_name, file_records = rip_file(file, file_definition)    
```

The FileRipper class also supports ripping multiple files using the rip_files function.

```python
from file_ripper import rip_files, FileDefinition, FieldDefinition, file_constants as fc
from typing import List, Tuple

field_definitions = [
    FieldDefinition('name'),
    FieldDefinition('age'),
    FieldDefinition('dob')
]
    
file_definition = FileDefinition(fc.DELIMITED, field_definitions)
with open('path/to/file.txt', 'r') as file:
    file_results: List[Tuple[str, list]] = rip_files([file], file_definition) 
```

## Finding And Ripping Files
This is a new feature for version 1.1.0 of file-ripper.  It now supports finding and ripping your files based on
a provided file mask (using glob pattern matching) and an input directory.  An optional completed directory can be specified
if you wish for the file to be moved after they are ripped.

In the following example, any file in /usr/bin matching whose name matches the glob pattern 
Valid-*.txt will be ripped and have its data added to the result set. Those files will then be moved to 
/usr/bin/completed so that they will not be ripped if that directory is processed a second time

```python
from file_ripper import find_and_rip_files, FileDefinition, FieldDefinition, file_constants as fc
from typing import List, Tuple

field_definitions = [
    FieldDefinition('name'),
    FieldDefinition('age'),
    FieldDefinition('dob')
]
    
file_definition = FileDefinition(fc.DELIMITED, field_definitions, file_mask='Valid-*.txt', input_directory='/usr/bin',
                                 completed_directory='/usr/bin/completed')
file_results: List[Tuple[str, dict]] = find_and_rip_files(file_definition)
``` 