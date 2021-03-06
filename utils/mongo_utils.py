#!/usr/bin/env python
"""
Mongo interface
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

class Mongo(object):
    """
    Mongo interface
    """
    def __init__(self, address='localhost', port=27017, database='rackhd'):
        self.db_name = database
        self.client = MongoClient(address, port)
        self.db = self.client[database]
        self.collections = self.db.collection_names(include_system_collections=False)

    def find_collection_by_id(self, mongo_id):
        """
        Find operator by id
        """
        for collect in self.collections:
            doc = self.db[collect].find_one({'_id': ObjectId(mongo_id)})
            if doc:
                return collect
        raise Exception('Mong id {} is invalid'.format(mongo_id))

    def find_doc_by_id(self, mongo_id):
        """
        Find operator by id
        """
        for collect in self.collections:
            doc = self.db[collect].find_one({'_id': ObjectId(mongo_id)})
            if doc:
                return dumps(doc)
        raise Exception('Mong id {} is invalid'.format(mongo_id))

    def find_operator_by_id(self, mongo_id):
        """
        Find API operator by id
        """
        col_to_opr_map = {
            'workitems': 'pollers'
        }
        opr = self.find_collection_by_id(mongo_id)
        if opr in col_to_opr_map:
            opr = col_to_opr_map[opr]
        return opr

    def clear_rackhd_db(self):
        """
        Clear RackHD database
        """
        self.client.drop_database(self.db_name)

mongo = Mongo()
