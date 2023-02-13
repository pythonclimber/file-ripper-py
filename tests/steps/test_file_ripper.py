import os
import shutil
from datetime import datetime
from types import SimpleNamespace
from typing import List, IO

from pytest_bdd import scenarios, given, when, then
from pytest_bdd.parsers import parse
from pytest import fixture

from file_ripper import FieldDefinition, FileDefinition, rip_file, rip_files, find_and_rip_files
from file_ripper import file_constants as fc
from file_ripper.fileinstance import FileRow, FileInstance

scenarios("../features/FileRipper.feature")
field_names = ['name', 'age', 'dob']


def before_scenario(context):
    if not os.path.exists('tests/files'):
        os.mkdir('tests/files')
    context.original_cwd = os.getcwd()
    file_path = os.path.join(os.getcwd(), 'tests/files')
    os.chdir(file_path)


def after_scenario(context):
    try:
        path_to_delete = os.getcwd()
        os.chdir(context.original_cwd)
        shutil.rmtree(path_to_delete)
    except Exception as ex:
        print(ex)


@fixture(autouse=True)
def configure_environment():
    context = SimpleNamespace()
    before_scenario(context)
    yield context
    after_scenario(context)


def assert_file_records(file_rows: List[FileRow]):
    assert len(file_rows[0]) == 3
    assert 'Aaron' == file_rows[0]['name']
    assert '39' == file_rows[0]['age']
    assert '09/04/1980' == file_rows[0]['dob']
    assert len(file_rows[1]) == 3
    assert 'Gene' == file_rows[1]['name']
    assert '61' == file_rows[1]['age']
    assert '01/15/1958' == file_rows[1]['dob']
    assert len(file_rows[2]) == 3
    assert 'Xander' == file_rows[2]['name']
    assert '5' == file_rows[2]['age']
    assert '11/22/2014' == file_rows[2]['dob']
    assert len(file_rows[3]) == 3
    assert 'Mason' == file_rows[3]['name']
    assert '12' == file_rows[3]['age']
    assert '04/13/2007' == file_rows[3]['dob']


def assert_file_from_list(file_name: str,  file_output_list: List[FileInstance]):
    file_instance = next(x for x in file_output_list if x.file_name.endswith(file_name))
    assert_file_records(file_instance.file_rows)


def create_fixed_file(file_name: str) -> IO:
    with open(file_name, 'w+') as file:
        file.write('Aaron        39       09/04/1980\n')
        file.write('Gene         61       01/15/1958\n')
        file.write('Xander       5        11/22/2014\n')
        file.write('Mason        12       04/13/2007\n')
        return file


def write_xml_record(file, name, age, dob):
    file.write('\t<person>\n')
    file.write(f'\t\t<name>{name}</name>\n')
    file.write(f'\t\t<age>{age}</age>\n')
    file.write(f'\t\t<dob>{dob}</dob>\n')
    file.write('\t</person>\n')


def publish_file_definition(file_definition: FileDefinition):
    with open('file.json', 'wt') as file:
        file.write(file_definition.to_json())


@given(parse("a file whose fields are separated by a {delimiter}"), target_fixture="context")
def step_impl(delimiter):
    context = SimpleNamespace()
    with open(f'Valid-delimited-{datetime.now().strftime("%m%d%Y")}.txt', 'w+') as file:
        file.write(f'Name{delimiter}DOB{delimiter}Age\n')
        file.write(f'Aaron{delimiter}09/04/1980{delimiter}39\n')
        file.write(f'Gene{delimiter}01/15/1958{delimiter}61\n')
        file.write(f'Xander{delimiter}11/22/2014{delimiter}5\n')
        file.write(f'Mason{delimiter}04/13/2007{delimiter}12\n')
        context.file = file
    return context


@given(parse("a delimited file definition with {delimiter}"), target_fixture="context")
def step_impl(delimiter, context):
    field_definitions = [
        FieldDefinition('age', 'DELIMITED', position_in_row=2),
        FieldDefinition('dob', 'DELIMITED', position_in_row=1),
        FieldDefinition('name', 'DELIMITED', position_in_row=0)
    ]
    context.file_definition = FileDefinition(fc.DELIMITED, field_definitions, delimiter=delimiter, has_header=True)
    publish_file_definition(context.file_definition)
    return context


