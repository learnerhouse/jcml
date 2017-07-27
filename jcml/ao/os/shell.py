# -*- coding: utf-8 -*-
import os
import datetime

now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yestoday = yes_time.strftime('%Y-%m-%d')

redis = "| redis-cli --raw -h 3fc46a7aec5f4316.m.cnhza.kvstore.aliyuncs.com -a iamSorry123"

outputfile = yestoday + ".txt"

os.system("echo " + yestoday + "访问板块集最多的前 20 个用户" + ">>" + outputfile)

os.system("echo zrevrange bkjAccess:user:rank:day:"+yestoday+" 0 20 withscores" + redis + ">>" + outputfile)


os.system("echo "+yestoday+"日被访问次数最多的板块集 ID ，名字和访问次数" + ">>" + outputfile)

os.system("echo zrevrange bkjAccess:rank:day:"+yestoday+":all 0 20 withscores" + redis + ">>" + outputfile)




