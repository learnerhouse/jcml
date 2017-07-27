# -*- coding: UTF-8 -*-
'''
发送txt文本邮件
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class mail:

    def __init__(self):
        pass

    mail_host="smtp.163.com"  #设置服务器
    mail_user="freedomichael"    #用户名
    mail_pass="xiao10123813"   #口令
    mail_postfix="163.com"  #发件箱的后缀
    nickname = "michael"

    def send_mail(self,to_list,sub,content,attachs):
        me=self.nickname+"<"+self.mail_user+"@"+self.mail_postfix+">"

        #创建一个带附件的实例
        msg = MIMEMultipart()
        for attach in attachs:
            #构造附件1
            att1 = MIMEText(open(attach[1], 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="'+attach[0]+'"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
            msg.attach(att1)

        txtmsg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg.attach(txtmsg)

        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False

if __name__ == '__main__':
    attachs = [['2017-07-25.txt','/Users/xiaoren/Desktop/实习/7_27/2017-07-25.txt']]
    # mailto_list=['434835764@qq.com','chenfei@wallstreetcn.com','fengzhihao@wallstreetcn.com']
    mailto_list = ['freedomichael@163.com']
    mail = mail()
    if mail.send_mail(mailto_list,"michael","不要再屏蔽我了好吗！！！！！！",attachs):
        print "发送成功"
    else:
        print "发送失败"