@given('a file whose fields are of fixed width', target_fixture="context")
def step_impl():
    context = SimpleNamespace()
    context.file = create_fixed_file(f'Valid-fixed-{datetime.now().strftime("%m%d%Y")}.txt')
    return context


@given('a fixed file definition', target_fixture="context")
def step_impl(context):
    start_positions = [0, 13, 22]
    field_lengths = [13, 9, 10]
    field_definitions = [FieldDefinition(field_names[i], 'FIXED', start_positions[i], field_lengths[i])
                         for i in range(0, len(field_names))]
    context.file_definition = FileDefinition(fc.FIXED, field_definitions, has_header=False)
    return context


@given('a file in xml format', target_fixture="context")
def step_impl():
    context = SimpleNamespace()
    with open(f'Valid-{datetime.now().strftime("%m%d%Y")}.xml', 'w+') as file:
        file.write('<people>\n')
        write_xml_record(file, 'Aaron', 39, '09/04/1980')
        write_xml_record(file, 'Gene', 61, '01/15/1958')
        write_xml_record(file, 'Xander', 5, '11/22/2014')
        write_xml_record(file, 'Mason', 12, '04/13/2007')
        file.write('</people>\n')
        context.file = file
    return context


@given('a xml file definition', target_fixture="context")
def step_impl(context):
    field_definitions = [FieldDefinition(field_name, 'XML') for field_name in field_names]
    context.file_definition = FileDefinition(fc.XML, field_definitions, record_element_name='person')
    return context


@given('files stored on file system', target_fixture="context")
def step_impl():
    context = SimpleNamespace()
    context.files = [
        create_fixed_file(f'Valid-fixed-{datetime.now().strftime("%m%d%Y")}-1.txt'),
        create_fixed_file(f'Valid-fixed-{datetime.now().strftime("%m%d%Y")}-2.txt'),
        create_fixed_file(f'Valid-fixed-{datetime.now().strftime("%m%d%Y")}-3.txt'),
    ]
    return context


@given('file definition has input directory, file mask', target_fixture="context")
def step_impl(context):
    context.file_definition.input_directory = os.getcwd()
    context.file_definition.file_mask = 'Valid-fixed-*.txt'
    return context


@given('file definition has completed directory')
def step_impl(context):
    context.file_definition.completed_directory = f'{os.getcwd()}/completed'


@when("the file is ripped", target_fixture="context")
def step_impl(context):
    try:
        with open(context.file.name, 'r') as file:
            file_instance = rip_file(file, context.file_definition)
            context.output_file_name = file_instance.file_name
            context.file_records = file_instance.file_rows
    except Exception as ex:
        context.error = ex
    finally:
        return context


@when('the files are ripped', target_fixture="context")
def step_impl(context):
    context.file_names = [context.file.name]
    with open(context.file.name, 'r') as file:
        context.file_output_list = rip_files([file], context.file_definition)
    return context


@when('the files are found and ripped', target_fixture="context")
def step_impl(context):
    context.file_names = [file.name for file in context.files]
    context.file_output_list = find_and_rip_files(context.file_definition)
    return context


@then("the file data is returned")
def step_impl(context):
    assert context.file.name == context.output_file_name
    assert_file_records(context.file_records)


@then('data is returned for all files')
def step_impl(context):
    [assert_file_from_list(context.file_names[i], context.file_output_list)
     for i in range(0, len(context.file_names))]


@then(parse('a {error_name} occurs'))
def step_impl(error_name, context):
    assert error_name == context.error.__class__.__name__


@then('files are still in input directory')
def step_impl(context):
    for file_name in context.file_names:
        assert os.path.exists(f'{os.getcwd()}/{file_name}')


@then('files are in completed directory')
def step_impl(context):
    for file_name in context.file_names:
        assert not os.path.exists(f'{os.getcwd()}/{file_name}')
        assert os.path.exists(f'{context.file_definition.completed_directory}/{file_name}')
