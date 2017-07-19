# --*-- coding=utf-8 --*--
from pymongo import MongoClient

#从mongodb中取数据
conn = MongoClient("127.0.0.1", 27017)
db = conn["jcml"]

data_set = db["jcml"]
print data_set.find()[0]['data']
