from unittest import TestCase

import file_ripper.fileconstants as fc
from file_ripper.filedefinition import FileDefinition, FieldDefinition


class TestFieldDefinitionConstruction(TestCase):
    def test_field_name_blank(self):
        with self.assertRaises(ValueError):
            FieldDefinition('', fc.DELIMITED)

    def test_file_type_blank(self):
        with self.assertRaises(ValueError):
            FieldDefinition('name', '')

    def test_file_type_delimited_field_name_only(self):
        with self.assertRaises(ValueError):
            FieldDefinition('name', fc.DELIMITED)

    def test_file_type_fixed_without_start_position(self):
        with self.assertRaises(ValueError):
            FieldDefinition('name', fc.FIXED, start_position=None)

    def test_file_type_fixed_without_field_length(self):
        with self.assertRaises(ValueError):
            FieldDefinition('name', fc.FIXED, start_position=0, field_length=None)

    def test_file_type_xml_without_xml_node_name(self):
        field_definition = FieldDefinition('name', fc.XML, xml_node_name='')
        self.assertEqual('name', field_definition.xml_node_name)


class TestFieldDefinitionCreateFromDict(TestCase):
    def setUp(self) -> None:
        self.field_definition = FieldDefinition.create_from_dict(fc.XML, {
            fc.FIELD_NAME: 'age',
            fc.START_POSITION: 10,
            fc.FIELD_LENGTH: 5,
            fc.XML_NODE_NAME: 'personAge',
            fc.POSITION_IN_ROW: 0
        })

    def test_file_type_set(self):
        self.assertEqual('XML', self.field_definition.file_type)

    def test_field_name_set(self):
        self.assertEqual('age', self.field_definition.field_name)

    def test_start_position_set(self):
        self.assertEqual(10, self.field_definition.start_position)

    def test_field_length_set(self):
        self.assertEqual(5, self.field_definition.field_length)

    def test_xml_node_name_set(self):
        self.assertEqual('personAge', self.field_definition.xml_node_name)


class TestFileDefinitionConstruction(TestCase):
    def setUp(self) -> None:
        self.field_definition = FieldDefinition('dob', 'XML')
        self.file_definition = FileDefinition('XML', [self.field_definition], has_header=True,
                                              delimiter='|', record_element_name='person',
                                              input_directory='input', completed_directory='completed',
                                              file_mask='mask')

    def test_file_type_and_field_definitions(self):
        self.assertEqual('XML', self.file_definition.file_type)
        self.assertTrue(len(self.file_definition.field_definitions) == 1)
        self.assertEqual(self.field_definition, self.file_definition.field_definitions[0])

    def test_has_header(self):
        self.assertTrue(self.file_definition.has_header)

    def test_delimiter(self):
        self.assertEqual('|', self.file_definition.delimiter)

    def test_record_element_name(self):
        self.assertEqual('person', self.file_definition.record_element_name)

    def test_input_directory(self):
        self.assertEqual('input', self.file_definition.input_directory)

    def test_completed_directory(self):
        self.assertEqual('completed', self.file_definition.completed_directory)

    def test_file_mask(self):
        self.assertEqual('mask', self.file_definition.file_mask)

    def test_file_type_missing(self):
        with self.assertRaises(ValueError):
            FileDefinition('', [self.file_definition])

    def test_file_definitions_missing(self):
        with self.assertRaises(ValueError):
            FileDefinition('XML', [])

    def test_delimited_file_delimiter_missing(self):
        with self.assertRaises(ValueError):
            FileDefinition(fc.DELIMITED, [self.field_definition], delimiter='')

    def test_xml_file_record_element_name_missing(self):
        with self.assertRaises(ValueError):
            FileDefinition(fc.XML, [self.field_definition], record_element_name='')


class TestFileDefinitionCreateDelimitedFromDict(TestCase):
    def setUp(self) -> None:
        self.file_definition = FileDefinition.create_from_dict({
            fc.FILE_TYPE: fc.DELIMITED,
            fc.DELIMITER: ',',
            fc.RECORD_ELEMENT_NAME: 'record',
            fc.HAS_HEADER: True,
            fc.INPUT_DIRECTORY: 'input',
            fc.COMPLETED_DIRECTORY: 'completed',
            fc.FILE_MASK: 'mask',
            fc.FIELD_DEFINITIONS: [{
                fc.FIELD_NAME: 'name',
                fc.POSITION_IN_ROW: 0
            }]
        })

    def test_file_type(self):
        self.assertEqual(fc.DELIMITED, self.file_definition.file_type)

    def test_delimiter(self):
        self.assertEqual(',', self.file_definition.delimiter)

    def test_record_element_name(self):
        self.assertEqual('record', self.file_definition.record_element_name)

    def test_has_header(self):
        self.assertTrue(self.file_definition.has_header)

    def test_input_directory(self):
        self.assertEqual('input', self.file_definition.input_directory)

    def test_completed_directory(self):
        self.assertEqual('completed', self.file_definition.completed_directory)

    def test_file_mask(self):
        self.assertEqual('mask', self.file_definition.file_mask)

    def test_field_definitions(self):
        self.assertTrue(len(self.file_definition.field_definitions) == 1)
