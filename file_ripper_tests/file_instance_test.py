from unittest import TestCase

from file_ripper.fileinstance import FileRow, FileInstance


class TestFileRowConstruction(TestCase):
    def test_empty_dict(self):
        file_row = FileRow({})
        self.assertTrue(len(file_row.fields) == 0)

    def test_non_empty_dict(self):
        file_row = FileRow({'key': 'value'})
        self.assertTrue(len(file_row.fields) == 1)
        self.assertEqual('value', file_row.fields['key'])

    def test_none(self):
        file_row = FileRow(None)
        self.assertTrue(file_row.fields is None)


class TestFileRowContainerProtocol(TestCase):
    def setUp(self) -> None:
        self.file_row = FileRow({'name': 'Aaron', 'age': '26'})

    def test_positive_contained(self):
        self.assertTrue('name' in self.file_row)

    def test_negative_contained(self):
        self.assertFalse('dob' in self.file_row)

    def test_positive_not_contained(self):
        self.assertTrue('addr' not in self.file_row)

    def test_negative_not_contained(self):
        self.assertFalse('age' not in self.file_row)


class TestFileRowSizedProtocol(TestCase):
    def test_zero(self):
        row = FileRow({})
        self.assertEqual(0, len(row))

    def test_one(self):
        row = FileRow({'key': 'value'})
        self.assertEqual(1, len(row))

    def test_five(self):
        row = FileRow({'key1': 'value', 'key2': 'value', 'key3': 'value', 'key4': 'value', 'key5': 'value'})
        self.assertEqual(5, len(row))


class TestFileRowIterableProtocol(TestCase):
    def setUp(self) -> None:
        self.row = FileRow({'name': 'Xander', 'age': '6', 'dob': '11/22/63'})

    def test_iter(self):
        i = iter(self.row)
        self.assertEqual('name', next(i))
        self.assertEqual('age', next(i))
        self.assertEqual('dob', next(i))
        with self.assertRaises(StopIteration):
            next(i)

    def test_for_loop(self):
        expected = ['name', 'age', 'dob']
        index = 0
        for i in self.row:
            self.assertEqual(expected[index], i)
            index += 1


class TestFileRowSequenceProtocol(TestCase):
    def setUp(self) -> None:
        self.row = FileRow({'name': 'Xander', 'age': '6', 'addr': '123 Main St', 'dob': '11/22/63'})

    def test_indexing(self):
        self.assertEqual('Xander', self.row['name'])
        self.assertEqual('6', self.row['age'])
        self.assertEqual('123 Main St', self.row['addr'])
        self.assertEqual('11/22/63', self.row['dob'])

    def test_slicing(self):
        with self.assertRaises(TypeError):
            fields = self.row['name':'age']

    def test_reversing(self):
        with self.assertRaises(TypeError):
            reversed(self.row)


class TestFileInstanceConstruction(TestCase):
    def test_file_name_and_file_rows(self):
        file_row = FileRow({'name': 'John'})
        file_instance = FileInstance('file_name', [file_row])
        self.assertEqual('file_name', file_instance.file_name)
        self.assertTrue(len(file_instance.file_rows) == 1)
        self.assertEqual([file_row], file_instance.file_rows)

    def test_file_name_missing(self):
        with self.assertRaises(TypeError):
            FileInstance(file_rows=[])

    def test_file_rows_missing(self):
        with self.assertRaises(TypeError):
            FileInstance(file_name='file_name')


class TestFileInstanceContainerProtocol(TestCase):
    def setUp(self) -> None:
        self.file_row = FileRow({'name': 'Alex', 'age': '27'})
        self.file_instance = FileInstance('file_name', [self.file_row])

    def test_positive_contains(self):
        self.assertTrue(self.file_row in self.file_instance)

    def test_negative_contains(self):
        self.assertFalse(FileRow({'name': 'Jeff'}) in self.file_instance)

    def test_negative_not_contains(self):
        self.assertFalse(self.file_row not in self.file_instance)

    def test_positive_not_contains(self):
        self.assertTrue(FileRow({'name': 'Jeff'}) not in self.file_instance)


class TestFileInstanceSizedProtocol(TestCase):
    def test_zero(self):
        self.assertTrue(len(FileInstance('', [])) == 0)

    def test_one(self):
        file_row = FileRow({})
        self.assertTrue(len(FileInstance('', [file_row])) == 1)

    def test_five(self):
        file_rows = [FileRow({}), FileRow({}), FileRow({}), FileRow({}), FileRow({})]
        self.assertTrue(len(FileInstance('', file_rows)) == 5)


class TestFileInstanceIterableProtocol(TestCase):
    def setUp(self) -> None:
        self.file_rows = [FileRow({'name': 'Aaron'}), FileRow({'age': '40'}), FileRow({'dob': '06/12/1980'})]
        self.file_instance = FileInstance('file_name', self.file_rows)

    def test_iter(self):
        i = iter(self.file_instance)
        self.assertEqual(self.file_rows[0], next(i))
        self.assertEqual(self.file_rows[1], next(i))
        self.assertEqual(self.file_rows[2], next(i))
        with self.assertRaises(StopIteration):
            next(i)

    def test_for_loop(self):
        index = 0
        for row in self.file_instance:
            self.assertEqual(self.file_rows[index], row)
            index += 1


class TestFileInstanceSequenceProtocol(TestCase):
    def setUp(self) -> None:
        self.file_rows = [FileRow({'name': 'John'}), FileRow({'name': 'Joe'}), FileRow({'name': 'Jeff'}),
                          FileRow({'name': 'Adam'}), FileRow({'name': 'Alex'}), FileRow({'name': 'Steve'})]
        self.file_instance = FileInstance('', self.file_rows)

    def test_indexing(self):
        self.assertEqual(self.file_rows[1], self.file_instance[1])

    def test_slicing_beginning(self):
        self.assertEqual(self.file_rows[:2], self.file_instance[:2])

    def test_slicing_end(self):
        self.assertEqual(self.file_rows[4:], self.file_instance[4:])

    def test_slicing_middle(self):
        self.assertEqual(self.file_rows[2:4], self.file_instance[2:4])

    def test_reversed(self):
        expected = reversed(self.file_rows)
        rev = reversed(self.file_instance)
        self.assertEqual(next(expected), next(rev))
        self.assertEqual(next(expected), next(rev))
        self.assertEqual(next(expected), next(rev))
        self.assertEqual(next(expected), next(rev))
        self.assertEqual(next(expected), next(rev))
        self.assertEqual(next(expected), next(rev))
        with self.assertRaises(StopIteration):
            next(rev)


class TestFileInstanceEquality(TestCase):
    def setUp(self) -> None:
        self.file_name = 'file_name'
        self.file_rows = [FileRow({'name': 'Dominic'}), FileRow({'age': '44', 'dob': '11/11/1977'})]

    def test_are_equal(self):
        self.assertTrue(FileInstance(self.file_name, self.file_rows) == FileInstance(self.file_name, self.file_rows))

    def test_different_file_names(self):
        self.assertFalse(FileInstance(self.file_name + '1', self.file_rows) == FileInstance(self.file_name + '2', self.file_rows))

    def test_different_file_rows(self):
        self.assertFalse(FileInstance(self.file_name, self.file_rows) == FileInstance(self.file_name, [FileRow({})]))
