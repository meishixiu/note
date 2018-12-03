#!/usr/bin/python3

# 消费上传队列任务

import redis
import sys
import os
import json
import urllib.request
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import config

def aria2_remove_download_result(api, token, gid):
    data = '{"jsonrpc":"2.0","method":"aria2.removeDownloadResult","id":"'+gid+'","params":["token:'+token+'","'+gid+'"]}'
    data = bytes(data, encoding='utf8')
    req = urllib.request.Request(api, data=data)
    req.add_header('Content-Type', 'application/json;charset=UTF-8')
    result = urllib.request.urlopen(req)
    data = json.loads( result.read().decode('utf-8') )

    if data['result'] == 'OK' :
        return True
    else:
        return False

def send_mail( mail_subject, mail_body, to_addrs ):
    # 读取配置
    conf = config.read()

    if conf['enable_mail'] == False :
        return True

    try:
        msg = MIMEText( mail_body, 'html', 'utf-8' )
        msg['From'] = formataddr(["离线下载通知", conf['smtp_username']])
        msg['To'] = to_addrs
        msg['Subject'] = Header(mail_subject, 'utf-8')
        if conf['smtp_mode'] == 1 :
            server = smtplib.SMTP(conf['smtp_server'], conf['smtp_port'])
        else:
            server = smtplib.SMTP_SSL(conf['smtp_server'], conf['smtp_port'])
        server.login(conf['smtp_username'], conf['smtp_password'])
        server.sendmail(conf['smtp_username'], to_addrs, msg.as_string())
        server.quit()  # 关闭连接
        return True
    except Exception:
        return False

def main():
    # 读取配置
    conf = config.read()

    r = redis.Redis(host=conf['redis_host'] , port=conf['redis_port'], db=conf['redis_db'], password=conf['redis_password']) # 连接 Redis

    upload_task_lock = r.get("upload_queue_lock")  # 获取上传任务锁
    
    # 有任务正在上传就跳过
    if upload_task_lock is not None:
        sys.exit()

    # 出队
    upload_task = r.lpop("upload_queue")

    # 没有上传任务
    if upload_task is None:
        sys.exit()

    # 把 Redis 里存的字符串转成 json 对象
    upload_task = json.loads(upload_task)

    # 设置上传任务锁
    r.set("upload_queue_lock", "lock")
    
    # 开始上传
    os.system(upload_task['command'])

    # 任务执行完后删除任务锁
    r.delete("upload_queue_lock")

    # 上传完后删除 Aria2 中的任务
    aria2_remove_download_result(conf['api'], conf['token'], upload_task['gid'])

    # 发送邮件通知
    mail_body = '<b>' + upload_task['task_name'] + '</b> 离线下载任务已完成，并上传到了 <b>' + upload_task['save_path'] + '</b>'
    send_mail( conf['mail_subject'], mail_body, conf['to_addrs'] )

if __name__ == "__main__":
    main()