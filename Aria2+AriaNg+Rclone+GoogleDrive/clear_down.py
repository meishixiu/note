#!/usr/bin/python3

# 清理下载目录
# 如果没有 下载、暂停、停止\完成 几种状态的任务时，且下载目录不为空时就清空下载目录，这样可以清理 Aria2 和被 rclone 过滤的小文件。

import redis
import sys
import os
import shutil
import json
import urllib.request
import urllib.parse
import config

def aria2_get_global_stat(api, token):
    data = '{"jsonrpc":"2.0","method":"aria2.getGlobalStat","id":"id","params":["token:'+token+'"]}'
    data = bytes(data, encoding='utf8')
    req = urllib.request.Request(api, data=data)
    req.add_header('Content-Type', 'application/json;charset=UTF-8')
    result = urllib.request.urlopen(req)
    data = json.loads( result.read().decode('utf-8') )
    if data['result']['numActive'] == '0' and data['result']['numWaiting'] == '0' and data['result']['numStopped'] == '0' :
        return True
    else:
        return False


def main():
    # 读取配置
    conf = config.read()

    if os.path.exists(conf['download_path']) is False : # 下载目录不存在
        sys.exit()

    if aria2_get_global_stat(conf['api'], conf['token']) :  # 无任务，删除下载目录
        shutil.rmtree(conf['download_path'])

if __name__ == "__main__":
    main()