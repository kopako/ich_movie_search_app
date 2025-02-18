from datetime import datetime
import functools
import logging

import pymongo
import os

from singleton import SingletonMeta
from sql_to_json import SQLToJSON


class MongoConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))

    def get_client(self):
        return self.client

class MongoService:
    db = MongoConnection().client[os.getenv("MONGO_DB")]
    queries_collection = db['film_queries']
    parameters_collection = db['film_queries_parameters']

    def list_collections(self):
        [print(collection) for collection in self.db.list_collection_names()]

    def save_query(self, query: str):
        document = SQLToJSON(query).to_json()
        self.queries_collection.insert_one(document)

def load_decorator(func):
    """
    Decorator that saves the SQL query from the function's argument to a mongodb.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the function's arguments
        inputs = dict()
        inputs['params'] = kwargs.get('params') or (args[2] if len(args)>2 else None)
        query = kwargs.get('query') or (args[1] if args else None)
        if query:
            MongoService().save_query(query)
            logging.info(f"Query {query} loaded.")
        else:
            print("No query found in the function arguments.")
        if inputs['params']:
            inputs['creation_time'] = datetime.now()
            MongoService().parameters_collection.insert_one(inputs)
        return func(*args, **kwargs)
    return wrapper
