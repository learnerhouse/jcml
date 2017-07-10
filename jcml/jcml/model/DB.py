from pymongo import MongoClient


#从mongodb中取数据
conn = MongoClient('127.0.0.1', 27017);db = conn['jsml']; data_set = db["jsml"]