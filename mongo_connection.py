from datetime import datetime
import functools
import logging

import pymongo
import os

import sql_queries
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

    def top_three(self):
        return self.parameters_collection.aggregate(sql_queries.MongoQueries.TOP_PIPLINES)

def load_decorator(func):
    """
    Decorator that saves the SQL query and params from the function's argument to a mongodb.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        inputs = dict()
        inputs['params'] = kwargs.get('params') or (args[2] if len(args)>2 else None)
        query = kwargs.get('query') or (args[1] if args else None)
        if query:
            query = SQLToJSON(query).to_json()
            query['creation_timestamp'] = datetime.now().isoformat()
            MongoService().queries_collection.insert_one(query)
            logging.info(f"Query {query} loaded.")
        else:
            print("No query found in the function arguments.")
        if inputs['params']:
            inputs['creation_time'] = datetime.now()
            MongoService().parameters_collection.insert_one(inputs)
        return func(*args, **kwargs)
    return wrapper
