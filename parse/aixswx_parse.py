#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:aixswx_parse.py
# 创建日期:2022/3/23 17:29
# 作者:XU
# 联系邮箱:iswongx@163.com

import re

#解析 www.aixswx.com

def aixswx_par(data,dict):
    dict_details = {}
    author = re.findall('<a.*?class="author fl">(.*?)</a>', data, re.S)
    if author:
        dict_details['author'] = author[0].replace('作者：', '').replace('&nbsp;', '').strip()
    else:
        dict_details['author'] = ''
    description = re.findall('<b>导读：</b>(.*?)<b>', data, re.S)
    if description:
        dict_details['describe'] = description[0].replace('\r\n', '').replace('&nbsp;', '').strip().replace('<br/>', '')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall('<span class="name fl">(.*?)</span>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details