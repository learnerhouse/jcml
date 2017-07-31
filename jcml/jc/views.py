# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from numpy import *

import jc.models as models
from jc.ml.kmeans import KMeans as km
from jc.ml.preprocess import features

# Create your views here.

def index(request):
    vr = models.VisitRecord.objects.all().values_list('user_id','bkj_id','time_stamp')
    ft = features.feature(vr)
    f,b = ft.sigma_reverse_dx()
    dataSet_times_f , userId_time_f=ft.get_times_f()#  [figture1 figture2]  次数 f
    dataSet_b_f , userId_b_f= ft.get_b_f()

    a=[];b=[];cf1=[];userId_cf1=[];cf2=[];userId_cf2=[];bf1=[];userId_bf1=[];bf2=[];userId_bf2=[]
    flage = 0
    a, b,ids=km.kMeans(dataSet_times_f,2)

    if array(a)[0][1] < array(a)[1][1]: flage = 0
    else:flage=1
    for id in range(len(dataSet_times_f)):
        if id in ids[flage]:
            cf1.append(dataSet_times_f[id])
            userId_cf1.append(userId_time_f[id])
            models.VisitRecord.objects.filter(user_id=int(userId_time_f[id]))\
                .update(is_crawler=0,
                        visit_times=dataSet_times_f[id][0],
                        visit_freq=dataSet_times_f[id][1],serially=userId_b_f[str(userId_time_f[id])])
        else:
            cf2.append(dataSet_times_f[id])
            userId_cf2.append(userId_time_f[id])
            models.VisitRecord.objects.filter(user_id=int(userId_time_f[id])).update(is_crawler=1)
            models.VisitRecord.objects.filter(user_id=int(userId_time_f[id]))\
                            .update(visit_times=dataSet_times_f[id][0],
                                    visit_freq=dataSet_times_f[id][1],serially=userId_b_f[str(userId_time_f[id])])

    a, b,ids=km.kMeans(dataSet_b_f,2)

    if array(a)[0][1] < array(a)[1][1]: flage = 0
    else:flage=1
    for id in range(len(dataSet_b_f)):
        if id in ids[flage]:
            bf1.append(dataSet_b_f[id])
        else:
            bf2.append(dataSet_b_f[id])
#    models.VisitRecord.objects.filter(user_id=)
    ret = {
           'cf1':cf1,'cf2':cf2,'bf1':bf1,'bf2':bf2,
           'userId_cf1':userId_cf1,'userId_cf2':userId_cf2,
           'userId_bf1':userId_bf1,'userId_bf2':userId_bf2
           }
    return render(request,'jc/index.html',{'ret':ret})

def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request,'jc/article_page.html',{'article':article})

def edited_page(request,edited_id):
    return  render(request,'jc/edited_page.html')


def add_visit_record (request,user_id,bkj_id,time_stamp ):
    resaults = models.VisitRecord\
        .objects.raw('select id, time_stamp from jc_visitrecord where user_id = '+user_id+' order by time_stamp desc')

    if len(list(resaults)) != 0:
        models.VisitRecord.objects.create(user_id=user_id,
                                          bkj_id=bkj_id,
                                          time_stamp=time_stamp,
                                          reverse_deta = 1000/abs(float(time_stamp)-float(resaults[0].time_stamp)))
    else:
        models.VisitRecord.objects.create(user_id=user_id,
                                          bkj_id=bkj_id,
                                          time_stamp=time_stamp,
                                          reverse_deta = 0)

    return render(request,'jc/add_visit_record.html')

def show_visit_record(request):
    records = models.VisitRecord.objects.all()
    return render(request,'jc/show_visit_record.html',{'records':records})