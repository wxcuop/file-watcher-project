import unittest
from unittest.mock import MagicMock
import json
import tempfile
from urllib.parse import urlparse

class JsonHelperTest(unittest.TestCase):
    
    def setUp(self):
        self.json_helper = MagicMock()
        self.s3_helper = MagicMock()
        self.s3_client = MagicMock()
        self.s3_utilities = MagicMock()
        
    def test_to_json(self):
        flow = MagicMock()
        entry = ("zz", flow)
        h = {"batchId": "batchId", "size": 0}
        
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            self.json_helper.to_json(h, tmp.name, entry)
            
    def test_to_json_s3(self):
        flow = MagicMock()
        s3 = MagicMock()
        s3.name = "test"
        s3.directory = "/tmp"
        
        self.s3_helper.get_s3_key.return_value = "test"
        self.s3_helper.get_s3_path.return_value = "s3//test/test.txt"
        self.s3_helper.get_s3.return_value = self.s3_client
        self.s3_client.utilities.return_value = self.s3_utilities
        self.s3_utilities.get_url.return_value = urlparse("https://abc")
        
        entry = ("zz", flow)
        h = {"batchId": "batchId", "size": 0}
        
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            self.json_helper.to_json(h, tmp.name, entry)

if __name__ == '__main__':
    unittest.main()
