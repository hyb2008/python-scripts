#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


reload(sys)
sys.setdefaultencoding('utf8')



def get_file():
    day = time.strftime('%Y%m%d', time.localtime(time.time()))
    name = day + "_trade.xlsx"
    filename = '/home/release/trunk/src/release/exchange_bk/' + name 
    pkey = '/home/huyabing/.ssh/id_rsa'
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('101.200.60.142', username='release', pkey=key)
    t = ssh.get_transport()
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(filename,name)
    t.close()
    if os.path.exists(name):
        currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "%s  Download file %s successful" %(currenttime,name)
    return name


def send_mail():
    filename = get_file()
    smtpserver = 'smtp.sohu.com'
    username = 'royunwei@sohu.com'
    password = 'roshyhda'
    sender = 'royunwei@sohu.com'
    receivers = ['274871780@qq.com', '834440967@qq.com']
    msg = MIMEMultipart()
    msg['From'] = 'huyabing'
    msg['To'] = ",".join(receivers)
    subject = '每周交易所数据'
    msg['Subject'] = subject
    msg.attach(MIMEText('交易所数据已发送，请查收。', 'plain', 'utf-8'))
    att = MIMEText(open(filename).read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename=%s' % (filename)
    msg.attach(att)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(smtpserver, 25)
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receivers, msg.as_string())
	current = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "%s  邮件发送成功。" %(current)
    except Exception as e:
        print "%s  邮件发送失败。" %(current)

if __name__ == '__main__':
    send_mail()
