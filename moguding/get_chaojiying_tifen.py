# !/usr/bin/env python
# coding: utf-8

# 获得超级鹰账号剩余的题分
# 作者：江致远
# 作者邮箱：1914813051@qq.com
# 链接：https://www.chaojiying.com/api-5.html
# 修改日期：2021年2月24日


import requests, json
from global_config import *

def get_chaojiying_tifen(chaojiying_usename,chaojiying_password):
    
    github_url = "http://upload.chaojiying.net/Upload/GetScore.php"

    data = json.dumps({'user':chaojiying_usename, 'pass':chaojiying_password})

    r = requests.post(github_url, data)

    a = r.json()

    tifen = a["tifen"]    # tifen,(数值) 题分

    return tifen
