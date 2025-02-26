import unittest
import tempfile
import shutil
from unittest.mock import MagicMock

class FileHelperTest(unittest.TestCase):
    
    def test_copy(self):
        r = MagicMock()
        r.get_file.return_value = "Book1.xlsx"
        tmp = tempfile.NamedTemporaryFile(delete=True)
        
        try:
            FileHelper.copy(r.get_file(), tempfile.gettempdir())
            FileHelper.copy(r.get_file(), None)
        except Exception as e:
            self.fail(f"copy() raised an exception {e}")
    
    def test_move(self):
        r = MagicMock()
        r.get_file.return_value = "Book1.xlsx"
        tmp = tempfile.NamedTemporaryFile(delete=True)
        
        try:
            FileHelper.copy(r.get_file(), tempfile.gettempdir())
            FileHelper.move(tmp.name, "/dev/null")
            
            FileHelper.copy(r.get_file(), tempfile.gettempdir())
            FileHelper.move(tmp.name, None)
            
            FileHelper.copy(r.get_file(), tempfile.gettempdir())
            FileHelper.move(tmp.name, tempfile.gettempdir())
        except Exception as e:
            self.fail(f"move() raised an exception {e}")
    
    def test_rename(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=True) as r:
            try:
                FileHelper.rename(r.name, "test1.xlsx")
            except Exception as e:
                self.fail(f"rename() raised an exception {e}")

if __name__ == '__main__':
    unittest.main()
