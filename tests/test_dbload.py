import unittest
from unittest.mock import MagicMock, patch
import sqlite3
import tempfile
import os

class DBLoadTest(unittest.TestCase):
    
    @patch('sqlite3.connect')
    def test_load_microsoft(self, mock_connect):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        cursor.execute.return_value = 1
        connection.execute.return_value = cursor
        connection.get_server_version.return_value = "microsoft"
        mock_connect.return_value = connection
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as test_file:
            test_file_path = test_file.name
        
        try:
            load_config = {
                "url": "sqlite:///test.db",
                "username": "username",
                "password": "password",
                "table": "test_table",
                "column_headers": True,
                "run_reference_in_first_column": True
            }
            
            ctx = {"runReference": "12345"}
            self.load(test_file_path, load_config, "12345", {})
            
            connection.get_server_version.assert_called()
        finally:
            os.remove(test_file_path)
    
    @patch('sqlite3.connect')
    def test_load_filter_is_provided(self, mock_connect):
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        cursor.execute.return_value = 1
        connection.execute.return_value = cursor
        connection.get_server_version.return_value = "microsoft"
        mock_connect.return_value = connection
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as test_file:
            test_file_path = test_file.name
            self.write_to_file_with_headers(test_file_path)
        
        try:
            load_config = {
                "url": "sqlite:///test.db",
                "username": "username",
                "password": "password",
                "table": "test_table",
                "column_headers": True,
                "run_reference_in_first_column": True,
                "filter_column": "Column1",
                "filter_key": "1"
            }
            
            ctx = {"runReference": "12345"}
            result = self.filter_rows(test_file_path, load_config)
            
            self.assertEqual(2, self.count_lines(result))
        finally:
            os.remove(test_file_path)
    
    def write_to_file_with_headers(self, file_path):
        with open(file_path, 'w') as writer:
            writer.write("Column1,Column2\n")
            writer.write("1,Test\n")
            writer.write("2,Test2\n")
    
    def count_lines(self, file_path):
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)
    
    def filter_rows(self, file_path, config):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        header = lines[0]
        filtered_lines = [header] + [line for line in lines[1:] if line.startswith(config['filter_key'])]
        
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            temp_file.writelines(filtered_lines)
            return temp_file.name
    
    def load(self, file_path, config, reference, extra_config):
        print(f"Loading data from {file_path} into {config['table']} with reference {reference}")
        return True

if __name__ == '__main__':
    unittest.main()
