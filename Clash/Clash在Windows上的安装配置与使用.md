# Clash 在 Windows 上的安装配置与使用

由于 Clash 在 Windows 上没有一个图形界面的客户端，在配置与使用的时候存在一些困难和不便，所以写篇日志以便大家参考。

## 环境

- Windows 7 旗舰版


## 下载并安装

- 先到 [https://github.com/Dreamacro/clash/releases](https://github.com/Dreamacro/clash/releases) 这里下载最新版的 `clash-win64.zip` 压缩包到电脑上；
- 把压缩包里的 `clash-win64.exe` 解压出来，放到任意你想放的地方；
- 第一次运行 `clash-win64.exe` 会看到下面的两行提示，意思是：
1. 没有在 `C:\Users\你的电脑用户名\.config\clash` 文件夹中找到配置文件，软件自动创建了一个空的 `config.ini` 配置文件；
2. 没有找到 MMDB IP 地址库，软件自动下载中；
```
←[36mINFO←[0m[0000] Can't find config, create a empty file
←[36mINFO←[0m[0000] Can't find MMDB, start download
```
- 我们等一会儿，发现在 `C:\Users\你的电脑用户名\.config\clash` 目录中的 `Country.mmdb` 文件大小已停止增长，并固定在 3.31 MB 左右，说明这个 IP 库已经下载完成了，那就关掉 `clash-win64.exe` 的运行窗口；


## 配置

对于新手，估计最难的地方就是如何配置了，这里有一个 [配置文件的详细说明示例](https://github.com/Hackl0us/SS-Rule-Snippet/blob/master/LAZY_RULES/clashX.ini)，大家把它复制下来，在它的基础上进行修改会简单很多。

这里特别提一下我在配置过程中遇到的坑：

1. 节点名称和节点组名称不能有特殊符号,好像圆括号也不行，否则软件启动时会报错；
2. ss 的混淆不能使用 `tls` 混淆，只能用 `http` 混淆，否则节点连不上 ( 具体原因不明，macOS 上就没问题 )。

我的这个配置 [config.ini](https://github.com/meishixiu/note/blob/master/Clash/config.ini) 就是根据上面的那个配置示例修改而来。

### 大致解释一下这个配置文件

- `[General]` 部分的常规配置的每一行我已经在里面写了注释这里就不多说；
- `[Proxy]` 部分配置了大量的节点信息 ( 节点的 IP 地址和连接密码我已经去掉了 )；
- `[Proxy Group]` 部分是整个配置文件的核心，我的配置在这里设置了三个代理组，其中两个类型为 `url-test` 的自动测速组 ( 因为我有两家机场，所以把他们两家的节点各分成一组 )。还有一个名叫 `Proxy` ，类型为 `select` 的代理组，这个组里先填写了两家机场的自动测速组的组名 “`Auto星辰, Auto老板娘,`” 然后再填入所有的节点名称。这样做的目的是在软件启动后可以手动选择需要使用的节点或者节点组，至于在 Windows 上如何选择节点，下文中有说明。
- `[Rule]` 部分是 `Rule` 模式的规则，我的这些规则取自 [lhie1](https://github.com/lhie1/Rules) 大佬那里的规则。最后有两条兜底规则比较特殊：一条是在匹配规则的时候，如果上面的规则都没匹配到，而解析出来又是中国 IP 则走直连；一条是在匹配规则的时候，如果上面的规则都没匹配到，而解析出来又不是中国 IP 则走代理。新手如果还是无法理解的话这两条规则不建议修改。

```
GEOIP,CN,DIRECT
FINAL,,Proxy
```

## 设置系统代理

通过系统代理连接 Clash 的好处就是不用在 浏览器、Telegram 等软件内单独给他们设置代理，而是使用上面配置的规则进行智能分流，让所有的流量该走代理的走代理，该走直连的走直连。

我们运行 `clash-win64.exe` ，如果只看到四行这样的提示，说明配置没有问题：

```
←[36mINFO←[0m[0000] RESTful API listening at: 127.0.0.1:8080
←[36mINFO←[0m[0000] HTTP proxy listening at: :7890
←[36mINFO←[0m[0000] SOCKS proxy listening at: :7891
←[36mINFO←[0m[0000] Redir proxy listening at: :7892
```

![设置系统代理](https://github.com/meishixiu/note/raw/master/Clash/设置系统代理.png)

打开 IE 浏览器，选择 “工具 -> Internet 选项”，然后根据上图箭头顺序打开“代理服务器设置”，在里面填写代理服务器的地址和端，注意“套接字”类型的端口是 `7891`，其他的都是 `7890` ，服务器地址填写 `127.0.0.1` 。

## 使用 GUI 选择节点和模式切换

![GUI](https://github.com/meishixiu/note/raw/master/Clash/GUI.png)

由于 Clash 在 Windows 上没有一个图形界面的客户端，在使用的时候切换节点和模式非常的不方便，所以我用 html+js 写了一个简单的图形界面的客户端 ( 我不太懂前端技术，丑是丑了点，但将就用吧 )。

下载 [ClashGUI.zip](https://github.com/meishixiu/note/raw/master/Clash/ClashGUI.zip) ，解压出 `ClashGUI.html` 文件，在 Clash 运行的时候用 Google Chrome 浏览器打开 `ClashGUI.html` 就可以切换模式和选择节点了。

我选择了一个自动测速组，然后在浏览器里访问 [https://twitter.com](https://twitter.com) ，如果能够打开，说明我们的配置与节点都没有问题。


## 后台运行

正常情况下 `clash-win64.exe` 是在前台运行的，最小化后也会在底部的任务栏里留下一个任务，无法隐藏，不能关闭，总放那看着又碍眼。所以我们得想办法把它隐藏到后台运行，通过 Google 找到一个方法：

- 下载并安装 `Bat To Exe Converter` 这个软件，如果官网不好下载的话，可以使用我提供的这个 [安装包](https://github.com/meishixiu/note/raw/master/Clash/Bat_To_Exe_Converter.zip)；
- 打开 `Bat To Exe Converter` ，在左侧编辑器中填写

```
.\clash-win64.exe
```
- 在右侧“选项”中 `EXE 格式` 选择 `64位 | Windows（隐形）`；
- 在上面的“工具”栏中点击 `保存`，名称任意，位置任意；
- 最后在“工具”栏中点击 `转换`，名称任意 ( 我取名叫 `clash-win64-后台.exe` )，保存位置必须与 `clash-win64.exe` 在同一文件夹内。

如果觉得麻烦或者不会做，可以下载我做好的 [clash-win64-后台.zip](https://github.com/meishixiu/note/raw/master/Clash/clash-win64-后台.zip)，只需要把它解压后放到 `clash-win64.exe` 同一文件夹内运行即可。

这样我们就做好了一个可以让 `clash-win64.exe` 再后台运行的程序，双击运行 `clash-win64-后台.exe`，`clash-win64.exe` 就启动了。启动后我们会发现看不见任何程序运行的效果，因为他们都在后台运行。要查看的话需要在任务栏上“右键 -> 启动任务管理器 -> 进程”中去查看。如果要关闭或重启 Clash，只需要结束掉 `clash-win64.exe` 的进程就可以了，如下图所示。

![进程](https://github.com/meishixiu/note/raw/master/Clash/进程.png)


## 开机启动

1. 右键 `clash-win64-后台.exe` ，选择 `创建快捷方式`；
2. 打开 `C:\Users\你的电脑用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\` ，把刚才创建的快捷方式复制到这个文件夹里就可以实现开机启动了。