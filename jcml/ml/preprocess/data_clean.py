# -*- coding: utf-8 -*-

# 有待进一步归纳

class data_clean:

    def __init__(self):
        pass


    def setleanFuncs(self,leanFuncs):
        pass


    def setkeys(self,keys):
        pass

    def clean(self):
        pass

    def removeIdField(self,key,value):
        if key == 'id':
            return None
        else:
            return value