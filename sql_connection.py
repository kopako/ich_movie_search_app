from locale import normalize

import pymysql
import pymysql.cursors
from pymysql.connections import Connection
import logging
import os
from mongo_connection import load_decorator
from singleton import SingletonMeta


class SqlConnection(metaclass=SingletonMeta):
    def __init__(self):
        params = dict()
        params['host'] = os.getenv('sql_host')
        params['user'] = os.getenv('sql_user')
        params['password'] = os.getenv('sql_password')
        params['database'] = os.getenv('sql_database')
        params['charset'] = os.getenv('sql_charset')
        params['cursorclass'] = pymysql.cursors.DictCursor
        self.cnx: Connection = pymysql.connect(**params)
        self.cursor = self.cnx.cursor()

    def tear_down(self):
        self.cursor.close()
        self.cnx.close()

    @load_decorator
    def execute(self, query, *params):
        normalized_query = ' '.join(line.strip() for line in query.splitlines()).strip()
        logging.info('Query to execute: ',normalized_query)
        logging.info('Params: ',*params)
        self.cursor.execute(query, *params)