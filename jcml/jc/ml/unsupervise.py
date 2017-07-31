# --*-- coding=utf-8 --*--
import time

import matplotlib.pyplot as plt
import numpy
from sklearn import linear_model

from jc.ml.preprocess import features as pt


def fixData2xy (data,dateStart,dateEnd):
    x=[]
    y=[]
    for cell in data["data"]:
        if float(cell[0]['time'])>=time.mktime(time.strptime(dateStart,'%Y-%m-%d %H:%M:%S')) \
                and float(cell[0]['time'])<time.mktime(time.strptime(dateEnd,'%Y-%m-%d %H:%M:%S')):
            x.append(cell[0]['id'])
            y.append(cell[0]['time'])
    return x,y

def countSameIds(ids):
    x = {}
    for id in ids:
        try:
            x[id]+=1
        except KeyError:
            x[id]=1
    return x

def sigma_reverse_dx (data):
    f = {}; tmp = {}
    for cell in data:
        if tmp.has_key(str(cell[0]["id"])):
            f[str(cell[0]["id"])] += 3600/abs(float(cell[0]["time"])-tmp[str(cell[0]["id"])])
            tmp[str(cell[0]["id"])] = float(cell[0]["time"])
        else:
            f[str(cell[0]["id"])] = 0.0
            tmp[str(cell[0]["id"])] = float(cell[0]["time"])
    return f

datestart = "2017-07-04 00:00:00";dateend = "2017-07-07 23:00:00"

data = pt.load("data.json")
#data = data_set.find()[0]

x,y = fixData2xy(data,datestart,dateend)

y_view = []
for value in y:
    y_view.append(time.strftime("%Y/%m/%d", time.localtime(float(value))))

print x,y_view

xnumbers = countSameIds(x)      # 和异常度成正比{userId:times} 在制定的时间内
#sorted(xnumbers.keys())
print xnumbers



fig1 = plt.figure(1)
plt.subplot(211)
ft = sigma_reverse_dx(data["data"])   # 和连续出现的点的时间间隔成反比{userId,sgma(1/dx)}
#sorted(ft.keys())
plt.plot(ft.keys(),ft.values(),"rx")
plt.margins(0.08)
plt.subplots_adjust(bottom=0.15)
plt.xlabel("userId"+" from "+datestart+" to "+dateend)
plt.ylabel("sigma reverse dx")

plt.subplot(212)
plt.plot(xnumbers.keys(),xnumbers.values(),'rx')
plt.xlabel("userId"+" from "+datestart+" to "+dateend)
plt.ylabel("visits")
plt.margins(0.08)
plt.subplots_adjust(bottom=0.15)

ret = []
for i in range(len(xnumbers.values())):
    ret.append([xnumbers.values()[i],ft.values()[i]])

print ret

# weight=[1 for i in range(len(ft.values()))]
# print weight

clf = linear_model.LinearRegression()
clf.fit(ret,ft.values())
print('Coefficients:\n',clf.coef_)

fig2 = plt.figure(2)
plt.plot(xnumbers.values(),ft.values(),'rx')

x = numpy.arange(0, 5, 0.1)
#plt.plot(x,clf.coef_[1]*x+clf.coef_[0],'r-')
plt.xlabel("visits"+" from "+datestart+" to "+dateend)
plt.ylabel("sigma reverse dx")
plt.margins(0.08)
plt.subplots_adjust(bottom=0.15)
plt.show()
