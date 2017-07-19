# -*- coding: utf-8 -*-
'''
@author: hakuri
'''
import json

from numpy import *
import matplotlib.pyplot as plt
import features as pt


def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) #map all elements to float()
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))#create centroid mat
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(array(dataSet)[:,j])
        rangeJ = float(max(array(dataSet)[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]             #获取行数
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points                                       #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(array(centroids)[j,:],array(dataSet)[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
#         print nonzero(array(clusterAssment)[:,0]
        for cent in range(k):#recalculate centroids
                ptsInClust = dataSet[nonzero(array(clusterAssment)[:,0]==cent)[0][0]]#get all the point in this cluster
                centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean

    id=nonzero(array(clusterAssment)[:,0]==cent)[0]
    return centroids, clusterAssment,id

def plotBestFit(dataSet,id,centroids):

    dataArr = array(dataSet)
    cent=array(centroids)
    n = shape(dataArr)[0]
    n1=shape(cent)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    xcord3=[];ycord3=[]
    j=0
    for i in range(n):
        if j in id:
            xcord1.append(dataArr[i,0]); ycord1.append(dataArr[i,1])
        else:
            xcord2.append(dataArr[i,0]); ycord2.append(dataArr[i,1])
        j=j+1
    for k in range(n1):
          xcord3.append(cent[k,0]);ycord3.append(cent[k,1])

    fig = plt.figure(fignum)
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
#    ax.scatter(xcord3, ycord3, s=50, c='black')
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.show()



if __name__=='__main__':

    dataSet_times_f=pt.get_times_f()#  [figture1 figture2]  次数 f

    dataSet_b_f = pt.get_b_f()
#   print randCent(dataSet,2)
#   print dataSet

    print  kMeans(dataSet_times_f,2)
    a=[]
    b=[]
    a, b,id=kMeans(dataSet_b_f,2)
    plotBestFit(dataSet_b_f,id,a)

    a1=[]
    b1=[]
    a1, b1,id1=kMeans(dataSet_times_f,2)
    plotBestFit(dataSet_times_f,id1,a1)



