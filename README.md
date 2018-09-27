# ucas_course_tool

QQ交流群号：516235884

功能列表：
1、国科大自动选课、退课、评教
2、课件自动下载、同步
3、查看作业信息、查看谁和你一起上课、登录校园网


**创始人：沈津生、李博伟、陈黎栋、陈明毅、何厚华**


<font color="red">111</font>

#选课脚本
## 环境依赖
运行环境：Python 2.7-3.5

依赖 `BeautifulSoup` 、｀RawConfigParser｀和 `Requests`，通过如下命令可安装

```
bash> pip install beautifulsoup4
bash> pip install requests
bash> pip install configparser
```
注意包名有大写，但安装的时候都是小写


## 信息配置
在目录下新建 `config` 文件并填入用户名密码及期望动作，格式如下：

```
[info]
username =
password =

[action]
enroll = true
evaluate = false
```

其中

- enroll设置为true表示选课
- evaluate设置为true表示评教

在目录下新建 `courseid` 文件并填入课程，格式如下：

```
091M5023H:on
091M4002H
```

其中

- 课程编号:on #表示该课程选择为学位课
- 课程编号 #表示普通选课

以上例子表示091M5023H作为学位课选课，091M4002H只进行普通选课

## 执行
配置完成后直接执行脚本即可。

```
bash> python3 evaluate.py
bash> Login success
bash> Enrolling start
bash> [Success] 091M5042H
bash> Enrolling finish
```

## 问题及解决方式
Ubuntu系统下脚本可能会出现“No such course”的错误，即使填入的courseid是正确的，可以通过如下方法来修复：

```
bash> sudo locale-gen en_US.UTF-8  
bash> export LC_ALL=en_US.UTF-8
bash> python3 evaluate.py
```

# 国科大课件下载脚本
## 简介
使用教务系统账号、密码登录课程网站，读取选课信息，从所选课程的“讲义课件”中下载该课程的课件

## 脚本功能
1. 自动登录课程网站，获取你所选课程列表
2. 在脚本当前目录下建立以课程名命名的文件夹，下载课件到相应文件夹中
3. 根据文件名判断课件是否已经下载，如课件已存在，则不进行下载

## 脚本使用
### Windows控制台下执行脚本

脚本运行需要requests和bs4库，可用pip安装
```
pip install requests
pip install bs4
```

在脚本所在目录新建`user.txt`文件，将第一行改为你的登录名和密码（以空格分隔）

在脚本所在目录按shift键+鼠标右键，选择"在此处打开命令窗口"，执行命令：
```
python download_courseware.py
```

### 运行exe可执行文件
可下载`download_courseware.exe`文件


在`download_courseware.exe`所在目录新建`user.txt`文件，将第一行改为你的登录名和密码（以空格分隔）


双击运行程序
