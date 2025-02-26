import unittest
import tempfile
import boto3
from moto import mock_s3
from kafka import KafkaProducer, KafkaConsumer
from unittest.mock import patch
from my_module import DeliverySetupService  # Replace with actual import

class TestDeliverySetupService(unittest.TestCase):
    @mock_s3
    @patch("my_module.KafkaProducer")
    def setUp(self, mock_kafka_producer):
        self.s3 = boto3.client("s3", region_name="us-east-1")
        self.s3.create_bucket(Bucket="test-bucket")
        self.delivery_setup_service = DeliverySetupService()
        self.mock_kafka_producer = mock_kafka_producer.return_value

    @mock_s3
    @patch("my_module.KafkaConsumer")
    def test_register_flows(self, mock_kafka_consumer):
        with tempfile.NamedTemporaryFile(delete=False) as test_file:
            test_file.write(b"test content")
            test_file_name = test_file.name

        message = {
            "fileName": test_file_name,
            "nbId": "123",
            "PlatformId": "platform123"
        }

        self.delivery_setup_service.trigger_integration_flow(message)
        self.mock_kafka_producer.send.assert_called()

if __name__ == "__main__":
    unittest.main()
