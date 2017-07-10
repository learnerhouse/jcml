# --*-- coding=utf-8 --*--
import urllib2
import urllib
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator, FormatStrFormatter

weatherHtml = urllib.urlopen('http://sh.fangjia.com/trend/year2Data?defaultCityName=上海&districtName=&region=&block=&keyword=')
#通过urllib模块中的urlopen的方法打开url
weatherHtml1 = weatherHtml.read()
#通过read方法获取返回数据
print "url返回的json数据：",weatherHtml1
#打印返回信息
weatherJSON = json.loads(weatherHtml1)
#将返回的json格式的数据转化为python对象，json数据转化成了python中的字典，按照字典方法读取数据
print "python的字典数据：",weatherJSON
data = weatherJSON["series"][0]["data"]
xlable = []
x = []
y = []
for pt in data:
    xlable.append(time.strftime("%Y/%m/%d", time.localtime(pt[0]/1000)))
    x.append(pt[0])
    y.append(pt[1])
print x
print y
plt.title('')
plt.plot(x,y,'r')
#plt.xlabel(xlable)
plt.show()
# print "lists列表的数据",weatherJSON["data"]["lists"][0]
# #lists里面的数据是一个列表（按照序列编号来查看数据）
# print weatherJSON["data"]["lists"][0]["SongName"]
#lists的0号数据是一个字典，按照字典方法查看数据