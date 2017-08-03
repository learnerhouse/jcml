# -*- coding: utf-8 -*-

from ml.preprocess.modeling import modeling
import jc.models as models
import copy
import threading

class process_unit:

    tableName = ''
    sql = ''
    data_unit_size = 2000
    unit_num = 1
    modelings = []
    threads = []
    data_set = []

    def __init__(self,modeling):
        self.maxIdSql = "select id , max(id) as maxId from " + modeling.tableName
        self.minIdSql = "select id , min(id) as minId from " + modeling.tableName
        self.maxId = int(models.VisitRecord.objects.raw(self.maxIdSql)[0].maxId)
        self.minId = int(models.VisitRecord.objects.raw(self.minIdSql)[0].minId)
        self.unit_num = (self.maxId - self.minId)/self.data_unit_size + 1
        self.modeling = modeling

    def run(self):
        start = self.minId ; end = self.maxId
        for i in range(self.minId ,self.maxId ,self.data_unit_size):
            start = i; end = i + self.data_unit_size
            sql = "select "+ \
                  self.modeling.fieldstr + \
                  " from " + self.modeling.tableName +" " +\
            self.modeling.where + " and "+ "id < " + str(end) + " and id > "+ str(start)+" "+ \
            self.modeling.show_format
            self.modeling.sql = sql
            self.modeling.retMatrix = []
            md = copy.copy(self.modeling)
            self.modelings.append(md)
            t = threading.Thread(target=md.getDataSet,args=())
            self.threads.append(t)
            t.setDaemon(True)
            t.start()

    def get_data_set(self):
        for md in self.modelings:
            self.data_set.extend(md.retMatrix)
        return self.data_set


