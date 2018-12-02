#!/usr/bin/python3

# 消费上传队列任务

import redis
import sys
import os
import json
import urllib.request
import urllib.parse
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

if __name__ == "__main__":
    main()