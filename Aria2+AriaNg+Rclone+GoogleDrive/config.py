#!/usr/bin/python3

def read():
    config = {
                "api": "http://127.0.0.1:6800/jsonrpc", # Aria2 RPC 地址
                "token": "ec3c14e036ed3051e1d1",    # Aria2 RPC 令牌
                "download_path": "/home/wwwroot/lixian.xxx.com/down/",  # Aruia2 下载目录 ( 结尾必须有 / )
                "google_drive_path": "gd:Download/",    # Google Drive 上传目录 ( 如果是子目录，结尾必须有 / )
                "filter_file": "/home/filter-file.txt", # rclone 上传文件夹时的过滤规则文件路径
                "redis_host": "127.0.0.1",  # Redis 主机地址
                "redis_port": 6379, # Redis 端口
                "redis_db": 0,  # 使用的 Redis 数据存储库
                "redis_password": None, # Redis 连接密码 ( None 是无密码 )
            }
    return config