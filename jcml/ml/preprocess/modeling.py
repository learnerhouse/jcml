# -*- coding: utf-8 -*-
import ml.models as model
from ml.preprocess.data_flow  import data_flow
from ml.preprocess.mining import mining
from ml.preprocess.data_clean import data_clean
class modeling:

    last_last_value = None
    last_value = None
    last_last_key = None
    last_key = None
    retMatrix = []
    mining_func = None
    fieldPreProcess = None

    def __init__(self,model,selectFields,tableName,where,format):
        fieldstr = ''
        for field in selectFields:
            fieldstr +=  field + ","
        self.dataSet = list(model.objects.raw("select "+ fieldstr[:-1] + " from "+ tableName + " "+ where+format))
        self.selectFields = selectFields
        self.data_flow = data_flow()
        self.dc = data_clean()
        self.set_fieldPreProcess_func(self.dc.removeIdField)  # 数据预处理
        self.mn = mining()
        self.set_mining_func()                                # 数据特征处理



    def getDataSet (self,fieldNames=None):

        row = []
        if fieldNames == None:
            fieldNames = self.selectFields
        for obj in self.dataSet:
            for field in fieldNames:
                if hasattr(obj,field):
                    if self.fieldPreProcess == None:
                        self.data_flow.set(field,getattr(obj,field))
                        self.data_flow.set_a_n_minus_i(self.last_key,self.last_value,0)
                        self.data_flow.set_a_n_minus_i(self.last_last_key,self.last_last_value,1)
                        self.data_flow = self.mining_func(
                            self.data_flow
                        )
                        row.append(self.data_flow.value)
                        self.last_last_value = self.last_value
                        self.last_last_key = self.last_key
                        self.last_value = self.data_flow.value
                        self.last_key= self.data_flow.key
                    elif self.fieldPreProcess(field,getattr(obj,field))!= None:

                        self.data_flow.set(field,getattr(obj,field))
                        self.data_flow.set_a_n_minus_i(self.last_key,self.last_value,0)
                        self.data_flow.set_a_n_minus_i(self.last_last_key,self.last_last_value,1)
                        self.data_flow = self.mining_func(
                            self.data_flow
                        )
                        row.append(self.data_flow.value)
                        self.last_last_value = self.last_value
                        self.last_last_key = self.last_key
                        self.last_value = self.data_flow.value
                        self.last_key= self.data_flow.key

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



