# -*- coding: utf-8 -*-
import ml.models as model
from ml.preprocess.data_flow  import data_flow
from ml.preprocess.mining import mining
from ml.preprocess.data_clean import data_clean
import jc.models as models

class modeling:

    mining_func = None
    fieldPreProcess = None
    sql = ''
    retMatrix = []
    def __init__(self,selectFields,tableName,where,show_format):
        fieldstr = ''
        for field in selectFields:
            fieldstr +=  field + ","
        self.tableName = tableName
        self.where = where
        self.show_format = show_format
        self.fieldstr = fieldstr[:-1]
        self.selectFields = selectFields
        self.data_flow = data_flow()
        self.dc = data_clean()
        self.set_fieldPreProcess_func(self.dc.removeIdField)  # 数据预处理
        self.mn = mining()
        self.set_mining_func()                                # 数据特征处理
        self.sql = "select "+ self.fieldstr +  " from "+ self.tableName + " "+ self.where+ self.show_format

    def getDataSet (self,fieldNames=None):
        self.dataSet = list(models.VisitRecord.objects.raw( self.sql ))
        row = []
        if fieldNames == None:
            fieldNames = self.selectFields
        for obj in self.dataSet:
            for field in fieldNames:
                if hasattr(obj,field):
                    if self.fieldPreProcess == None:

                        self.data_flow.add_history_colume(field,getattr(obj,field))
                        self.data_flow.set(field,getattr(obj,field))
                        self.data_flow = self.mining_func(
                            self.data_flow
                        )
                        row.append(self.data_flow.value)

                    elif self.fieldPreProcess(field,getattr(obj,field))!= None:

                        self.data_flow.add_history_colume(field,getattr(obj,field))
                        self.data_flow.set(field,getattr(obj,field))
                        self.data_flow = self.mining_func(
                            self.data_flow
                        )
                        row.append(self.data_flow.value)

            self.retMatrix.append(row)
            row = []
        return self.retMatrix,self.dataSet

    def defaultfieldPreProcess(self,key,value,last_value=None):
        if key in self.selectFields:  #
            pass   # function
            return key,value

    def set_mining_func(self,mining_func=None):

        if mining_func == None:
            self.mining_func = self.mn.get_feature
        else:
            self.mining_func = mining_func
        pass

    def set_fieldPreProcess_func(self,fieldPreProcess):
        self.fieldPreProcess = fieldPreProcess
        pass



