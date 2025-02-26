import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os

class TestIntegrationFlow(unittest.TestCase):
    
    def setUp(self):
        self.delivery_setup_service = MagicMock()
        self.transaction_manager = MagicMock()
        self.s3_helper = MagicMock()
        self.flow_map = MagicMock()
        self.metadata_store = MagicMock()
        self.integration_flow_registration = MagicMock()
        self.registration_builder = MagicMock()
        self.integration_flow_context = MagicMock()
        
    @patch("builtins.open", new_callable=MagicMock)
    def test_integration_flow(self, mock_open):
        path = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
        path.close()
        
        mock_flow = MagicMock()
        s3bucket = MagicMock()
        s3bucket.name = "test"
        
        bucket_list = MagicMock()
        bucket_list.s3_bucket = s3bucket
        
        mock_flow.s3_bucket_list = [bucket_list]
        mock_flow.add_date_suffix = True
        mock_flow.source_directory = "source_directory_path"
        mock_flow.copy_directory = path.name
        mock_flow.copy_directories = ["/tmp"]
        
        self.flow_map.items.return_value = {"key": mock_flow}.items()
        self.integration_flow_context.registration.return_value = self.registration_builder
        self.registration_builder.register.return_value = self.integration_flow_registration
        
        self.delivery_setup_service.register_flows()
        
        self.integration_flow_context.registration.assert_called()
        
        os.unlink(path.name)  # Cleanup temporary file

if __name__ == "__main__":
    unittest.main()
