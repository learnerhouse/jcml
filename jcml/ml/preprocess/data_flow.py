# -*- coding: utf-8 -*-

class data_flow:
    tatol_element = 0
    history_colume = {}
    history_table = []
    local_colume = {}
    key = None
    value = None
    row_num = 0
    is_continue = True
    length = 3
    colume_num = 0
    index = 0
    is_row_num_equal_length = False
    is_row_num_change = False
    row = []
    latest_row = []
    return_ans = []

    def clear(self):
        self.tatol_element = 0
        self.history_colume = {}
        self.key = None
        self.value = None
        self.row_num = 0
        self.is_continue = True
        self.length = 0
        self.colume_num = 0
        self.index = 1

    def add_history_colume(self, key, val):
        if key != None:
            self.index += 1
            if key in self.history_colume:
                self.is_row_num_change = False
                if self.row_num==0:
                    self.history_table.append(self.row)
                    self.latest_row = self.row
                    self.row = []
                    self.row_num += 1
                self.row.append(val)
                if self.index % self.colume_num == 0 :
                    self.history_table.append(self.row)
                    self.latest_row = self.row
                    self.row = []
                    self.row_num += 1
                    if self.is_row_num_equal_length:
                        self.row_num = self.length
                    self.get_local_colume()
                    self.is_row_num_change = True
                    self.index = 0

                self.history_colume[key].append(val)
            else:
                self.history_colume[key] = []
                self.local_colume[key] = []
                self.local_colume[key].append(val)
                self.history_colume[key].append(val)
                self.row.append(val)
                self.colume_num += 1


    def set(self, key, val):
        self.key = key
        self.value = val

    def set_history_colume_length(self, length):
        self.length = length

    def get_local_colume(self):
        for key in self.history_colume:
            self.local_colume[key] = self.history_colume[key][self.row_num - self.length:self.row_num]

    def set_all_history2local(self, bool):
        self.is_row_num_equal_length = bool
