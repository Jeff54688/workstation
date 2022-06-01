[TOC]



------

# 一.Linux Base

## 1.帮助命令

```
whatis command   whatis -w "xargs"  正则匹配
info command  更详细的文档说明
man command man分为9类，常用1(可操作命令)，3(函数与数据库)  man 3 printf
man -k GNOME config | grep 1  -k 查询关键字
which xargs  查询binary文件所在路径  which make make程序安装路径
whereis xargs  查看程序的搜索路径，查询同一软件多版本
-h --help 

```

## 2.文件及目录管理

文件管理不外乎文件或目录的创建、删除、查询、移动，有mkdir/rm/mv；文件查询是重点，用find来进行查询

### 2.1创建和删除

- 创建：mkdir
- 删除：rm
- 删除非空目录：rm -rf file目录
- 删除日志 rm *log (等价: $find ./ -name “*log” -exec rm {} ;)
- 移动：mv  重命名
- 复制：cp (复制目录：cp -r )
- 查询：find ./ | wc -l    统计当前目录下文件个数

### 2.2目录切换

- 切换到上一个工作目录： cd -

- 按修改时间排序，以列表的方式显示目录项 ls -lrt  

### 2.3查找目录及文件

```
find ./ -name "core*" | xargs file  搜寻文件或目录
find ./ -name ".o" -exec rm {} \;  递归当前目录及子目录删除所有.o文件
locate passwd  locate /etc/sh 以sh开头的文件 locate -i ~/r 忽略大小写
locate 只在 /var/lib/slocate 资料库中找，一般文件数据库在 /var/lib/slocate/slocate.db 中，所以 locate 的查找并不是实时的，而是以数据库的更新为准，一般是系统自己维护，也可以手工升级数据库 ，命令为：
```



## 文本处理

## 7.网络工具

**netstat** 显示各种网络相关信息

```
netstat -anp：显示系统端口使用情况
netstat -nupl：UDP类型的端口
netstat -ntpl：TCP类型的端口
netstat -na|grep ESTABLISHED|wc -l：统计已连接上的，状态为"established"
netstat -l：只显示所有监听端口
netstat -lt：只显示所有监听tcp端口
netstat -antpl | grep 6379   
```

**查询端口运行什么程序**

lsof -i:7902 先查pid     ps -ef | grep pid 

**route -n**   查看路由状态

```
添加到主机的路由
route add -host 192.168.1.132 gw 192.168.1.1 dev eth0

添加到网络的路由
route add -net 192.168.1.0/24 (ornetmask 255.255.255.0) gw 192.168.1.1 dev eth0

添加默认路由
route add default gw 192.168.1.1

删除路由
route del -host 192.168.1.2 gw 192.168.1.1 dev eth0
route del -net 192.168.1.0 netmask 255.255.255.0  gw 192.168.1.1 dev eth0
route del default gw 192.168.1.1      route del default   删除所有的默认路由
```

host domain    DNS查询

**wget** 

```
wget http://mirrors.163.com/.help/CentOS7-Base-163.repo  下载到当前目录
wget -O wordpress.zip http://www.centos.bz/download.php?id=1080   以不同的文件名保存
wget -o download.log URL    下载信息存入日志文件
wget -limit-rate=300k http://        限速下载
wget -c http://     断点续传 文件较大下载时使用
wget -b http://     后台下载 tail -f wget-log     查看下载进度
wget –tries=40 URL    wget默认重试20次连接下载文件。–tries增加重试次数
wget -i filelist.txt   下载文件中的链接
wget -reject=gif url    过滤指定格式 .gif图片

```

**curl**

