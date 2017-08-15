# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from ml.preprocess import features
from numpy import *

import jc.models as models
from jc.baoer.baoer import baoer
from ml.kmeans import KMeans as km
from ml.preprocess.modeling import modeling as modeling
from ml.preprocess.data_clean import data_clean
from ml.preprocess.mining import mining
from ml.preprocess.data_flow import data_flow
from ml.preprocess.mysql_process_unit import mysql_process_unit


# Create your views here.


def index(request):
    Ba = baoer();Ba.run()
    cf1 = [];cf2 = [];bf1 = [];bf2 = [];output = []
    a, b, ids = km.kMeans(Ba.t_f, 2)

    if array(a)[0][1] < array(a)[1][1]:flage = 0
    else:flage = 1
    output.append(["","","","","","频率"])
    for id in range(len(Ba.t_f)):
        if id in ids[flage]:
            cf1.append(Ba.t_f[id])
        else:
            cf2.append(Ba.t_f[id])
            output.append(Ba.ret2csv[id])

    a, b, ids = km.kMeans(Ba.t_b, 2)
    if array(a)[0][1] < array(a)[1][1]:flage = 0
    else:flage = 1
    output.append(["","","","","","板块集"])
    for id in range(len(Ba.t_b)):
        if id in ids[flage]:
            bf1.append(Ba.t_b[id])
        else:
            bf2.append(Ba.t_b[id])
            output.append(Ba.ret2csv[id])
    Ba.output2csv("static/一周的图数据.csv",output,["用户Id","板块集连续性","时间戳","频率特性和","次数"])
    ret = {'cf1': cf1, 'cf2': cf2, 'bf1': bf1, 'bf2': bf2}
    return render(request, 'jc/index.html', {'ret': ret})


def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'jc/article_page.html', {'article': article})


def edited_page(request, edited_id):
    return render(request, 'jc/edited_page.html')


def add_visit_record(request, user_id, bkj_id, time_stamp):
    md = modeling(['id', 'time_stamp'], 'jc_visitrecord',
                  'where user_id = ' + user_id ,' order by time_stamp desc')
    _, resaults = md.getDataSet()
    if len(resaults) != 0:
        models.VisitRecord.objects.create(user_id=user_id,
                                          bkj_id=bkj_id,
                                          time_stamp=time_stamp,
                                          reverse_deta=1000 / abs(float(time_stamp) - float(resaults[0].time_stamp)))
    else:
        models.VisitRecord.objects.create(user_id=user_id,
                                          bkj_id=bkj_id,
                                          time_stamp=time_stamp,
                                          reverse_deta=0)

    return render(request, 'jc/add_visit_record.html')


def show_visit_record(request):
    records = models.VisitRecord.objects.all()
    return render(request, 'jc/show_visit_record.html', {'records': records})
