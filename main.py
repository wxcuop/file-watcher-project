import os
import time
import shutil
import fnmatch
import boto3
import psycopg2
import pyodbc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from lxml import etree
from kafka import KafkaProducer
import pandas as pd

# Configuration
DIRECTORIES_TO_WATCH = ["/path/to/dir1", "/path/to/dir2"]
FILE_NAME_PATTERN = "trades-*.csv"
XML_CONTENT_FILTER = "//portfolio[@id='XTANG_TST']"
DATABASE_CONFIG = {
    'dbname': 'your_db',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}
S3_BUCKET = "your_s3_bucket"
S3_REGION = "your_s3_region"
KAFKA_TOPIC = "your_kafka_topic"
KAFKA_SERVER = "your_kafka_server"
ARCHIVE_DIR = "/path/to/archive"
DELETE_DIR = "/dev/null"

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class Watcher:
    def __init__(self, directories_to_watch):
        self.observer = Observer()
        self.directories_to_watch = directories_to_watch

    def run(self):
        event_handler = Handler()
        for directory in self.directories_to_watch:
            self.observer.schedule(event_handler, directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def process(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created' or event.event_type == 'modified':
            file_path = event.src_path
            if fnmatch.fnmatch(file_path, FILE_NAME_PATTERN):
                if file_path.endswith('.csv') or file_path.endswith('.xlsx'):
                    import_to_database(file_path)
                    upload_to_s3(file_path)
                    archive_file(file_path)
                    delete_file(file_path)
                    send_kafka_notification(file_path)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

# Function to import CSV/XLSX to database
def import_to_database(file_path):
    # Truncate the table
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE your_table")
            conn.commit()

    # Import file content
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)

    df.to_sql('your_table', conn, if_exists='append', index=False)

# Function to upload file to S3
def upload_to_s3(file_path):
    s3_client = boto3.client('s3', region_name=S3_REGION)
    s3_client.upload_file(file_path, S3_BUCKET, os.path.basename(file_path))

# Function to archive file
def archive_file(file_path):
    shutil.move(file_path, os.path.join(ARCHIVE_DIR, os.path.basename(file_path)))

# Function to delete file
def delete_file(file_path):
    shutil.move(file_path, DELETE_DIR)

# Function to send Kafka notification
def send_kafka_notification(file_path):
    producer.send(KAFKA_TOPIC, key=b'file_flow_complete', value=file_path.encode())
    producer.flush()

if __name__ == '__main__':
    watcher = Watcher(DIRECTORIES_TO_WATCH)
    watcher.run()
