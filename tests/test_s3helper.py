import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os
from pathlib import Path

class TestS3Helper(unittest.TestCase):
    
    def setUp(self):
        self.s3_helper = S3Helper()
        self.s3_client = MagicMock()
        self.s3_waiter = MagicMock()
        self.waiter_response = MagicMock()
        
        self.s3_helper.s3_client = self.s3_client
        
    def test_upload_directory(self):
        directory = self.s3_helper.get_upload_directory(self.get_test_s3_bucket())
        self.assertEqual("/tmp/", directory)

    def test_get_s3_bucket(self):
        s3_bucket = self.s3_helper.get_s3_bucket(self.get_test_s3_bucket())
        self.assertEqual("s3://test", s3_bucket)

    def test_s3_path(self):
        directory = self.s3_helper.get_s3_path(self.get_test_s3_bucket())
        self.assertEqual("s3://test//tmp/", directory)

    @patch("S3Helper.upload")
    def test_upload(self, mock_upload):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            file_path = Path(temp_file.name)
        
        self.s3_client.put_object.return_value = MagicMock()
        self.s3_client.waiter.return_value = self.s3_waiter
        self.s3_waiter.wait_until_object_exists.return_value = self.waiter_response
        
        flow = Flow()
        s3_bucket = self.get_test_s3_bucket()
        bucket_list = S3BucketList()
        bucket_list.set_s3_bucket(s3_bucket)
        flow.set_s3_bucket_list([bucket_list])
        
        self.s3_helper.upload(file_path, flow)
        self.s3_client.put_object.assert_called()
        
        os.remove(file_path)  # Clean up temp file
    
    def get_test_s3_bucket(self):
        s3 = S3Bucket()
        s3.set_name("test")
        s3.set_directory("/tmp")
        return s3

if __name__ == "__main__":
    unittest.main()
