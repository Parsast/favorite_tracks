import json
import logging
from pymongo import MongoClient
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection(uri, db_name):
    
    client = MongoClient(uri)
    return client[db_name]

def load_data_from_file(file_path):
    
    with open(file_path, 'r') as file:
        return json.load(file)

def insert_data_into_collection(collection, data):
   
    collection.insert_many(data)

def main():
    uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
<<<<<<< HEAD
    db_name = 'saved_tracks_progress'
    collection_name = 'saved_tracks_progress'
    file_path = 'saved_tracks_progress.json'
=======
    db_name = 'saved_tracks'
    collection_name = 'saved_tracks'
    file_path = 'saved_tracks.json'
>>>>>>> origin/main

    db = get_db_connection(uri, db_name)
    collection = db[collection_name]
    
    try:
        tracks = load_data_from_file(file_path)
        insert_data_into_collection(collection, tracks)
        logging.info("Data imported successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
