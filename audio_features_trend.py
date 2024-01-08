from pymongo import MongoClient
import pandas as pd
import logging 
import os

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection(host='localhost', port=27017, db_name = "saved_tracks"):

    try:
        client = MongoClient(host, port)
        return client[db_name]
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        raise

def retrieve_data(collection_name="saved_tracks", fields=["added_at","audio_features"]):

    try:
        db = get_db_connection()
        collection = db[collection_name]
        return list(collection.find({},{key:1 for key in fields}))
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")
        raise
def process_data(documents):
    
    data_for_df = []
    for document in documents:
        row = {'date_added': document['added_at']}
        row.update(document['audio_features'])
        data_for_df.append(row)
    return pd.DataFrame(data_for_df)

def save_to_csv(df, filename='audio_features.csv'):

    try:
        df.set_index('date_added', inplace=True)
        df.to_csv(filename)
        logging.info(f"Data saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
        raise

def main():
    try:
        documents = retrieve_data()
        df = process_data(documents)
        save_to_csv(df)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
client = MongoClient('localhost',27017)
db = client['saved_tracks']
collection = db['saved_tracks']

