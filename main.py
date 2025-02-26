import os
import time
import shutil
import fnmatch
import boto3
import psycopg2
import pandas as pd
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer

# Load configuration from JSON file
with open("config.json", 'r') as config_file:
    config = json.load(config_file)

# Configuration
DIRECTORIES_TO_WATCH = [config['flows']['demoFlow_1']['sourceDirectory']]
FILE_NAME_PATTERN = config['flows']['demoFlow_1']['pattern']
DATABASE_CONFIG = {
    'dbname': config['shared']['dmDevDatabase']['url'].split('/')[-1],
    'user': config['shared']['dmDevDatabase']['username'],
    'password': os.getenv('DB_PASSWORD'),
    'host': config['shared']['dmDevDatabase']['url'].split('//')[1].split('/')[0],
    'port': '5432'
}
KAFKA_TOPIC = "env.delivery-manager"
KAFKA_SERVER = os.getenv('KAFKA_SERVER')
ARCHIVE_DIR = config['flows']['demoFlow_1']['archiveDirectory']

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
                import_to_database(file_path)
                send_kafka_notification(file_path)
                move_file(file_path)

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

def import_to_database(file_path):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    df = pd.read_csv(file_path)
    df.to_sql('flow_demo', conn, if_exists='append', index=False)
    conn.close()

def send_kafka_notification(file_path):
    with open(file_path, 'r') as file:
        producer.send(KAFKA_TOPIC, key=b'file_flow_complete', value=file.read().encode())
    producer.flush()

def move_file(file_path):
    shutil.move(file_path, os.path.join(ARCHIVE_DIR, os.path.basename(file_path)))

if __name__ == '__main__':
    watcher = Watcher(DIRECTORIES_TO_WATCH)
    watcher.run()
