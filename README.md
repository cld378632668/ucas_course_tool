# ucas_course_tool
国科大自动选课、退课（以开发）｜评教、课件同步、查看作业信息、查看谁和你一起上课、登录校园网（未提交）
鸣谢：两位原作者、王运韬、张逸飞、陈明毅、何厚华。
如果想要学习，联系QQ：378632668，联系时请主动自我介绍和发送简历，谢谢配合。

<font color="red">111</font>

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

