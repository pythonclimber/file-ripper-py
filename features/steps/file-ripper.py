from datetime import datetime
from typing import IO, List

from behave import given, when, then

from file_ripper import FieldDefinition, FileDefinition, rip_files, rip_file
from file_ripper import file_constants as fc

field_names = ['name', 'age', 'dob']


def assert_file_data(file_name: str, output_file_name: str, file_records: List[dict]):
    assert file_name == output_file_name
    assert 'Aaron' == file_records[0]['name']
    assert '39' == file_records[0]['age']
    assert '09/04/1980' == file_records[0]['dob']
    assert 'Gene' == file_records[1]['name']
    assert '61' == file_records[1]['age']
    assert '01/15/1958' == file_records[1]['dob']
    assert 'Xander' == file_records[2]['name']
    assert '5' == file_records[2]['age']
    assert '11/22/2014' == file_records[2]['dob']
    assert 'Mason' == file_records[3]['name']
    assert '12' == file_records[3]['age']
    assert '04/13/2007' == file_records[3]['dob']


def write_xml_record(file, name, age, dob):
    file.write('\t<person>\n')
    file.write(f'\t\t<name>{name}</name>\n')
    file.write(f'\t\t<age>{age}</age>\n')
    file.write(f'\t\t<dob>{dob}</dob>\n')
    file.write('\t</person>\n')


@given('a file whose fields are separated by a "{delimiter}"')
def step_impl(context, delimiter):
    with open(f'features/files/Valid-delimited-{datetime.now().strftime("%m%d%Y")}.txt', 'w+') as file:
        file.write(f'Name{delimiter}Age{delimiter}DOB\n')
        file.write(f'Aaron{delimiter}39{delimiter}09/04/1980\n')
        file.write(f'Gene{delimiter}61{delimiter}01/15/1958\n')
        file.write(f'Xander{delimiter}5{delimiter}11/22/2014\n')
        file.write(f'Mason{delimiter}12{delimiter}04/13/2007\n')
        context.file = file


@given('a delimited file definition with "{delimiter}"')
def step_impl(context, delimiter):
    field_definitions = [FieldDefinition(field_name) for field_name in field_names]
    context.file_definition = FileDefinition(fc.DELIMITED, field_definitions, delimiter=delimiter, has_header=True)


@given('a file whose fields are of fixed width')
def step_impl(context):
    with open(f'features/files/Valid-fixed-{datetime.now().strftime("%m%d%Y")}.txt', 'w+') as file:
        file.write('Aaron        39       09/04/1980\n')
        file.write('Gene         61       01/15/1958\n')
        file.write('Xander       5        11/22/2014\n')
        file.write('Mason        12       04/13/2007\n')
        context.file = file


@given('a fixed file definition')
def step_impl(context):
    start_positions = [0, 13, 22]
    field_lengths = [13, 9, 10]
    field_definitions = [FieldDefinition(field_names[i], start_positions[i], field_lengths[i])
                         for i in range(0, len(field_names))]
    context.file_definition = FileDefinition(fc.FIXED, field_definitions, has_header=False)


@given('a file in xml format')
def step_impl(context):
    with open(f'features/files/Valid-{datetime.now().strftime("%m%d%Y")}.xml', 'w+') as file:
        file.write('<people>\n')
        write_xml_record(file, 'Aaron', 39, '09/04/1980')
        write_xml_record(file, 'Gene', 61, '01/15/1958')
        write_xml_record(file, 'Xander', 5, '11/22/2014')
        write_xml_record(file, 'Mason', 12, '04/13/2007')
        file.write('</people>\n')
        context.file = file


@given('a xml file definition')
def step_impl(context):
    field_definitions = [FieldDefinition(field_name) for field_name in field_names]
    context.file_definition = FileDefinition(fc.XML, field_definitions)


@when('the file is ripped')
def step_impl(context):
    try:
        with open(context.file.name, 'r') as file:
            context.output_file_name, context.file_records = rip_file(file, context.file_definition)
    except Exception as ex:
        context.error = ex


@when('the files are ripped')
def step_impl(context):
    with open(context.file.name, 'r') as file:
        context.file_output_list = rip_files([file], context.file_definition)


@then('the file data is returned')
def step_impl(context):
    assert_file_data(context.file.name, context.output_file_name, context.file_records)


@then('data is returned for all files')
def step_impl(context):
    [assert_file_data(context.file.name, output_file_name, file_records)
     for output_file_name, file_records in context.file_output_list]


@then('a {error_name} occurs')
def step_impl(context, error_name):
    assert error_name == context.error.__class__.__name__
