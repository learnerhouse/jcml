# -*- coding: utf-8 -*-

from ml.preprocess.mining import mining
from ml.preprocess.modeling import modeling
from ml.preprocess.data_clean import data_clean
from ml.preprocess.mining import mining
from ml.preprocess.data_flow import data_flow
from ml.preprocess.mysql_process_unit import mysql_process_unit


class baoer(mining):
    bkj_id = 0

    frq = 0
    bkj_serially = {}
    ret = {}
    ans = []
    def __init__(self):
        pass

    def find_serially(self, data_flow):

        if data_flow.is_row_num_change:

            if data_flow.latest_row[0] in self.ret:
                self.ret[data_flow.latest_row[0]][3] = float(data_flow.latest_row[3])+ float(self.ret[data_flow.latest_row[0]][3])
                if abs(int(self.ret[data_flow.latest_row[0]][1]) - int(self.bkj_serially[data_flow.latest_row[0]])) <= 1:
                    self.bkj_serially[data_flow.latest_row[0]] += 1
                    self.ret[data_flow.latest_row[0]][1] = self.bkj_serially[data_flow.latest_row[0]]
            else:
                self.ret[data_flow.latest_row[0]] = data_flow.latest_row
                self.bkj_serially[data_flow.latest_row[0]] = 0

        return data_flow

    def run(self):
        md = modeling(['id', 'user_id', 'bkj_id', 'time_stamp', 'reverse_deta'],
                      "jc_visitrecord", "where id !=0 ", "ORDER BY time_stamp desc limit 10000")
        # mpu = mysql_process_unit(md)
        # mpu.run()
        # data = mpu.get_data_set()               # 添加结束判断标准

        dc = data_clean()
        md.set_fieldPreProcess_func(dc.removeIdField)  # 数据预处理
        md.set_mining_func(self.find_serially)  # 数据特征处理
        dataFlow, resaults = md.getDataSet()  # 执行数据分析
        self.ans = [[list(self.ret[x])[1],list(self.ret[x])[3] ] for x in self.ret.keys()]

        pass
