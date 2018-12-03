#!/usr/bin/python3

def read():
    config = {
                # Aria2 连接配置
                "api": "http://127.0.0.1:6800/jsonrpc", # Aria2 RPC 地址
                "token": "ec3c14e036ed3051e1d1",    # Aria2 RPC 密钥
                
                # rclone 上传配置
                "download_path": "/home/wwwroot/lixian.xxx.com/down/",  # Aruia2 下载目录 ( 结尾必须有 / )
                "google_drive_path": "gd:Download/",    # Google Drive 上传目录：前缀 gd 是配置 rclone 是取的名字；后缀是指定上传到 GD 的那个目录里 ( 如果指定目录，结尾必须有 / )
                "filter_file": "/home/filter-file.txt", # rclone 上传文件夹时的过滤规则文件路径
                
                # Redis 配置
                "redis_host": "127.0.0.1",  # Redis 主机地址
                "redis_port": 6379, # Redis 端口
                "redis_db": 0,  # 使用的 Redis 数据存储库
                "redis_password": None, # Redis 连接密码 ( None 是无密码 )
                
                # 邮件通知配置
                "enable_mail": False,                   # 是否启用邮件通知 ( True: 启用； False: 禁用 )
                "smtp_server": "smtp.qq.com",           # SMTP 服务器
                "smtp_port": 465,                       # SMTP 端口号 ( 普通模式一般是 25 端口，SSL 模式一般是 465 端口 )
                "smtp_mode": 2,                         # SMTP 连接模式 ( 1: 使用普通模式； 2: 使用 SSL 模式 ) 
                "smtp_username": "10000@qq.com",        # SMTP 帐号
                "smtp_password": "iknkmstvfmdqbida",    # SMTP 密码 ( 如果使用 QQ 邮箱发件，请在电脑上用浏览器打开 QQ 邮箱，然后 邮箱设置 -> 帐户 -> 生成授权码，使用授权码来作为这里的 SMTP 密码 )
                "to_addrs": "10000@qq.com",             # 收件邮箱
                "mail_subject": "有离线下载任务已完成",     # 邮件标题
            }
    return config