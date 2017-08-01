# -*- coding: utf-8 -*-
import ml.models as model
class modeling:

    def __init__(self,model,selectFields,tableName,where):
        fieldstr = ''
        for field in selectFields:
            fieldstr +=  field + ","
        self.dataSet = list(model.objects.raw("select "+ fieldstr[:-1] + " from "+ tableName + " "+ where))
        self.selectFields = selectFields


    def getDataSet (self,fieldPreProcess=None,fieldNames=None):
        retMatrix = []
        row = []
        if fieldNames == None:
            fieldNames = self.selectFields
        for obj in self.dataSet:
            for field in fieldNames:
                if hasattr(obj,field):
                    if fieldPreProcess==None:
                        row.append(self.fieldPreProcess(field,getattr(obj,field)))
                    elif fieldPreProcess(field,getattr(obj,field))!= None:
                        row.append(fieldPreProcess(field,getattr(obj,field)))

            retMatrix.append(row)
            row = []
        return retMatrix,self.dataSet

    def fieldPreProcess(self,key,value):
        if key in self.selectFields:  #
            pass   # function
            return value





