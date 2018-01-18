# -*- coding:utf8 -*-

import requests

r = requests.get('https://www.baidu.com')
print("Response.content:"+str(r.content))
print("Response.cookies:"+str(r.cookies))
print("Response.headers:"+str(r.headers))
print("Response.history:"+str(r.history))
print("Response.text:"+str(r.text))
print("occupy for debug ")