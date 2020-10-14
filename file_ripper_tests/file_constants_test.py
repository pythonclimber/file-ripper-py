from unittest import TestCase

import file_ripper.fileconstants as fc


class FileConstantsTests(TestCase):
    def test_file_type(self):
        self.assertEqual(fc.FILE_TYPE, 'file_type')

    def test_file_mask(self):
        self.assertEqual(fc.FILE_MASK, 'file_mask')

    def test_delimited(self):
        self.assertEqual(fc.DELIMITED, 'DELIMITED')

    def test_fixed(self):
        self.assertEqual(fc.FIXED, 'FIXED')

    def test_xml(self):
        self.assertEqual(fc.XML, 'XML')

    def test_delimiter(self):
        self.assertEqual(fc.DELIMITER, 'delimiter')

    def test_has_header(self):
        self.assertEqual(fc.HAS_HEADER, 'has_header')

    def test_field_definitions(self):
        self.assertEqual(fc.FIELD_DEFINITIONS, 'field_definitions')

    def test_field_name(self):
        self.assertEqual(fc.FIELD_NAME, 'field_name')

    def test_start_position(self):
        self.assertEqual(fc.START_POSITION, 'start_position')

    def test_field_length(self):
        self.assertEqual(fc.FIELD_LENGTH, 'field_length')

    def test_record_element_name(self):
        self.assertEqual(fc.RECORD_ELEMENT_NAME, 'record_element_name')

    def test_xml_node_name(self):
        self.assertEqual(fc.XML_NODE_NAME, 'xml_node_name')

    def test_input_directory(self):
        self.assertEqual(fc.INPUT_DIRECTORY, 'input_directory')

    def test_completed_directory(self):
        self.assertEqual(fc.COMPLETED_DIRECTORY, 'completed_directory')