```
curl -o home.html https://www.gdut.edu.cn/xxgk/xxjj.htm   抓取页面内容到文件
curl https://www.gdut.edu.cn/xxgk/xxjj.htm >home.html 抓取页面内容,GET请求
curl -C -O http://www.mydomain.com/linux/index.html     断点续传  -O url要具体到文件 index.html
curl -# -o     显示下载进度条     curl -f http        显示抓取错误
curl -d "user=nickname&password=12345" http://www.yahoo.com/login.cgi   POST请求
curl -e http://localhost  http://         伪造来源地址，有的网站会判断，请求来源地址
curl -x 10.0.1.3:80 -o home.html http:         使用代理ip
curl -r 0-100 - o img.part1 http://mydomian.cn/thumb/xxx.jpg     分段下载，组合查看cat img.part* > img.jpg
curl -r 100-200 -o img.part2 http://mydomian.cn/thumb/xxx.jpg     n
curl -user user:passwd https://http://blog.mydomain.com/login.php     模拟登录   -u ftp下载
curl -O [ftp://xukai:test@192.168.242.144:21/www/focus/enhouse/index.php](ftp://xukai:test@192.168.242.144:21/www/focus/enhouse/index.php)    ftp下载
curl -T xukai.php [ftp://xukai:test@192.168.242.144:21/www/focus/enhouse/](ftp://xukai:test@192.168.242.144:21/www/focus/enhouse/)    ftp上传
$curl -x 123.45.67.89:1080 -o page1.html -D cookie0001.txt http://mydomain.net    保存cookie
```

**ftp/sftp文件传输:**

```
$sftp ID@host
```

登陆服务器host，ID为用户名。sftp登陆后，可以使用下面的命令进一步操作：

```
- get filename # 下载文件
- put filename # 上传文件
- ls # 列出host上当前路径的所有文件
- cd # 在host上更改当前路径
- lls # 列出本地主机上当前路径的所有文件
- lcd # 在本地主机更改当前路径
```

将本地localpath指向的文件上传到远程主机的path路径:

```
$scp localpath ID@host:path
```

以ssh协议，遍历下载path路径下的整个文件系统，到本地的localpath:

```
$scp -r ID@site:path localpath
```

## 8.用户管理工具

用户

用户的组

用户权限

## 9.系统管理及IPC资源管理

uname -a   内核版本号     lsb_release -a   Ubuntu版本

more /etc/release   cat /etc/redhat-release

sar -u 5 10     查看CPU采样时间内的负载   5秒统计一次 统计10次  

- ```
  - %user：用于表示用户模式下消耗的 CPU 时间的比例；
  - %nice：通过 nice 改变了进程调度优先级的进程，在用户模式下消耗的 CPU 时间的比例；
  - %system：系统模式下消耗的 CPU 时间的比例；
  - %iowait：CPU 等待磁盘 I/O 导致空闲状态消耗的时间比例；
  - %steal：利用 Xen 等操作系统虚拟化技术，等待其它虚拟 CPU 计算占用的时间比例；
  - %idle：CPU 空闲时间比例。
  ```

  

sar -d 3 5    查看系统磁盘读写性能

- ```
  -   tps：每秒从物理磁盘 I/O 的次数。注意，多个逻辑请求会被合并为一个 I/O 磁盘请求，一次传输的大小是不确定的；
  - rd_sec/s：每秒读扇区的次数；
  - wr_sec/s：每秒写扇区的次数；
  - avgrq-sz：平均每次设备 I/O 操作的数据大小（扇区）；
  - avgqu-sz：磁盘请求队列的平均长度；
  - await：从请求磁盘操作到系统完成处理，每次请求的平均消耗时间，包括请求队列等待时间，单位是毫秒（1 秒=1000 毫秒）；
  - svctm：系统处理每次请求的平均时间，不包括在请求队列中消耗的时间；
  - %util：I/O 请求占 CPU 的百分比，比率越大，说明越饱和。
  
  ```

cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c       查看CPU信息（型号）

cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l     # 查看物理CPU个数

cat /proc/cpuinfo| grep "cpu cores"| uniq     查看每个物理CPU中core的个数(即核数)

cat /proc/cpuinfo| grep "processor"| wc -l      查看逻辑CPU的个数

arch  查看架构       pagesize  显示内存page大小     date  显示时间

**ipcs  查看系统使用IPC资源**

ipcs        IPC 主要有消息队列、信号量和共享内存3种机制,一个 IPC 至少包含 key值、ID值、拥有者、权限和使用的大小等关键信息

**检测和设置系统资源限制**
ulimit – a      显示当前所有的系统资源limit 信息

ulimit – c unlimited     对生成的 core 文件的大小不进行限制













