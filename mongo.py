import os
import json
import time
from pymongo import MongoClient
from dotenv import load_dotenv


def database_insertion(json_file):

    load_dotenv()   # initialises the environment variables from .env file

    with open(json_file) as f:
        database_input_file = json.load(f)  # loads json data into database input variable

        # connects to the mongodb server with user/pass
        cluster = MongoClient(f"mongodb+srv://{os.getenv('mongo_user')}:{os.getenv('mongo_pass')}"
                              f"@pairings-d8pll.gcp.mongodb.net/test?retryWrites=true&w=majority")

        db = cluster['pairings']    # selects pairings database from server
        print()
        rp = db[input('Please enter database collection name (rpXX_20XX): ')]   # creates a new collection name variable

        print(f'Inserting documents....')

        start = time.perf_counter()     # starts timing before inserting the documents to the database
        rp.insert_many(database_input_file)     # inserts new collection into database
        end = time.perf_counter()   # finishes timing on completion of the document insertion

        print(f'Completed in {round((end - start), 4)} seconds')
        print()
