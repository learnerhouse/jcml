# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from jc.model import features,KMeans as km
import json, models

# Create your views here.

def index(request):
#   dataSet=pt.getDataset()

    vr = models.VisitRecord.objects.all().values_list('user_id','bkj_id','time_stamp')
    ft = features.feature(vr)
    f,b = ft.sigma_reverse_dx()
    dataSet_times_f=ft.get_times_f()#  [figture1 figture2]  次数 f
    dataSet_b_f = ft.get_b_f()
    print dataSet_times_f
    a=[];b=[];cf1=[];cf2=[];bf1=[];bf2=[]
    a, b,ids=km.kMeans(dataSet_times_f,2)
    for id in range(len(dataSet_times_f)):
        if id in ids:
            cf1.append(dataSet_times_f[id])
        else:
            cf2.append(dataSet_times_f[id])

    a, b,ids=km.kMeans(dataSet_b_f,2)
    for id in range(len(dataSet_b_f)):
        if id in ids:
            bf1.append(dataSet_b_f[id])
        else:
            bf2.append(dataSet_b_f[id])

    return render(request,'jc/index.html',{'cf1':cf1,'cf2':cf2,'bf1':bf1,'bf2':bf2})

def article_page(request, article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request,'jc/article_page.html',{'article':article})

def edited_page(request,edited_id):
    return  render(request,'jc/edited_page.html')

def add_visit_record (request,user_id,bkj_id,time_stamp ):
    models.VisitRecord.objects.create(user_id=user_id,bkj_id=bkj_id,time_stamp=time_stamp)
    records = models.VisitRecord.objects.all()
    return render(request,'jc/add_visit_record.html',{'records':records})

def show_visit_record(request):
    records = models.VisitRecord.objects.all()
    return render(request,'jc/show_visit_record.html',{'records':records})