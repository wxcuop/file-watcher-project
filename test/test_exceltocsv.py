import unittest
import tempfile
from unittest.mock import MagicMock

class ExcelToCsvTest(unittest.TestCase):
    
    def test_convert(self):
        r = MagicMock()
        r.get_file.return_value = "Book1.xlsx"
        
        with tempfile.NamedTemporaryFile(suffix='zzz', delete=True) as tmp:
            try:
                ExcelToCsv.convert(r.get_file(), tmp.name)
            except Exception as e:
                self.fail(f"convert() raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
