import unittest
from unittest.mock import MagicMock
from csv_data_formatter import CsvDataFormatter

class CsvDataFormatterTest(unittest.TestCase):
    def setUp(self):
        self.csvDataFormatter = CsvDataFormatter()

    def test_format_raw_cell_contents(self):
        self.assertIsNone(self.csvDataFormatter.format_raw_cell_contents(0.0, 0, "", True))
        self.assertIsNone(self.csvDataFormatter.format_raw_cell_contents(0.0, 0, "yyyy-MM-dd", True))
        self.assertIsNone(self.csvDataFormatter.format_raw_cell_contents(0.0, 0x0e, "yyyy-MM-dd", True))

if __name__ == '__main__':
    unittest.main()
