import unittest
from unittest.mock import MagicMock

class DbExtractAndLoadUtilTest(unittest.TestCase):
    
    def test_execute(self):
        db_extract_and_load = MagicMock()
        db_extract = MagicMock()
        db_extract_and_load.set_db_extract(db_extract)
        
        db_extract.url = "sqlite:///:memory:"
        db_extract.sql = "SELECT 1"
        
        try:
            DbExtractAndLoadUtil.execute(db_extract_and_load, "r", {})
        except Exception as e:
            self.fail(f"execute() raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
