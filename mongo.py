import os
import json
import time
from pymongo import MongoClient


def database_insertion(json_file):

    with open(json_file) as f:
        database_input_file = json.load(f)

        cluster = MongoClient(f"mongodb+srv://a5pire:{os.environ['mongo']}@pairings-d8pll.gcp.mongodb.net/"
                              "test?retryWrites=true&w=majority")
        db = cluster['pairings']
        print()
        rp = db[input('Please enter database collection name (rpXX_20XX): ')]

        print(f'Inserting documents....')

        start = time.perf_counter()
        rp.insert_many(database_input_file)
        end = time.perf_counter()

        print(f'Completed in {round((end - start), 4)} seconds')
