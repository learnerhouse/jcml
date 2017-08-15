# -*- coding: utf-8 -*-

from ml.preprocess.mining import mining
from ml.preprocess.modeling import modeling
from ml.preprocess.data_clean import data_clean
from ml.preprocess.mining import mining
from ml.preprocess.data_flow import data_flow
from ml.preprocess.mysql_process_unit import mysql_process_unit
import csv
import codecs
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class baoer(mining):
    bkj_id = 0

    frq = 0
    bkj_serially = {}
    ret = {}
    t_f = []
    t_b = []
    ret2csv = []

    def __init__(self):
        self.frq = 0
        self.bkj_serially = {}
        self.ret = {}
        self.t_b = []
        self.t_f = []

    def find_serially(self, data_flow):

        if data_flow.is_row_num_change:

            if data_flow.latest_row[0] in self.ret:
                self.ret[data_flow.latest_row[0]][4] += 1
                try:
                    self.ret[data_flow.latest_row[0]][3] = float(data_flow.latest_row[3]) + float(
                        self.ret[data_flow.latest_row[0]][3])
                except:
                    #print (self.ret[data_flow.latest_row[0]])
                    pass
                if abs(int(self.ret[data_flow.latest_row[0]][1]) - int(
                        self.bkj_serially[data_flow.latest_row[0]][0])) == 1:
                    self.bkj_serially[data_flow.latest_row[0]][1] += 300
                elif int(self.ret[data_flow.latest_row[0]][1]) - int(
                        self.bkj_serially[data_flow.latest_row[0]][0])==0:
                    self.bkj_serially[data_flow.latest_row[0]][1] += 30
                self.bkj_serially[data_flow.latest_row[0]][0] = data_flow.latest_row[1]


            else:
                data_flow.latest_row.append(1)
                self.ret[data_flow.latest_row[0]] = data_flow.latest_row
                self.bkj_serially[data_flow.latest_row[0]] = [data_flow.latest_row[1]]
                self.bkj_serially[data_flow.latest_row[0]].append(0)

        return data_flow

    def output2csv(self, name, table, tableName=None):
        with codecs.open(name, "w+", "utf_8_sig") as csvfile:
            cfile = csv.writer(csvfile, dialect="excel")
            if tableName != None:
                cfile.writerow(tableName)
            for row in table:
                cfile.writerow(row)

    def run(self):

        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-7)
        before_n_days = str(time.mktime(yes_time.timetuple()))[:-2] + "000"

        md = modeling(['id', 'user_id', 'bkj_id', 'time_stamp', 'reverse_deta'],
                      "jc_visitrecord", "where id !=0 and time_stamp > " + before_n_days,
                      " ORDER BY time_stamp desc limit 10000")

        high_frq = modeling(["id", "user_id",
                             "bkj_id",
                             "sum(round(reverse_deta)) as freq",
                             "FROM_UNIXTIME(time_stamp/1000,'%%Y-%%m-%%d %%H:%%i:%%s') as ftime "],

                            "jc_visitrecord", "where id !=0 "
                                              "and FROM_UNIXTIME(time_stamp/1000,'%%H:%%i:%%s') > '00:00:00' "
                                              "and FROM_UNIXTIME(time_stamp/1000,'%%H:%%i:%%s') < '23:59:59' "
                                              "AND time_stamp >" + before_n_days,

                            " GROUP BY user_id  ORDER BY sum(round(reverse_deta)) desc limit 20"
                            )
        high_visit = modeling(["id", "user_id",
                               "bkj_id",
                               "count(id) as numberoftimes",
                               "sum(round(reverse_deta)) as freq",
                               "FROM_UNIXTIME(time_stamp/1000,'%%Y-%%m-%%d %%H:%%i:%%s') as ftime "],

                              "jc_visitrecord", "where id !=0 "
                                                "and FROM_UNIXTIME(time_stamp/1000,'%%H:%%i:%%s') > '00:00:00' "
                                                "and FROM_UNIXTIME(time_stamp/1000,'%%H:%%i:%%s') < '23:59:59' "
                                                "AND time_stamp >" + before_n_days,

                              " GROUP BY user_id  ORDER BY count(id)  desc limit 20"
                              )

        # mpu = mysql_process_unit(md)
        # mpu.run()
        # data = mpu.get_data_set()               # 添加结束判断标准

        dc = data_clean()
        md.set_fieldPreProcess_func(dc.removeIdField)  # 数据预处理
        md.set_mining_func(self.find_serially)  # 数据特征处理
        md.getDataSet()  # 执行数据分析

        for x in self.ret.keys():
            try:
                self.t_f.append([float(list(self.ret[x])[4]), float(list(self.ret[x])[3])])
                self.t_b.append([float(list(self.bkj_serially[x])[1]), float(list(self.ret[x])[3])])
                self.ret2csv.append(self.ret[x])
            except:
                #print (self.ret[x])
                pass

        freqSet, result = high_frq.getDataSet(["user_id", "bkj_id", "freq", "ftime"])
        visitSet, visit_resault = high_visit.getDataSet(["user_id", "bkj_id", "numberoftimes", "ftime"])
        self.output2csv("static/最近一周按频率排序.csv", freqSet, ["用户Id", "板块集", "频率", "时间"])
        self.output2csv("static/最近一周按次数排序.csv", visitSet, ["用户Id", "板块集", "次数", "时间"])
