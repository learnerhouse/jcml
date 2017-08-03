# -*- coding: utf-8 -*-

class data_flow:

    tatol_element = 0
    history_data = {}
    local_data= {}
    key = None
    value = None
    row = 0
    is_continue = True
    length = 3
    colume_num = 0
    index = 0
    is_row_equal_length = False
    is_row_change = False


    def clear(self):
        self.tatol_element = 0
        self.history_data = {}
        self.key = None
        self.value = None
        self.row = 0
        self.is_continue = True
        self.length = 0
        self.colume_num = 0
        self.index = 0

    def add_history_data(self,key,val):
        if key != None:
            if key in self.history_data:
               self.is_row_change = False
               if self.index % self.colume_num ==0:
                   self.row +=1
                   if self.is_row_equal_length:
                       self.row = self.length
                   self.get_local_data()
                   self.is_row_change = True

               self.history_data[key].append(val)
               self.index += 1
            else:
                self.history_data[key] = []
                self.local_data[key] = []
                self.local_data[key].append(val)
                self.history_data[key].append(val)
                self.colume_num +=1

    def set(self,key,val):
        self.key = key
        self.value = val
        
    def set_history_data_length(self,length):
        self.length = length

    def get_local_data(self):
        for key in self.history_data:
            self.local_data[key] = self.history_data[key][self.row-self.length:self.row]

    def set_all_history2local(self,bool):
        self.is_row_equal_length = bool






