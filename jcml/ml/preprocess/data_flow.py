# -*- coding: utf-8 -*-

class data_flow:

    tatol_element = 0
    a_n_minus_i = {}
    key = None
    value = None

    def clear(self):
        self.tatol_element = 0
        self.a_n_minus_i = {}
        self.key = None
        self.value = None

    def set_a_n_minus_i(self,key,val,i):
        if key != None:
            if key in self.a_n_minus_i:
                if len(self.a_n_minus_i[key]) < i+1:
                    self.a_n_minus_i[key].append(val)
                    self.tatol_element += 1
                else:
                    self.a_n_minus_i[key][i] = val
            else:
                self.a_n_minus_i[key] = []
                self.a_n_minus_i[key].append(val)
                self.tatol_element += 1


    def set(self,key,val):
        self.key = key
        self.value = val





