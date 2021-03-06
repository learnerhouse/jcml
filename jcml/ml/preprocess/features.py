# -*- coding: utf-8 -*-
import json
import time
import matplotlib.pyplot as plt
#from DB import db
class feature:
    def __init__(self,data):
        self.data = data

    def store(self,filepath):
        with open(filepath, 'w') as json_file:
            json_file.write(json.dumps(self.data))

    def load(self,filepath):
        with open(filepath) as json_file:
            data = json.load(json_file)
            return data



    def fixData2xy (self,dateStart,dateEnd):
        x=[]
        y=[]
        for cell in self.data:
              if float(cell[2])>=time.mktime(time.strptime(dateStart,'%Y-%m-%d %H:%M:%S')) \
                      and float(cell[2])<time.mktime(time.strptime(dateEnd,'%Y-%m-%d %H:%M:%S')):
                x.append(cell[0])
                y.append(cell[2])
        return x,y

    def countSameIds(self,ids):
        x = {}
        for id in ids:
            if id in x.keys():
                x[id]+=1
            else:
                x[id]=1
        return x

    threshold = 60.0
    def sigma_reverse_dx (self):#data 要按照时间排序
        f = {}; tmp = {};lastB={};b = {}
        tmpB ={}
        for cell in self.data:
            if str(cell[0]) in tmp.keys():
                if float(cell[2])-tmp[str(cell[0])] ==0:
                    f[str(cell[0])] += self.threshold/0.5
                else:
                    f[str(cell[0])] += self.threshold/abs(float(cell[2])-tmp[str(cell[0])])
                    if abs(int(cell[1]) - lastB[str(cell[0])]) == 1:
                        tmpB[str(cell[0])] += 2
                    elif int(cell[1]) - lastB[str(cell[0])] == 0:
                        tmpB[str(cell[0])] += 1
                    else:
                        if tmpB[str(cell[0])] > b[str(cell[0])]:
                            b[str(cell[0])] = tmpB[str(cell[0])]
                        tmpB[str(cell[0])] = 1
                    tmp[str(cell[0])] = float(cell[2])
                    lastB[str(cell[0])] = int(cell[1])
            else:
                f[str(cell[0])] = 0.0
                b[str(cell[0])] = 1
                tmpB[str(cell[0])] = 1
                tmp[str(cell[0])] = float(cell[2])
                lastB[str(cell[0])] = int(cell[1])
        return f,b


    datestart = "2017-07-23 00:00:00";dateend = "2017-07-24 23:00:00"

    #data = load("data.json")

    #data = db["jcml"].find()[0]

    def get_times_f(self):
        x,y = self.fixData2xy(self.datestart,self.dateend)
        xnumbers = self.countSameIds(x)      # 和异常度成正比{userId:times} 在制定的时间内
        ft,b = self.sigma_reverse_dx()       # 和连续出现的点的时间间隔成反比{userId,sgma(1/dx)}
        ret = [];userId =[]
        for i in xnumbers.keys():
            ret.append([xnumbers[i],ft[str(i)]])
            userId.append(i)
        return ret,userId

    def get_b_f(self):
        ret = [];
        x,y = self.fixData2xy(self.datestart,self.dateend)
        ft,b = self.sigma_reverse_dx()   # 和连续出现的点的时间间隔成反比{userId,sgma(1/dx)}
        xnumbers = self.countSameIds(x)      # 和异常度成正比{userId:times} 在制定的时间内
        for i in range(len(xnumbers.values())):
            ret.append([list(b.values())[i]/list(xnumbers.values())[i],list(ft.values())[i]])
        return ret,b


    def getDataset(self):
        ret = []
        x,y = self.fixData2xy(self.datestart,self.dateend)
        xnumbers = self.countSameIds(x)      # 和异常度成正比{userId:times} 在制定的时间内
        for i in range(len(xnumbers.values())):
            ret.append([list(xnumbers.values())[i],list(ft.values())[i]])
        return ret

    if __name__ == "__main__":

        data = {}
        # data["last"]=time.strftime("%Y%m%d")
        # store(data)
        data = load('data.json')
        fig2 = plt.figure(2)
        plt.plot(xnumbers.values(),ft.values(),'rx')
        plt.show()
