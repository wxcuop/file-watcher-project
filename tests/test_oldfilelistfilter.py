import unittest
from unittest.mock import MagicMock
import os
from datetime import timedelta

class OldFileListFilterTest(unittest.TestCase):
    
    def setUp(self):
        self.mock_consumer = MagicMock()
        self.file_filter = OldFileListFilter(86400)
        self.file_filter.set_age(timedelta(seconds=86400))
        self.file_filter.add_discard_callback(self.mock_consumer)

    def test_filter_files(self):
        files = [
            "file1.txt",
            "file2.txt",
            "file3.txt"
        ]

        filtered_files = self.file_filter.filter_files(files)

        self.mock_consumer.assert_any_call("file1.txt")
        self.mock_consumer.assert_any_call("file2.txt")
        self.mock_consumer.assert_any_call("file3.txt")

        self.assertEqual(len(filtered_files), 0)

    def test_accept(self):
        file = "test.txt"
        result = self.file_filter.accept(file)

        self.mock_consumer.assert_called_with(file)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
