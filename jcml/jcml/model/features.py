# -*- coding: utf-8 -*-
import json
import time
import matplotlib.pyplot as plt

def store(data,filepath):
    with open(filepath, 'w') as json_file:
        json_file.write(json.dumps(data))

def load(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data



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

data = load("data.json")
#data = data_set.find()[0]

x,y = fixData2xy(data,datestart,dateend)

y_view = []
for value in y:
    y_view.append(time.strftime("%Y/%m/%d", time.localtime(float(value))))

xnumbers = countSameIds(x)      # 和异常度成正比{userId:times} 在制定的时间内
ft = sigma_reverse_dx(data["data"])   # 和连续出现的点的时间间隔成反比{userId,sgma(1/dx)}

def getDataset():
    ret = []
    for i in range(len(xnumbers.values())):
        ret.append([xnumbers.values()[i],ft.values()[i]])
    return ret


def getDataset():
    ret = []
    for i in range(len(xnumbers.values())):
        ret.append([xnumbers.values()[i],ft.values()[i]])
    return ret

if __name__ == "__main__":

    data = {}
    # data["last"]=time.strftime("%Y%m%d")
    # store(data)
    fig2 = plt.figure(2)
    plt.plot(xnumbers.values(),ft.values(),'rx')
    plt.show()
    data = load('data.json')
    print data