#!/usr/bin/python3

# 添加上传队列任务

import redis
import sys
import os
import urllib.request
import urllib.parse
import json
import config

# 删除 completed/error/removed 三种状态的任务
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

# 获取任务的“下载目录”，如果是 BT 任务，还要获取“任务名称”
def aria2_tell_status(api, token, gid):
    post_data = '{"jsonrpc":"2.0","method":"aria2.tellStatus","id":"'+gid+'","params":["token:'+token+'","'+gid+'",["dir","bittorrent"]]}'
    post_data = bytes(post_data, encoding='utf8')
    req = urllib.request.Request(api, data=post_data)
    req.add_header('Content-Type', 'application/json;charset=UTF-8')
    result = urllib.request.urlopen(req)
    json_data = json.loads( result.read().decode('utf-8') )

    data = {}
    data['dir'] = json_data['result']['dir'].rstrip('/') + '/'

    # BT 类型
    if 'bittorrent' in json_data['result']:
        data['bt'] = {'name':'', 'mode':''}
        if 'info' in json_data['result']['bittorrent']:
            data['bt']['name'] = json_data['result']['bittorrent']['info']['name']
        if 'mode' in json_data['result']['bittorrent']:
            data['bt']['mode'] = json_data['result']['bittorrent']['mode']
    return data


def main(argv1, argv2, argv3):
    # 读取配置
    conf = config.read()

    gid = argv1  # 任务 GID
    num = int(argv2)  # 文件数
    file_path = argv3.replace('//', '/')  # 文件路径（1.如果是 BT 任务，此文件为一个随机的文件路径; 2.如果创建下载任务时保存目录最后带有/，这个路径会有双//的情况）

    api = conf['api']
    token = conf['token']  # Aria2 令牌
    download_path = conf['download_path']   # Aruia2 下载根目录 (结尾必须有 / )
    google_drive_path = conf['google_drive_path']   # Google Drive 上传根目录

    tell_status = aria2_tell_status(api, token, gid)  # 获取任务详情

    dir_path = tell_status['dir']   # 任务的下载目录路径
    relative_dir_path = dir_path.replace(download_path, '') # 相对文件夹路径

    task_relative_file_path = file_path.replace(dir_path, '')    # 任务相对文件路径

    task_name = task_relative_file_path.split('/')[0]   # 任务文件夹名称

    task_relative_dir_path = os.path.split(task_relative_file_path)[0]  # 任务相对文件夹路径

    r = redis.Redis(host=conf['redis_host'] , port=conf['redis_port'], db=conf['redis_db'], password=conf['redis_password']) # 连接 Redis

    if num < 1: # 文件数量小于 1，下载的可能是最开始的磁力链接任务，所以删除此任务
        aria2_remove_download_result(api, token, gid)
        sys.exit()
        
    elif num == 1 and os.path.exists(file_path):  # 文件数量等于 1 的时候直接传文件
        file_path = file_path.replace('"', '\\"')   # 双引号转义 避免文件或目录中带有双引号导致无法上传
        
        # 如果是 BT 任务，且“任务相对文件夹路径”是空，用任务名称作为“任务相对文件夹路径”（也就是说，如果下载的种子里只有一个文件的情况）
        if 'bt' in tell_status and task_relative_dir_path == '':
            task_relative_dir_path = tell_status['bt']['name']

        command = 'rclone move "'+file_path+'" "'+google_drive_path+relative_dir_path+task_relative_dir_path+'" --ignore-existing --delete-empty-src-dirs 1>/dev/null 2>/dev/null'

    elif num > 1 and os.path.exists(dir_path+task_name):   # 文件数量大于 1 的时候传文件夹
        command = 'rclone move "'+dir_path+task_name+'" "'+google_drive_path+relative_dir_path+task_name+'" --ignore-existing --delete-empty-src-dirs --ignore-case --filter-from "'+conf['filter_file']+'" 1>/dev/null 2>/dev/null'

    else:   # 文件或目录不存在
        sys.exit()

    r.rpush("upload_queue", json.dumps( {"gid":gid, "command":command} ) )  # 添加到上传队列

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
