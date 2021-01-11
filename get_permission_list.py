# -*- coding: utf-8 -*-
# @Time    : 2021/1/11 9:44
# @Author  : LuckyFuture
# @FileName: test.py
# @Software: PyCharm
# @Blog : http://blog.llloverr.com/index.php/index.html

import requests
import re
import ruamel_yaml as yaml


url = 'https://developer.android.com/reference/android/Manifest.permission?hl=zh_cn'
data = requests.get(url)
# print(data.text)
data = data.text.split("<!-- ========= ENUM CONSTANTS DETAIL ======== -->")
detail = data[1]
jingjian = detail.replace('\r','').replace('\n','')
permission_list = re.findall('<div data-version-added=(.*?)Constant Value', jingjian)

yaml_file = {}
num = 1
for permission in permission_list:
    #print(permission)
    api_name = re.findall('<h3 class=\"api-name\" id=\"(.*?)\"', permission)
    api_level = re.match('\"(.*?)\"', permission)

    if ('deprecated' in permission):
        Is_Deprecated = True
    else:
        Is_Deprecated = False
    Protection_level = re.findall('Protection level: (.*?)<', permission)
    if (len(Protection_level) == 0) and Is_Deprecated:
        Protection_level.append('This permission was deprecated')
    elif(len(Protection_level) == 0):
        Protection_level.append('Not for use by third-party applications')

    Description = re.search('<p>(.*?)<p>', permission)
    Description = re.sub('<.*?>', '', Description[0])

    print(api_name[0],Is_Deprecated, api_level[0], Protection_level[0], Description)
    yaml_file[api_name[0]] = {'api_name':api_name[0],'num':num,'api_level':api_level[0][1:-1],'Description':Description,'Protection_level':Protection_level[0],'Is_Deprecated':Is_Deprecated}
    num = num + 1
print(yaml_file)
with open('permission_list.yml', 'w') as nf:
    yaml.dump(yaml_file, nf, Dumper=yaml.RoundTripDumper)


