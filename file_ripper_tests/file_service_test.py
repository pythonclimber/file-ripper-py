import os
import unittest
from unittest import TestCase

import file_ripper.fileconstants as fc
from file_ripper.filedefinition import FileDefinition, FieldDefinition
from file_ripper.fileservice import XmlFileService, DelimitedFileService, FixedFileService, FileService


class CreateFileServiceTests(TestCase):
    """Test cases for file service factory function code"""
    def test_xml_file_definition(self):
        """Create xml file service given and xml file definition"""
        file_definition = self.create_file_definition(fc.XML, record_element_name='record')
        file_service = FileService.create_file_service(file_definition)
        self.assertTrue(isinstance(file_service, XmlFileService))

    def test_delimited_file_definition(self):
        """Create delimited file service given a delimited file definition"""
        file_definition = self.create_file_definition(fc.DELIMITED, delimiter='\t')
        file_service = FileService.create_file_service(file_definition)
        self.assertTrue(isinstance(file_service, DelimitedFileService))

    def test_fixed_file_definition(self):
        """Create fixed file service given fixed file definition"""
        file_definition = self.create_file_definition(fc.FIXED, start_position=0, field_length=12)
        file_service = FileService.create_file_service(file_definition)
        self.assertTrue(isinstance(file_service, FixedFileService))

    def test_invalid_file_type(self):
        """Raise value error when invalid file type is created"""
        file_definition = self.create_file_definition('file_type')
        with self.assertRaises(ValueError):
            FileService.create_file_service(file_definition)

    @staticmethod
    def create_file_definition(file_type, delimiter=None, record_element_name=None, start_position=None,
                               field_length=None):
        field_definitions = [FieldDefinition('name', file_type, start_position=start_position, field_length=field_length)]
        return FileDefinition(file_type, field_definitions,
                              record_element_name=record_element_name,
                              delimiter=delimiter)


class FileServiceTests(unittest.TestCase):
    def create_file_definitions(self, file_type):
        self.file_name = None
        self.field_definitions = [
            FieldDefinition('name', file_type, 0, 13),
            FieldDefinition('age', file_type, 13, 9),
            FieldDefinition('dob', file_type, 22, 10)
        ]

    def assert_valid_file_output(self, output_file_name, file_records):
        self.assertEqual(self.file_name, output_file_name)
        self.assertTrue(isinstance(file_records, list))
        self.assertEqual(4, len(file_records))
        self.assert_valid_records(file_records)

    def assert_valid_records(self, file_records):
        self.assertEqual('Aaron', file_records[0]['name'])
        self.assertEqual('39', file_records[0]['age'])
        self.assertEqual('09/04/1980', file_records[0]['dob'])
        self.assertEqual('Gene', file_records[1]['name'])
        self.assertEqual('61', file_records[1]['age'])
        self.assertEqual('01/15/1958', file_records[1]['dob'])
        self.assertEqual('Xander', file_records[2]['name'])
        self.assertEqual('4', file_records[2]['age'])
        self.assertEqual('11/22/2014', file_records[2]['dob'])

    def test_process_records_not_implemented(self):
        file_service = FileService(FileDefinition(fc.FIXED, [FieldDefinition('hello', 'file_type')]))
        with self.assertRaises(NotImplementedError):
            file_service.process_file_records(file_service)

    def tearDown(self):
        try:
            if self.file_name:
                os.remove(self.file_name)
        except Exception as ex:
            print(ex)


class DelimitedFileServiceTests(FileServiceTests):
    def setUp(self):
        super().create_file_definitions(fc.DELIMITED)
        self.file_definition = FileDefinition(fc.DELIMITED, self.field_definitions, True, '|')
        self.file_service = DelimitedFileService(self.file_definition)
        self.file_name = 'Valid-delimited-09032019.txt'
        with open(self.file_name, 'w') as f:
            f.write('Name|Age|DOB\n')
            f.write('Aaron|39|09/04/1980\n')
            f.write('Gene|61|01/15/1958\n')
            f.write('Xander|4|11/22/2014\n')
            f.write('Mason|12|04/13/2007\n')

    def test_process_given_pipe_delimiter(self):
        with open(self.file_name, 'r') as file:
            file_instance = self.file_service.process(file)
            self.assert_valid_file_output(file_instance.file_name, file_instance.file_rows)

    def test_process_given_invalid_file(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.remove(self.file_definition.field_definitions[-1])
            with self.assertRaises(OSError):
                self.file_service.process(file)


class FixedFileServiceTests(FileServiceTests):
    def setUp(self):
        super(FixedFileServiceTests, self).create_file_definitions(fc.FIXED)
        self.file_definition = FileDefinition(fc.FIXED, self.field_definitions, True)
        self.file_service = FileService.create_file_service(self.file_definition)
        self.file_name = 'Valid-fixed-09032019.txt'
        with open(self.file_name, 'w') as f:
            f.write('Name         Age      DOB       \n')
            f.write('Aaron        39       09/04/1980\n')
            f.write('Gene         61       01/15/1958\n')
            f.write('Xander       4        11/22/2014\n')
            f.write('Mason        12       04/13/2007\n')

    def test_process(self):
        with open(self.file_name, 'r') as file:
            file_instance = self.file_service.process(file)
            self.assert_valid_file_output(file_instance.file_name, file_instance.file_rows)

    def test_process_invalid_file_records_too_short(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.append(
                FieldDefinition.create_from_dict(fc.FIXED, {
                    fc.FIELD_NAME: 'address',
                    fc.START_POSITION: 32,
                    fc.FIELD_LENGTH: 2
                }))
            self.assertRaises(IndexError, self.file_service.process, file)


class XmlFileServiceTests(FileServiceTests):
    def setUp(self):
        super(XmlFileServiceTests, self).create_file_definitions(fc.XML)
        self.file_definition = FileDefinition(fc.XML, self.field_definitions, record_element_name='person')
        self.file_service = XmlFileService(self.file_definition)
        self.file_name = 'Valid-xml-09032019.txt'
        with open(self.file_name, 'w') as f:
            self.file = f
            f.write('<people>\n')
            self.write_xml_record('Aaron', 39, '09/04/1980')
            self.write_xml_record('Gene', 61, '01/15/1958')
            self.write_xml_record('Xander', 4, '11/22/2014')
            self.write_xml_record('Mason', 12, '04/13/2007')
            f.write('</people>\n')

    def write_xml_record(self, name, age, dob):
        self.file.write('\t<person>\n')
        self.file.write(f'\t\t<name>{name}</name>\n')
        self.file.write(f'\t\t<age>{age}</age>\n')
        self.file.write(f'\t\t<dob>{dob}</dob>\n')
        self.file.write('\t</person>\n')

    def test_process(self):
        with open(self.file_name, 'r') as file:
            file_instance = self.file_service.process(file)
            self.assert_valid_file_output(file_instance.file_name, file_instance.file_rows)

    def test_process_given_invalid_file_missing_attribute(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.append(
                FieldDefinition.create_from_dict(fc.XML, {fc.FIELD_NAME: 'address'}))
            self.assertRaises(AttributeError, self.file_service.process, file)


if __name__ == '__main__':
    unittest.main()
