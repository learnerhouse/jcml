# -*- coding: utf-8 -*-

import os
import datetime
import MySQLdb

class local:

    def __init__(self,filepath,date):
        self.filepath = filepath
        self.date = date

    userId_bkjVisitTimes = []
    userName_mobile = []
    bkjId_bkjVisiTimes = []
    bkjIds = []
    bkjNames = []
    filepath = ""
    date = ""

    def pretreatTxt(self):
        with open(self.filepath, 'r') as f:
            flage1 = False; flage2 = False; i1 = 0; i2 = 0;
            for line in f.readlines():
                if "访问板块集最多的" in line:
                    flage1 = True; flage2 = False
                    continue
                if "被访问次数最多的板块集" in line:
                    flage2 = True;flage1 = False
                    continue

                if flage1 and i1%2==0:
                    userId = line
                    i1+=1
                elif flage1 and i1%2==1:
                    self.userId_bkjVisitTimes.append([userId,line])
                    i1+=1
                elif flage2 and i2%2==0:
                    bkjId = line
                    self.bkjIds.append(line)
                    i2+=1
                elif flage2 and i2%2==1:
                    self.bkjId_bkjVisiTimes.append([bkjId,line])
                    i2+=1
            return self.userId_bkjVisitTimes ,self.bkjId_bkjVisiTimes

    def getBkjName(self):
        # 打开数据库连接
        db = MySQLdb.connect("139.196.106.83","baoer","baoer_07_19","jcml" )

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        for id in self.bkjIds:
            # SQL 查询语句
            sql = "SELECT name from sset_bankuaijis where id = '%d'" % (int(id))
            try:
               # 执行SQL语句
               cursor.execute(sql)
               # 获取所有记录列表
               results = cursor.fetchall()
               for row in results:
                  name = row[0]
                  # 打印结果
                  print "fname=%s" % (name )
                  self.bkjNames.append(name)
            except:
               print "Error: unable to fecth data"
        # 关闭数据库连接
        db.close()
        return self.bkjNames

    def getUserInfo(self):
        # 打开数据库连接
        db = MySQLdb.connect("139.196.106.83","baoer","baoer_07_19","jcml" )

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        for id in self.userId_bkjVisitTimes:
            # SQL 查询语句
            sql = "SELECT mobile , nickname from user_users where id ='%d'" % (int(id[0]))
            try:
               # 执行SQL语句
               cursor.execute(sql)
               # 获取所有记录列表
               results = cursor.fetchall()
               for row in results:
                  mobile = row[0]
                  nickName = row[1]
                  # 打印结果
                  print "mobile=%s name=%s" % (mobile ,nickName)
                  self.userName_mobile.append([nickName,mobile])
            except:
               print "Error: unable to fecth data"
        # 关闭数据库连接
        db.close()
        return self.userName_mobile

    def output2txt(self):
        try:
            with open('/Users/xiaoren/Desktop/用户'+self.date+'.txt', 'w') as output:
                output.write("电话号码\t\t访问次数 \n")
                for i in range(len(self.userId_bkjVisitTimes)):
                    output.write(str(self.userName_mobile[i][1]).strip()+'\t'+ self.userId_bkjVisitTimes[i][1])

            with open('/Users/xiaoren/Desktop/板块集'+self.date+'.txt', 'w') as output:
                output.write("板块集\t\t\t访问次数 \n")
                for i in range(len(self.bkjId_bkjVisiTimes)):
                    output.write(str(self.bkjNames[i]).strip()+'\t\t\t'+ self.bkjId_bkjVisiTimes[i][1])
        except:
            pass




now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yestoday = yes_time.strftime('%Y-%m-%d')
os.system("scp deploy@121.43.98.23:~/"+yestoday+".txt ~/Desktop/ ")
if __name__ == '__main__':
    localClass = local('/Users/xiaoren/Desktop/'+yestoday+'.txt',yestoday)
    localClass.pretreatTxt()
    localClass.getBkjName()
    localClass.getUserInfo()
    localClass.output2txt()






