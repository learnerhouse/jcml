# --*-- coding=utf-8 --*--
# from pymongo import MongoClient
#
# #从mongodb中取数据
# conn = MongoClient("127.0.0.1", 27017)
# db = conn["jcml"]
#
# data_set = db["jcml"]

import json

class DB:

    def __init__(self):
       return

    def load(self,filepath):
            with open(filepath) as json_file:
                data = json.load(json_file)
                return data

    def loadData(self):
        return self.load("data.json")

