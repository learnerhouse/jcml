# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^$', views.index),
]